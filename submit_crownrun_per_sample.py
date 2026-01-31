#!/usr/bin/env python3

import argparse
import shlex
import subprocess
import sys
import time
from pathlib import Path

import yaml


def load_datasets(dataset_file: Path) -> dict:
    with dataset_file.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def load_sample_list(sample_list: Path) -> list[str]:
    samples: list[str] = []
    for raw_line in sample_list.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        samples.append(line)
    return samples


def build_command(
    nick: str,
    sample_meta: dict,
    args: argparse.Namespace,
) -> list[str]:
    command = [
        "law",
        "run",
        "CROWNRun",
        "--nick",
        nick,
        "--analysis",
        args.analysis,
        "--config",
        args.config,
        "--production-tag",
        args.production_tag,
        "--scopes",
        args.scopes,
        "--sampletype",
        sample_meta["sample_type"],
        "--era",
        sample_meta["era"],
        "--files-per-task",
        str(args.files_per_task),
        "--no-poll",
        "False",
    ]

    if args.local_scheduler:
        command.append("--local-scheduler")
    else:
        if args.scheduler_host:
            command.extend(["--scheduler-host", args.scheduler_host])
        if args.scheduler_port is not None:
            command.extend(["--scheduler-port", str(args.scheduler_port)])

    if args.version:
        command.extend(["--version", args.version])

    if args.sampletypes:
        command.extend(["--sampletypes", args.sampletypes])
    else:
        command.extend(["--sampletypes", f'["{sample_meta["sample_type"]}"]'])

    if args.eras:
        command.extend(["--eras", args.eras])
    else:
        command.extend(["--eras", f'["{sample_meta["era"]}"]'])

    if args.channel:
        command.extend(["--channel", args.channel])

    if args.systematic:
        command.extend(["--systematic", args.systematic])

    if args.extra_args:
        command.extend(args.extra_args)

    # ensure all tokens are strings so shlex.quote and subprocess.run work
    return [str(t) for t in command]


def run_commands(commands: list[list[str]], dry_run: bool, keep_going: bool) -> int:
    return_code = 0
    
    if dry_run:
        for command in commands:
            printable = " ".join(shlex.quote(token) for token in command)
            print(f"[submit] {printable}", flush=True)
        return 0
    
    # 最多10个并发作业
    max_concurrent = 10
    active_processes: list[tuple[subprocess.Popen, list[str]]] = []
    command_queue = commands.copy()
    
    while command_queue or active_processes:
        # 启动新进程直到达到并发限制
        while len(active_processes) < max_concurrent and command_queue:
            command = command_queue.pop(0)
            printable = " ".join(shlex.quote(token) for token in command)
            print(f"[submit] {printable}", flush=True)
            proc = subprocess.Popen(command)
            active_processes.append((proc, command))
            time.sleep(2)  # 等待2秒再启动下一个
        
        # 检查完成的进程
        for proc, command in active_processes[:]:
            retcode = proc.poll()
            if retcode is not None:
                active_processes.remove((proc, command))
                if retcode != 0:
                    printable = " ".join(shlex.quote(token) for token in command)
                    print(f"[submit] command failed with exit code {retcode}: {printable}", 
                          file=sys.stderr, flush=True)
                    return_code = retcode
                    if not keep_going:
                        # 终止所有活动进程
                        for p, _ in active_processes:
                            p.terminate()
                        return return_code
        
        # 短暂休眠避免忙等待
        if active_processes:
            time.sleep(1)
    
    return return_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit per-sample CROWNRun jobs based on metadata")
    parser.add_argument(
        "--sample-list",
        default="sample_database/Htautau_input_list/NanoV12_2022signal_all.txt",
        type=Path,
        help="File containing one nick per line",
    )
    parser.add_argument(
        "--datasets",
        default="sample_database/datasets_2023.yaml",
        type=Path,
        help="YAML file with metadata keyed by nick",
    )
    parser.add_argument("--analysis", default="tau")
    parser.add_argument("--config", default="config_fullsyst")
    parser.add_argument("--production-tag", required=True)
    parser.add_argument("--scopes", default='["mt"]')
    parser.add_argument("--sampletypes", default=None)
    parser.add_argument("--eras", default=None)
    parser.add_argument("--channel", default=None)
    parser.add_argument("--version", default=None)
    parser.add_argument("--systematic", default=None)
    parser.add_argument("--files-per-task", type=int, default=1)
    parser.add_argument(
        "--local-scheduler",
        action="store_true",
        help="Use a local Luigi scheduler instead of connecting to luigid",
    )
    parser.add_argument(
        "--scheduler-host",
        default=None,
        help="Hostname of the Luigi scheduler when not using --local-scheduler",
    )
    parser.add_argument(
        "--scheduler-port",
        type=int,
        default=None,
        help="Port of the Luigi scheduler when not using --local-scheduler",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Continue submissions even if a command fails",
    )
    parser.add_argument(
        "extra_args",
        nargs=argparse.REMAINDER,
        help="Additional arguments appended verbatim to each law command",
    )

    args = parser.parse_args()

    dataset_file = args.datasets.resolve()
    sample_list = args.sample_list.resolve()

    if not dataset_file.is_file():
        print(f"dataset file not found: {dataset_file}", file=sys.stderr)
        return 1

    if not sample_list.is_file():
        print(f"sample list not found: {sample_list}", file=sys.stderr)
        return 1

    datasets = load_datasets(dataset_file)
    samples = load_sample_list(sample_list)

    if not samples:
        print("no samples to submit", file=sys.stderr)
        return 1

    commands: list[list[str]] = []

    for nick in samples:
        sample_meta = datasets.get(nick)
        if sample_meta is None:
            print(f"[warn] metadata missing for {nick}", file=sys.stderr)
            if not args.keep_going:
                return 1
            continue

        for key in ("era", "sample_type"):
            if key not in sample_meta:
                print(f"[warn] metadata key '{key}' missing for {nick}", file=sys.stderr)
                if not args.keep_going:
                    return 1
                sample_meta.setdefault(key, "")

        commands.append(build_command(nick, sample_meta, args))

    return run_commands(commands, args.dry_run, args.keep_going)


if __name__ == "__main__":
    sys.exit(main())
