from pathlib import Path
import tempfile
import asyncio
import time
from typing import Annotated
import typer


async def run(i: int):
    with tempfile.TemporaryDirectory(prefix="mmtk-xalan-") as tmpdir:
        cmd = f"uv run mmtk-jdk r --gc LXR -n 5 --heap 30M --bench xalan --no-weak-refs --no-class-unloading --scratch-dir {tmpdir}"
        print(f"    - Running benchmark {i} with command: {cmd}")
        process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            out = stdout.decode() + stderr.decode()
            return (i, out)
        else:
            return (i, None)


def dump_fails(fails: list[tuple[int, str]]) -> str:
    md = f""
    for i, error in fails:
        md += f"## Run {i}\n\n```\n{error}\n```\n\n"
    return md


async def run_batch(start: int, end: int, log: Path):
    tasks = [run(i) for i in range(start, end)]
    results = await asyncio.gather(*tasks)
    fails = [(i, error) for i, error in results if error is not None]
    with log.open("a") as f:
        f.write(dump_fails(fails))
    return fails


async def build_jdk():
    cmd = "uv run mmtk-jdk build"
    print(f"Building JDK with command: {cmd}")
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        out = stdout.decode() + stderr.decode()
        print(f"Build failed with output:\n\n{out}")
        raise Exception("Build failed")
    else:
        print("Build completed successfully.")


async def main(invocations: int, batch_size: int, build: bool):
    if build:
        await build_jdk()

    all_fails = []
    start_time = time.time()
    log = Path("_xalan_failed_runs_temp.md")
    log.write_text("")
    for start in range(0, invocations, batch_size):
        end = min(start + batch_size, invocations)
        print(f"Running batch from {start} to {end - 1}")
        fails = await run_batch(start, end, log)
        elapsed = time.time() - start_time
        if fails:
            all_fails.extend(fails)
            print(f"Batch from {start} to {end - 1} had {len(fails)} failures. Elapsed time: {elapsed:.2f} seconds.")
        else:
            print(f"Batch from {start} to {end - 1} completed successfully with no failures. Elapsed time: {elapsed:.2f} seconds.")

    log = Path("_xalan_failed_runs.md")
    md = f"# Failed Runs: {len(all_fails)} out of {invocations}\n\n"
    md += dump_fails(all_fails)
    log.write_text(md)


def main_cli(
    invocations: Annotated[int, typer.Option("-n", "--invocations")] = 30,
    batch_size: Annotated[int, typer.Option("-b", "--batch-size")] = 5,
    build: bool = True,
):
    asyncio.run(main(invocations, batch_size, build))


if __name__ == "__main__":
    typer.run(main_cli)
