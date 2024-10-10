#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from string import Template
import subprocess, re, json, gzip
import tempfile
from datetime import datetime
from mmtk_dev.constants import MMTK_DEV, MMTK_OPENJDK, OPENJDK, DACAPO_CHOPIN, PROBES
import os

BPFTRACE_SCRIPT = MMTK_DEV / "scripts" / "bpf" / "wp.bt"
MMTK_BIN_X = OPENJDK / "build" / "linux-x86_64-normal-server-release" / "jdk" / "lib" / "server" / "libmmtk_openjdk.so"
MMTK_BIN = OPENJDK / "build" / "linux-x86_64-normal-server-release" / "images" "jdk" / "lib" / "server" / "libmmtk_openjdk.so"

BPFTRACE_BIN = "bpftrace"


class BPFTraceDaemon:
    def __init__(self, process: subprocess.Popen, temp_file: Path, stdout_file: Path):
        self.__process = process
        self.__now = datetime.now()
        self.__temp_file = temp_file
        self.__stdout_file = stdout_file

    def finalize(self, name: str):
        print("Finalizing trace capture ...")
        returncode = self.__process.wait()
        stdout = self.__stdout_file.read_text()
        if returncode != 0:
            print(stdout)
        assert returncode == 0, f"bpftrace failed with return code {self.__process.returncode}"
        time_str = self.__now.strftime("%Y-%m-%d-%H%M%S")
        url = LogProcessor.process(stdout, Path(f"{name}-{time_str}.json.gz"))
        # Delete the temporary file
        self.__temp_file.unlink(missing_ok=True)
        self.__stdout_file.unlink(missing_ok=True)
        if url is not None:
            print("Trace Preview Link:", url)


def start_capturing_process(exploded: bool, name="wp"):
    mmtk_bin = MMTK_BIN_X if exploded else MMTK_BIN
    if not mmtk_bin.exists():
        raise RuntimeError(f"MMTk binary {str(mmtk_bin)} not found.")
    template = Template(BPFTRACE_SCRIPT.read_text())
    temp_file = tempfile.NamedTemporaryFile(mode="w+t", delete=False)
    stdout_file = tempfile.NamedTemporaryFile(mode="w+t", delete=False)
    print(f"Capturing trace with bpftrace script {BPFTRACE_SCRIPT} and MMTk binary {mmtk_bin}")
    content = template.safe_substitute(HARNESS=int(1), MMTK=mmtk_bin, TMP_FILE=temp_file.name)
    # if args.print_script:
    #     print(content)
    temp_file.write(content)
    temp_file.flush()
    process = subprocess.Popen(["sudo", BPFTRACE_BIN, "-f", "json", "--unsafe", temp_file.name], stdout=stdout_file, stderr=stdout_file, stdin=subprocess.DEVNULL)
    return BPFTraceDaemon(process, Path(temp_file.name), Path(stdout_file.name))


RE_TYPE_ID = re.compile(r"\d+")
UNKNOWN_TYPE = "(unknown)"


class LogProcessor:
    def __init__(self):
        self.type_id_name = {}
        self.results = []
        self.start_time = None
        self.tid_current_work_packet = {}

    def process_mmtk_event_gc(self, tid: str, ts: float, values: list[str | int]):
        be = "B" if values[0] == 0 else "E"
        result = {
            "name": "GC",
            "ph": be,
            # Put GC start/stop events in a virtual thread with tid=0
            "tid": 0,
            "ts": ts,
        }
        self.results.append(result)

    def process_mmtk_event_work(self, tid: str, ts: float, values: list[str | int]):
        be = "B" if values[0] == 0 else "E"
        work_id = int(values[1])
        result = {
            "name": "WORK",
            "ph": be,
            "tid": tid,
            "ts": ts,
            "args": {"type_id": int(work_id)},
        }
        match be:
            case "B":
                self.set_current_work_packet(tid, result)
            case "E":
                self.clear_current_work_packet(tid, result)
        self.results.append(result)

    def process_variable(self, line: str):
        data = json.loads(line)["data"]
        key = list(data.items())[0][0]
        if key == "@type_name":
            for k, v in data[key].items():
                self.type_id_name[int(k)] = v
        if not key.startswith("@mmtk_event_"):
            return
        for k, v in data[key].items():
            tid = k.split(",")[0]
            ts = int(k.split(",")[1])
            ts = ts / 1000.0  # https://github.com/google/perfetto/issues/274
            match key:
                case "@mmtk_event_gc":
                    self.process_mmtk_event_gc(tid, ts, v)
                case "@mmtk_event_work":
                    self.process_mmtk_event_work(tid, ts, v)

    def set_current_work_packet(self, tid, result):
        self.tid_current_work_packet[tid] = result

    def get_current_work_packet(self, tid):
        return self.tid_current_work_packet[tid]

    def clear_current_work_packet(self, tid, result):
        self.tid_current_work_packet[tid] = None

    def resolve_results(self):
        # get start time
        min_time = None
        for result in self.results:
            if min_time is None or result["ts"] < min_time:
                min_time = result["ts"]
        # adjust time
        for result in self.results:
            result["ts"] -= min_time
        for result in self.results:
            if result["name"] == "WORK":
                type_id = result["args"]["type_id"]
                type_name = self.type_id_name.get(type_id, "???")
                if type_name == UNKNOWN_TYPE:
                    type_name = f"(unknown:{type_id})"
                result["name"] = type_name

    def output(self, outfile):
        json.dump(
            {
                "traceEvents": self.results,
            },
            outfile,
        )

    def upload_trace(self, file: Path) -> str | None:
        url = "https://perfetto.wenyu.me/api/trace?scope=mmtk"
        print(f"Uploading trace file {file} ...")

        result = subprocess.run(["cloudflared", "access", "curl", url, "-F", f"file=@{file}"], stdout=subprocess.PIPE, universal_newlines=True, check=True)

        if result.returncode == 0:
            data = json.loads(result.stdout)
            url = data["url"]
            return url
        else:
            print("Failed to upload trace file to perfetto.wenyu.me")

    @staticmethod
    def process(content: str, out: Path) -> str | None:
        processor = LogProcessor()
        for line in content.splitlines():
            if not line.startswith('{"type": "map", "data": {'):
                continue
            processor.process_variable(line.strip())
        processor.resolve_results()
        with gzip.open(out, "wt") as f:
            processor.output(f)
        print(f"Trace captured to {out}")
        return processor.upload_trace(out)
