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

def detect_php():
    result = subprocess.run(
        "find /run/php -name 'php*-fpm.sock' 2>/dev/null | head -n 1",
        shell=True,
        capture_output=True,
        text=True
    )

    socket = result.stdout.strip()

    if socket:
        return socket

    return None

def create_nginx_config(domain, site_path, php_socket=None):
    config_path = f"/etc/nginx/sites-available/{domain}"

    if os.path.isdir(os.path.join(site_path, "public")):
        web_root = os.path.join(site_path, "public")
    else:
        web_root = site_path

    config = f"""
server {{
    listen 80;
    listen [::]:80;

    server_name {domain} www.{domain};

    root {web_root};
    index index.php index.html index.htm;

    location / {{
        try_files $uri $uri/ /index.php?$query_string;
    }}
"""

    if php_socket:
        config += f"""
    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:{php_socket};
    }}
"""

    config += """
    location ~ /\\.ht {{
        deny all;
    }
}
"""

    with open(config_path, "w") as file:
        file.write(config)

    print(f"✅ Nginx config created: {config_path}")

def enable_site(domain):
    available = f"/etc/nginx/sites-available/{domain}"
    enabled = f"/etc/nginx/sites-enabled/{domain}"

    if os.path.exists(enabled):
        os.remove(enabled)

    os.symlink(available, enabled)

    default_config = "/etc/nginx/sites-enabled/default"

    if os.path.exists(default_config):
        os.remove(default_config)

    run("nginx -t")
    run("systemctl enable nginx")
    run("systemctl restart nginx")

def set_permissions(site_path):
    print("\n🔐 Setting permissions...")

    run(f"chown -R www-data:www-data '{site_path}'")

    storage = os.path.join(site_path, "storage")
    cache = os.path.join(site_path, "bootstrap/cache")

    if os.path.isdir(storage):
        run(f"chmod -R 775 '{storage}'")

    if os.path.isdir(cache):
        run(f"chmod -R 775 '{cache}'")

def configure_ssl(domain):
    print("\n🔒 Configuring SSL...")

    run(
        f"certbot --nginx "
        f"-d {domain} "
        f"-d www.{domain} "
        f"--non-interactive "
        f"--agree-tos "
        f"--register-unsafely-without-email "
        f"--redirect"
    )
