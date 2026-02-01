#!/usr/bin/env python3

import argparse
import json
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional
from datetime import datetime

import yaml

### usage: # 2023 mt
# python sample_database/submit_crownrun_per_sample.py \
#   --analysis tau \
#   --config config_fullsyst \
#   --production-tag NanoV14_2023signal_all_Version13_syst_mt \
#   --sample-list sample_database/Htautau_input_list/NanoV12_2023signal_all.txt \
#   --scopes '["mt"]' \
#   --files-per-task 1 \
#   --check-status \
#   --min-complete-percent 80 \
#   --retry-incomplete \
#   --max-retries 10 \
#   --log-dir KingMaker_logs/submit_crownrun_per_sample



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


def update_luigi_config(config_path: Path, scopes_str: str, files_per_task: int) -> None:
    """更新 luigi 配置文件，设置 scopes、shifts 和 files_per_task"""
    try:
        scopes_list = json.loads(scopes_str)
    except json.JSONDecodeError:
        print(f"[warn] 无法解析 scopes: {scopes_str}，使用原始值", file=sys.stderr)
        scopes_list = scopes_str
    
    replacements = {
        'shifts': '["All"]',
        'scopes': str(scopes_list).replace("'", '"'),
        'files_per_task': str(files_per_task)
    }
    
    if not config_path.exists():
        print(f"[error] luigi config 不存在: {config_path}", file=sys.stderr)
        return
    
    for key, value in replacements.items():
        cmd = f"sed -i '/^{key} = /c\\{key} = {value}' {config_path}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[warn] 更新 {key} 失败: {result.stderr}", file=sys.stderr)
    
    print(f"[config] 已更新 {config_path}: shifts=[\"All\"], scopes={replacements['scopes']}, files_per_task={files_per_task}")


def get_incomplete_samples(
    analysis: str,
    config: str,
    sample_list: Path,
    production_tag: str,
    log_dir: Optional[Path] = None,
    min_complete_percent: float = 80.0,
) -> list[str]:
    """运行 ProductionStatus.py 并返回未完成的样本列表"""
    cmd = [
        "python3",
        "scripts/ProductionStatus.py",
        "--analysis", analysis,
        "--config", config,
        "--sample-list", str(sample_list),
        "--production-tag", production_tag
    ]
    
    print(f"[check] 检查作业状态: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        print("[warn] ProductionStatus 超时，将提交所有样本", file=sys.stderr)
        return []
    except Exception as e:
        print(f"[warn] ProductionStatus 运行失败: {e}，将提交所有样本", file=sys.stderr)
        return []
    
    # 保存 ProductionStatus 输出
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        status_log = log_dir / f"ProductionStatus_{production_tag}_{ts}.log"
        status_log.write_text(output, encoding="utf-8")
        print(f"[check] ProductionStatus 输出已保存: {status_log}")

    # 解析表格输出找到未完成的样本（Percent != 100%）
    incomplete = []
    in_table = False
    
    for line in output.splitlines():
        # 检测表格内容行（包含 │ 且不是表头分隔符）
        if '│' in line and '┃' not in line and '━' not in line and 'Sample' not in line:
            parts = [p.strip() for p in line.split('│')]
            
            # 表格格式: │ Sample │ Done │ Total │ Percent │
            # parts[0] 为空, parts[1] 为 Sample, parts[2] 为 Done, parts[3] 为 Total, parts[4] 为 Percent
            if len(parts) >= 5:
                sample_name = parts[1].strip()
                percent_str = parts[4].strip()
                
                # 检查是否未完成（Percent != 100%）
                if sample_name and percent_str:
                    if sample_name.strip().lower() == "total":
                        continue
                    in_table = True
                    # 提取百分比数字
                    match = re.search(r'(\d+(?:\.\d+)?)\s*%', percent_str)
                    if match:
                        percent = float(match.group(1))
                        if percent < min_complete_percent:
                            incomplete.append(sample_name)
                            print(f"[check] 未完成: {sample_name} ({percent_str})")
    
    if incomplete:
        print(f"[check] 共发现 {len(incomplete)} 个未完成样本")
    else:
        if in_table:
            print("[check] 所有样本已完成")
        else:
            print("[check] 未能解析状态表格，将提交所有样本")
    
    return incomplete


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


def sanitize_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value)


def get_scope_tag(scopes_str: str) -> str:
    try:
        scopes_list = json.loads(scopes_str)
        if isinstance(scopes_list, list) and scopes_list:
            return sanitize_filename(scopes_list[0])
    except json.JSONDecodeError:
        pass
    return sanitize_filename(scopes_str)


def run_commands(
    commands: list[list[str]],
    dry_run: bool,
    keep_going: bool,
    log_dir: Optional[Path] = None,
) -> int:
    return_code = 0
    
    if dry_run:
        for command in commands:
            printable = " ".join(shlex.quote(token) for token in command)
            print(f"[submit] {printable}", flush=True)
        return 0
    
    # 最多10个并发作业
    max_concurrent = 200
    active_processes: list[tuple[subprocess.Popen, list[str], Optional[Path], Optional[Path]]] = []
    command_queue = commands.copy()
    
    while command_queue or active_processes:
        # 启动新进程直到达到并发限制
        while len(active_processes) < max_concurrent and command_queue:
            command = command_queue.pop(0)
            printable = " ".join(shlex.quote(token) for token in command)
            print(f"[submit] {printable}", flush=True)
            stdout_path = None
            stderr_path = None
            if log_dir is not None:
                log_dir.mkdir(parents=True, exist_ok=True)
                try:
                    nick_index = command.index("--nick") + 1
                    nick = command[nick_index]
                except ValueError:
                    nick = "unknown"
                safe_nick = sanitize_filename(nick)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                stdout_path = log_dir / f"lawrun_{safe_nick}_{ts}.out"
                stderr_path = log_dir / f"lawrun_{safe_nick}_{ts}.err"
                stdout_handle = stdout_path.open("w", encoding="utf-8")
                stderr_handle = stderr_path.open("w", encoding="utf-8")
                proc = subprocess.Popen(command, stdout=stdout_handle, stderr=stderr_handle)
            else:
                proc = subprocess.Popen(command)
            active_processes.append((proc, command, stdout_path, stderr_path))
            time.sleep(2)  # 等待2秒再启动下一个
        
        # 检查完成的进程
        for proc, command, stdout_path, stderr_path in active_processes[:]:
            retcode = proc.poll()
            if retcode is not None:
                active_processes.remove((proc, command, stdout_path, stderr_path))
                if retcode != 0:
                    printable = " ".join(shlex.quote(token) for token in command)
                    print(f"[submit] command failed with exit code {retcode}: {printable}", 
                          file=sys.stderr, flush=True)
                    if stdout_path or stderr_path:
                        print(
                            f"[submit] 日志: stdout={stdout_path}, stderr={stderr_path}",
                            file=sys.stderr,
                            flush=True,
                        )
                    return_code = retcode
                    if not keep_going:
                        # 终止所有活动进程
                        for p, *_ in active_processes:
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
        "--check-status",
        action="store_true",
        help="Check production status and only submit incomplete samples",
    )
    parser.add_argument(
        "--luigi-config",
        default="lawluigi_configs/KingMaker_lxplus_luigi.cfg",
        type=Path,
        help="Path to luigi config file to update before checking status",
    )
    parser.add_argument(
        "--log-dir",
        default="KingMaker_logs/submit_crownrun_per_sample",
        type=Path,
        help="Directory to store ProductionStatus and law run logs",
    )
    parser.add_argument(
        "--min-complete-percent",
        type=float,
        default=80.0,
        help="Skip submission for samples with completion percent >= this value",
    )
    parser.add_argument(
        "--retry-incomplete",
        action="store_true",
        help="After all jobs finish, recheck status and resubmit incomplete samples until all complete",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=10,
        help="Maximum number of retry iterations when using --retry-incomplete",
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

    scope_tag = get_scope_tag(args.scopes)
    resolved_log_dir = args.log_dir.resolve() / scope_tag

    # 如果需要检查状态，先更新 luigi config 再运行 ProductionStatus
    if args.check_status:
        luigi_config = args.luigi_config.resolve()
        update_luigi_config(luigi_config, args.scopes, args.files_per_task)
        
        incomplete_samples = get_incomplete_samples(
            args.analysis,
            args.config,
            sample_list,
            args.production_tag,
            resolved_log_dir,
            args.min_complete_percent,
        )
        
        if incomplete_samples:
            # 过滤：只保留未完成的样本
            samples = [s for s in samples if s in incomplete_samples]
            if not samples:
                print("[info] 所有样本已完成，无需提交")
                return 0
            print(f"[info] 将提交 {len(samples)} 个未完成样本")
        else:
            print("[info] 状态检查失败或全部完成，将提交所有样本")

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

    # 首次提交
    return_code = run_commands(commands, args.dry_run, args.keep_going, resolved_log_dir)
    
    # 如果启用重试且不是 dry-run，循环检查并重新提交未完成的作业
    if args.retry_incomplete and not args.dry_run and args.check_status:
        retry_count = 0
        while retry_count < args.max_retries:
            retry_count += 1
            print(f"\n[retry] 第 {retry_count} 次重新检查状态...")
            
            # 重新检查状态
            incomplete_samples = get_incomplete_samples(
                args.analysis,
                args.config,
                sample_list,
                args.production_tag,
                resolved_log_dir,
                args.min_complete_percent,
            )
            
            if not incomplete_samples:
                print("[retry] 所有样本已完成！")
                break
            
            # 过滤出仍在原始 sample_list 中且未完成的样本
            original_samples = load_sample_list(sample_list)
            samples_to_retry = [s for s in original_samples if s in incomplete_samples]
            
            if not samples_to_retry:
                print("[retry] 没有需要重新提交的样本")
                break
            
            print(f"[retry] 将重新提交 {len(samples_to_retry)} 个未完成样本")
            
            # 构建重新提交的命令
            retry_commands: list[list[str]] = []
            for nick in samples_to_retry:
                sample_meta = datasets.get(nick)
                if sample_meta is None:
                    print(f"[warn] metadata missing for {nick}", file=sys.stderr)
                    continue
                retry_commands.append(build_command(nick, sample_meta, args))
            
            if not retry_commands:
                print("[retry] 没有有效命令可提交")
                break
            
            # 提交重试命令
            retry_return_code = run_commands(retry_commands, args.dry_run, args.keep_going, resolved_log_dir)
            if retry_return_code != 0 and not args.keep_going:
                return_code = retry_return_code
                break
        
        if retry_count >= args.max_retries:
            print(f"[retry] 达到最大重试次数 {args.max_retries}，停止重试")
    
    return return_code


if __name__ == "__main__":
    sys.exit(main())
