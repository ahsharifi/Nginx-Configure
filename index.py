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

def require_root():
    if os.geteuid() != 0:
        print("❌ این اسکریپت باید با root اجرا شود.")
        print("مثال:")
        print("sudo python3 deploy.py")
        sys.exit(1)

def install_packages():
    print("\n📦 Installing required packages...")

    run("apt update")

    packages = [
        "nginx",
        "curl",
        "certbot",
        "python3-certbot-nginx"
    ]

    run("apt install -y " + " ".join(packages))