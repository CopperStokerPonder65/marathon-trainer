"""Entry point for Marathon Trainer."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console

from src.bootstrap.attacher import attach_to_marathon
from src.bootstrap.config_loader import load_config
from src.core.pipeline import TrainerPipeline
from src.utils.logging import setup_logging

console = Console()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="marathon-trainer")
    parser.add_argument("--config", type=Path, default=Path("configs/default.yaml"))
    parser.add_argument("--dry-run", action="store_true", help="Resolve offsets but do not write")
    parser.add_argument("--no-overlay", action="store_true", help="Disable the overlay driver")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    cfg = load_config(args.config)
    setup_logging(cfg.trainer.log_level)

    console.rule("[bold cyan]Marathon Trainer[/]")
    console.print(f"config: {args.config}  dry_run={args.dry_run}")

    try:
        session = attach_to_marathon(cfg.game.process_name)
    except RuntimeError as exc:
        console.print(f"[red]attach failed:[/] {exc}")
        return 2

    console.print(f"[green]attached[/] pid={session.pid} build={session.build_id}")

    pipeline = TrainerPipeline(session, cfg, dry_run=args.dry_run)
    if args.no_overlay:
        pipeline.disable_driver("overlay")

    try:
        pipeline.run_forever()
    except KeyboardInterrupt:
        console.print("[yellow]interrupted - unloading[/]")
    finally:
        pipeline.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())