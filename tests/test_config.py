from pathlib import Path

import pytest

from src.bootstrap.config_loader import load_config


def test_load_default_config(tmp_path: Path):
    p = tmp_path / "c.yaml"
    p.write_text(
        "game:\n  process_name: Marathon.exe\ntrainer:\n  log_level: DEBUG\n", encoding="utf-8"
    )
    cfg = load_config(p)
    assert cfg.game.process_name == "Marathon.exe"
    assert cfg.trainer.log_level == "DEBUG"


def test_missing_config_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nope.yaml")
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>