import os
import sys
import subprocess
from pathlib import Path


def run(command, check=True):
    print(f"\n$ {command}")

    result = subprocess.run(
        command,
        shell=True,
        text=True
    )

    if check and result.returncode != 0:
        print("❌ Command failed")
        sys.exit(1)

    return result
