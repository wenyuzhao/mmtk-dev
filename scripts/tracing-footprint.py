from enum import Enum
import os
from pathlib import Path
from typing import Annotated
import typer
import subprocess


class GC(str, Enum):
    ix = "ix"
    lxr = "lxr"
    g1 = "g1"
    par = "par"
    shen = "shen"
    z = "z"


def find_symbol_pct(output: str, symbol: str, opt: bool = False) -> float:
    pct = 0.0
    found = False
    for line in output.splitlines():
        if line.endswith("[.] " + symbol):
            found = True
            children_pct = float(line.split()[0].removesuffix("%"))
            self_pct = float(line.split()[1].removesuffix("%"))
            pct += self_pct + children_pct
    if not found and not opt:
        print("Failed to find symbol: " + symbol)
        raise typer.Exit(-1)
    return pct


def gen_perf_data(gc: GC, heap: str = "540M", bench: str = "lusearch") -> Path:
    perf_args = ["-g", "-e", "cycles"]
    java_bin = "/home/wenyu/Workspace/mmtk-dev/openjdk/build/linux-x86_64-normal-server-release/jdk/bin/java"
    match gc:
        case GC.ix:
            gc_args = ["-XX:+UseThirdPartyHeap", "-XX:ThirdPartyHeapOptions=plan=Immix"]
        case GC.lxr:
            gc_args = ["-XX:+UseThirdPartyHeap", "-XX:ThirdPartyHeapOptions=plan=LXR"]
        case GC.g1:
            gc_args = ["-XX:+UseG1GC"]
        case GC.par:
            gc_args = ["-XX:+UseParallelGC"]
        case GC.shen:
            gc_args = ["-XX:+UseShenandoahGC"]
        case GC.z:
            gc_args = ["-XX:+UseZGC"]
    java_cmd = [java_bin, "-XX:+PreserveFramePointer", "-XX:+UnlockExperimentalVMOptions", "-XX:+UnlockDiagnosticVMOptions", "-XX:+ExitOnOutOfMemoryError", "-cp", "/usr/share/benchmarks/dacapo/dacapo-23.11-chopin.jar", *gc_args, f"-Xms{heap}", f"-Xmx{heap}", "Harness", "-n", "5", "lusearch"]
    cmd = ["perf", "record", *perf_args, "--", *java_cmd]
    print("RUN " + " ".join(cmd))
    subprocess.check_call(cmd)
    os.system(f"cp perf.data perf-{gc.value}.data")
    return Path(f"perf.data")


def report_one(gc: GC, perf_data: Path | None, run: bool):
    if run:
        if perf_data:
            print("perf_data is ignored when --run is set")
        perf_data = gen_perf_data(gc)
    elif not perf_data:
        perf_data = Path(f"perf-{gc.value}.data")
    if not perf_data.exists():
        print(f"perf data file not found: {perf_data}")
        raise typer.Exit(-1)
    out = subprocess.check_output(["perf", "report", "-i", perf_data, "--stdio", "-g", "none", "--percent-limit", "0.01"], text=True)
    match gc:
        case GC.ix:
            denom = find_symbol_pct(out, "start_worker")
            num = find_symbol_pct(out, "<mmtk::scheduler::gc_work::PlanProcessEdges<VM,P,_> as mmtk::scheduler::gc_work::ProcessEdgesWork>::process_slots")
        case GC.lxr:
            denom = find_symbol_pct(out, "start_worker")
            num = sum(
                [
                    find_symbol_pct(out, "<mmtk::plan::lxr::cm::LXRConcurrentTraceObjects<VM> as mmtk::scheduler::work::GCWork<VM>>::do_work"),
                    find_symbol_pct(out, "<mmtk::plan::lxr::rc::ProcessDecs<VM> as mmtk::scheduler::work::GCWork<VM>>::do_work"),
                    find_symbol_pct(out, "<mmtk::plan::lxr::rc::ProcessIncs<VM,_> as mmtk::scheduler::work::GCWork<VM>>::do_work"),
                    find_symbol_pct(out, "mmtk::scheduler::gc_work::<impl mmtk::scheduler::work::GCWork<<E as mmtk::scheduler::gc_work::ProcessEdgesWork>::VM> for E>::do_work"),
                ]
            )
        case GC.g1:
            denom = find_symbol_pct(out, "GangWorker::loop()")
            num = sum(
                [
                    find_symbol_pct(out, "G1ParEvacuateFollowersClosure::do_void()"),
                    find_symbol_pct(out, "G1CMRemarkTask::work(unsigned int)", opt=True),
                    find_symbol_pct(out, "G1FullGCMarkTask::work(unsigned int)", opt=True),
                ]
            )
            x = find_symbol_pct(out, "G1FullGCAdjustTask::work(unsigned int)", opt=True)
            if x > 0:
                num += x
                num -= find_symbol_pct(out, "G1RootProcessor::process_all_roots(OopClosure*, CLDClosure*, CodeBlobClosure*, bool)")
        case GC.par:
            denom = find_symbol_pct(out, "GCTaskThread::run()")
            num = find_symbol_pct(out, "StealTask::do_it(GCTaskManager*, unsigned int)") + find_symbol_pct(out, "StealMarkingTask::do_it(GCTaskManager*, unsigned int)")
        case GC.shen:
            denom = find_symbol_pct(out, "GangWorker::loop()")
            num = sum(
                [
                    find_symbol_pct(out, "ShenandoahConcurrentMarkingTask::work(unsigned int)"),
                    find_symbol_pct(out, "ShenandoahEvacuationTask::work(unsigned int)"),
                    find_symbol_pct(out, "ShenandoahFinalMarkingTask::work(unsigned int)"),
                    find_symbol_pct(out, "ShenandoahUpdateHeapRefsTask<ShenandoahUpdateHeapRefsClosure>::work(unsigned int)"),
                ]
            )
        case GC.z:
            denom = find_symbol_pct(out, "GangWorker::loop()")
            num = sum(
                [
                    find_symbol_pct(out, "ZMark::work(unsigned long)"),
                    find_symbol_pct(out, "ZRelocateTask::work()"),
                ]
            )
    print(f"{gc.value} tracing footprint: {num/denom:.2%}")
    return num / denom


def main(gc: Annotated[GC | None, typer.Argument()] = None, perf_data: Annotated[Path | None, typer.Argument(help="perf.data file. default to perf-{gc}.data")] = None, run: Annotated[bool, typer.Option("--run", is_flag=True, help="Run DaCapo-lusearch and generate perf.data")] = False, all: Annotated[bool, typer.Option("--all", is_flag=True, help="Report all GCs")] = False):
    if not all:
        if gc is None:
            print("Please specify a GC with --gc or use --all to report all GCs")
            raise typer.Exit(-1)
        report_one(gc, perf_data, run)
    else:
        if perf_data:
            print("perf_data is ignored when --all is set")
        results: dict[GC, float] = {}
        for gc in GC:
            pct = report_one(gc, None, run)
            results[gc] = pct
        print("\n---\n\nSummary:")
        for gc, pct in results.items():
            print(f" - {gc.value}: {pct:.2%}")


if __name__ == "__main__":
    typer.run(main)
