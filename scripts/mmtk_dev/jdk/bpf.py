#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from string import Template
import subprocess, re, json, gzip
import tempfile
from datetime import datetime
from mmtk_dev.constants import MMTK_DEV, MMTK_OPENJDK, OPENJDK, DACAPO_CHOPIN, PROBES

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

    def finalize(self):
        print("Finalizing trace capture: ", self.__process.stdout)
        returncode = self.__process.wait()
        if returncode != 0:
            print()
        assert returncode == 0, f"bpftrace failed with return code {self.__process.returncode}"
        stdout = self.__stdout_file.read_text()
        time_str = self.__now.strftime("%Y-%m-%d-%H%M%S")
        LogProcessor.process(stdout, Path(f"{time_str}.json.gz"))
        print(f"Trace captured to {time_str}.json.gz")
        # Delete the temporary file
        self.__temp_file.unlink(missing_ok=True)
        self.__stdout_file.unlink(missing_ok=True)


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
    process = subprocess.Popen(["sudo", BPFTRACE_BIN, "--unsafe", temp_file.name], stdout=stdout_file, stderr=stdout_file)
    return BPFTraceDaemon(process, Path(temp_file.name), Path(stdout_file.name))


RE_TYPE_ID = re.compile(r"\d+")
UNKNOWN_TYPE = "(unknown)"


class LogProcessor:
    def __init__(self):
        self.type_id_name = {}
        self.results = []
        self.start_time = None
        self.tid_current_work_packet = {}

    def process_line(self, line):
        if line.startswith("@type_name"):
            self.process_type_line(line)
        elif "," in line:
            self.process_log_line(line)

    def process_type_line(self, line):
        left, right = line.split(":", 1)
        search_result = RE_TYPE_ID.search(left)
        assert search_result is not None, f"Failed to find type ID in line: {line}"
        type_id = int(search_result.group())
        type_name = right.strip()
        if type_name == "":
            # bpftrace sometimes sees empty strings when using the `str` function
            # See the "Known issues" section in README.md
            type_name = UNKNOWN_TYPE
        self.type_id_name[type_id] = type_name

    def process_log_line(self, line):
        parts = line.split(",")
        try:
            name, be, tid, ts = parts[:4]
        except:
            print("Abnormal line: {}".format(line))
            raise
        ts = int(ts)
        rest = parts[4:]

        if not self.start_time:
            self.start_time = ts

        result = {
            "name": name,
            "ph": be,
            "tid": tid,
            # https://github.com/google/perfetto/issues/274
            "ts": (ts - self.start_time) / 1000.0,
        }

        match name:
            case "GC":
                # Put GC start/stop events in a virtual thread with tid=0
                result["tid"] = 0

            case "BUCKET_OPEN":
                result["args"] = {"stage": int(rest[0])}

            case "INST":
                result["args"] = {"val": int(rest[0])}

            case "WORK":
                result["args"] = {"type_id": int(rest[0])}
                match be:
                    case "B":
                        self.set_current_work_packet(tid, result)
                    case "E":
                        self.clear_current_work_packet(tid, result)

            case "process_slots":
                current = self.get_current_work_packet(tid)
                # eBPF may drop events.  Be conservative.
                if current is not None:
                    current["args"]["num_slots"] = int(rest[0])
                    current["args"]["is_roots"] = int(rest[1])

            case "sweep_chunk":
                current = self.get_current_work_packet(tid)
                # eBPF may drop events.  Be conservative.
                if current is not None:
                    current["args"]["allocated_blocks"] = int(rest[0])

        if be != "meta":
            self.results.append(result)

    def set_current_work_packet(self, tid, result):
        self.tid_current_work_packet[tid] = result

    def get_current_work_packet(self, tid):
        return self.tid_current_work_packet[tid]

    def clear_current_work_packet(self, tid, result):
        self.tid_current_work_packet[tid] = None

    def resolve_results(self):
        for result in self.results:
            if result["name"] == "WORK":
                type_id = result["args"]["type_id"]
                type_name = self.type_id_name[type_id]
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

    @staticmethod
    def process(content: str, out: Path):
        processor = LogProcessor()
        for line in content.splitlines():
            processor.process_line(line.strip())
        processor.resolve_results()
        with gzip.open(out, "wt") as f:
            processor.output(f)
