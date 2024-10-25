#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from string import Template
import subprocess, re, json, gzip
import tempfile
from datetime import datetime


def get_args():
    parser = ArgumentParser(
        description="""
This script is the first part of GC visualization.  It captures a trace,
recording the start and end of every GC and every work packet.
""",
        epilog="""
This script should be invoked as a normal user, but it will ask the user for
root password because it will use `sudo` to run `bpftrace`.  The user should
redirect the standard output to a log file so that the log file can be post-
processed by the `./visualize.py` script.
""",
    )

    parser.add_argument("-b", "--bpftrace", type=str, default="./bpftrace", help="Path of the bpftrace executable")
    parser.add_argument("-m", "--mmtk", type=str, default="openjdk/build/linux-x86_64-normal-server-release/jdk/lib/server/libmmtk_openjdk.so", help="Path of the MMTk binary")
    parser.add_argument("-H", "--harness", action="store_true", help="Only collect data for the timing iteration (harness_begin/harness_end)")
    parser.add_argument("-p", "--print-script", action="store_true", help="Print the content of the bpftrace script")
    parser.add_argument("-e", "--every", metavar="N", type=int, default=1, help="Only capture every N-th GC")
    return parser.parse_args()


def main():
    args = get_args()
    here = Path(__file__).parent.resolve()
    bpftrace_script = here / "wp.bt"
    mmtk_bin = Path(args.mmtk)
    now = datetime.now()

    if not mmtk_bin.exists():
        raise RuntimeError(f"MMTk binary {str(mmtk_bin)} not found.")

    template = Template(bpftrace_script.read_text())
    with tempfile.NamedTemporaryFile(mode="w+t") as tmp:
        print(f"Capturing trace with bpftrace script {bpftrace_script} and MMTk binary {mmtk_bin}")
        content = template.safe_substitute(HARNESS=int(args.harness), MMTK=mmtk_bin, TMP_FILE=tmp.name)
        if args.print_script:
            print(content)
        tmp.write(content)
        tmp.flush()
        # We use execvp to replace the current process instead of creating
        # a subprocess (or sh -c). This is so that when users invoke this from
        # the command line, Ctrl-C will be captured by bpftrace instead of the
        # outer Python script. The temporary file can then be cleaned up by
        # the END probe in bpftrace.
        #
        # In theory, you can implement this via pty, but it is very finicky
        # and doesn't work reliably.
        # See also https://github.com/anupli/running-ng/commit/b74e3a13f56dd97f73432d8a391e1d6cd9db8663
        # os.execvp("sudo", ["sudo", args.bpftrace, "--unsafe", tmp.name])
        result = subprocess.run(["sudo", args.bpftrace, "-f", "json", "--unsafe", tmp.name], stdout=subprocess.PIPE, check=True)
        stdout = result.stdout.decode("utf-8")
        print(stdout)
        time_str = now.strftime("%Y-%m-%d-%H%M%S")
        LogProcessor.process(stdout, Path(f"{time_str}.json.gz"))
        print(f"Trace captured to {time_str}.json.gz")


RE_TYPE_ID = re.compile(r"\d+")
UNKNOWN_TYPE = "(unknown)"


class LogProcessor:
    def __init__(self):
        self.type_id_name = {}
        self.results = []
        self.start_time = None
        self.tid_current_work_packet = {}

    def process_variable(self, line: str):
        data = json.loads(line)["data"]
        key = list(data.items())[0][0]
        if key == "@type_name":
            for k, v in data[key].items():
                self.type_id_name[int(k)] = v
        if not key.startswith("@mmtk_event_"):
            return
        for k, v in data[key].items():
            name: str = key[12:]
            be = "B" if v[0] == 0 else "E"
            tid = k.split(",")[0]
            ts = int(k.split(",")[1])
            work_id = v[1]
            result = {
                "name": name.upper(),
                "ph": be,
                "tid": tid,
                # https://github.com/google/perfetto/issues/274
                "ts": ts / 1000.0,
            }
            match key:
                case "@mmtk_event_gc":
                    # Put GC start/stop events in a virtual thread with tid=0
                    result["tid"] = 0
                case "@mmtk_event_work":
                    result["args"] = {"type_id": int(work_id)}
                    match be:
                        case "B":
                            self.set_current_work_packet(tid, result)
                        case "E":
                            self.clear_current_work_packet(tid, result)
            self.results.append(result)

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

    @staticmethod
    def process(content: str, out: Path):
        processor = LogProcessor()
        for line in content.splitlines():
            if not line.startswith('{"type": "map", "data": {'):
                continue
            processor.process_variable(line.strip())
        processor.resolve_results()
        with gzip.open(out, "wt") as f:
            processor.output(f)


if __name__ == "__main__":
    main()
