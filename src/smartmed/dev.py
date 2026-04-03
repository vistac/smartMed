import subprocess
import sys


def run_dev():
    cmd = ["watchfiles", "uv run python -m smartmed.app", "."]
    subprocess.run(cmd)
