# Contributing to Marathon Trainer

Thanks for wanting to help. Marathon Trainer is a community-driven Windows desktop trainer for the Marathon franchise (Bungie / Marathon Trilogy + Marathon 2026). This document covers the basics.

## Ground rules

- **Single-player / offline only.** Features that affect PvP or online sessions will be rejected.
- **Reversible.** Every memory write must be documented in `src/processors/` with the offset, expected type, and rollback value.
- **No obfuscated loaders.** Keep the code readable — this is an educational / modding repo, not a cracked binary.

## Development setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.main --config configs/default.yaml --dry-run
```

Always test with `--dry-run` first — it will attach the process, resolve signatures, and log every planned write without touching memory.

## Pull requests

1. Fork, branch from `main`, name your branch `feat/<short-desc>` or `fix/<short-desc>`.
2. Add a test under `tests/` for anything in `src/processors/` or `src/drivers/`.
3. Keep commits scoped. One feature per PR.
4. Update `configs/default.yaml` if you add tunables.

## Style

- `ruff` + `black` defaults.
- Type hints on public functions.
- Logging via `rich.console`, never `print()`.

## Reporting bugs

Open an issue with: game build id, trainer version, config used, and the `logs/session-*.log` tail. Redact your Windows username in paths.