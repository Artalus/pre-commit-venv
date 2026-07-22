#!/usr/bin/env python

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CFG_NAME = ".pre-commit-venv"


def main() -> int:
    script_name, *script_args = sys.argv
    if not script_args:
        log(f"USAGE: {script_name} <CMD> ...")
        sys.exit(1)

    config = Config.load()
    if isinstance(config, Exception):
        log(f"ERROR: pre-commit-venv could not load config: {config}")
        return 1

    command = script_args[:]
    command[0] = str(config.bin_dir / command[0])

    log("Will run:")
    log(f"Command: {command}")
    log(f"CWD: {os.getcwd()}\n\n")
    retcode = subprocess.call(command)
    return retcode


def log(*a: Any, **kw: Any) -> None:
    print("PCVW : ", *a, **kw, file=sys.stderr)


@dataclass
class Config:
    bin_dir: Path

    @staticmethod
    def load() -> "Config | Exception":
        cfg = Path(CFG_NAME).absolute()
        if not cfg.is_file():
            return RuntimeError(f"file `{cfg}` does not exist")

        txt = cfg.read_text().strip()
        if not txt:
            return RuntimeError(f"file `{cfg}` is empty")

        venv = Path(txt).absolute()
        if not venv.is_dir():
            return RuntimeError(f"virtualenv path `{venv}` from `{cfg}` is not a directory")

        bin_dir = venv / ("Scripts" if sys.platform == "win32" else "bin")
        return Config(bin_dir=bin_dir)


if __name__ == "__main__":
    sys.exit(main())
