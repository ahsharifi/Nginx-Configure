import os
import sys
import subprocess


# ==========================================
# Colors
# ==========================================

RESET = "\033[0m"

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
CYAN = "\033[0;36m"
WHITE = "\033[1;37m"

BOLD = "\033[1m"


# ==========================================
# Output Helpers
# ==========================================

def info(message):
    print(f"{CYAN}[INFO]{RESET} {message}")


def success(message):
    print(f"{GREEN}[✓]{RESET} {message}")


def warning(message):
    print(f"{YELLOW}[!]{RESET} {message}")


def error(message):
    print(f"{RED}[✗]{RESET} {message}")


def step(title):
    print()
    print(f"{MAGENTA}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{WHITE}{BOLD}{title}{RESET}")
    print(f"{MAGENTA}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")


# ==========================================
# Run Command
# ==========================================

def run(command, check=True):
    print(f"\n{BLUE}$ {command}{RESET}")

    result = subprocess.run(
        command,
        shell=True,
        text=True
    )

    if check and result.returncode != 0:
        error("Command failed.")
        sys.exit(1)

    return result


# ==========================================
# Root Check
# ==========================================

def require_root():
    if os.geteuid() != 0:
        error("This script must be run as root.")

        print()
        print(f"{YELLOW}Example:{RESET}")
        print(f"{CYAN}sudo python3 deploy.py{RESET}")

        sys.exit(1)


# ==========================================
# Install Packages
# ==========================================

def install_packages():
    step("2. Installing Required Packages")

    info("Updating package list...")

    run("apt update")

    success("Package list updated.")

    packages = [
        "nginx",
        "curl",
        "certbot",
        "python3-certbot-nginx"
    ]

    info("Installing required packages...")

    run("apt install -y " + " ".join(packages))

    success("Required packages installed.")


# ==========================================
# Detect PHP-FPM
# ==========================================

def detect_php():
    step("3. Detecting PHP-FPM")

    result = subprocess.run(
        "find /run/php -name 'php*-fpm.sock' 2>/dev/null | head -n 1",
        shell=True,
        capture_output=True,
        text=True
    )

    socket = result.stdout.strip()

    if socket:
        success("PHP-FPM detected.")
        print(f"  {CYAN}Socket:{RESET} {socket}")

        return socket

    warning("PHP-FPM not detected.")

    return None


# ==========================================
# Create Nginx Configuration
# ==========================================

def create_nginx_config(domain, site_path, php_socket=None):

    step("5. Creating Nginx Configuration")

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
    location ~ /\\.ht {
        deny all;
    }
}
"""

    with open(config_path, "w") as file:
        file.write(config)

    success("Nginx configuration created.")
    print(f"  {CYAN}Config:{RESET} {config_path}")


# ==========================================
# Enable Site
# ==========================================

def enable_site(domain):

    step("6. Enabling Website")

    available = f"/etc/nginx/sites-available/{domain}"
    enabled = f"/etc/nginx/sites-enabled/{domain}"

    if os.path.exists(enabled):
        os.remove(enabled)

    os.symlink(available, enabled)

    default_config = "/etc/nginx/sites-enabled/default"

    if os.path.exists(default_config):
        os.remove(default_config)

        info("Default Nginx configuration removed.")

    info("Testing Nginx configuration...")

    run("nginx -t")

    success("Nginx configuration is valid.")

    info("Enabling Nginx service...")

    run("systemctl enable nginx")

    info("Restarting Nginx...")

    run("systemctl restart nginx")

    success("Nginx is running.")


# ==========================================
# Set Permissions
# ==========================================

def set_permissions(site_path):

    step("4. Configuring Permissions")

    info("Changing ownership...")

    run(f"chown -R www-data:www-data '{site_path}'")

    storage = os.path.join(site_path, "storage")
    cache = os.path.join(site_path, "bootstrap/cache")

    if os.path.isdir(storage):
        info("Configuring storage permissions...")
        run(f"chmod -R 775 '{storage}'")

    if os.path.isdir(cache):
        info("Configuring bootstrap/cache permissions...")
        run(f"chmod -R 775 '{cache}'")

    success("Permissions configured.")


# ==========================================
# Configure SSL
# ==========================================

def configure_ssl(domain):

    step("8. Configuring SSL")

    info("Requesting Let's Encrypt certificate...")

    run(
        f"certbot --nginx "
        f"-d {domain} "
        f"-d www.{domain} "
        f"--non-interactive "
        f"--agree-tos "
        f"--register-unsafely-without-email "
        f"--redirect"
    )

    success("SSL certificate configured successfully.")


# ==========================================
# Main
# ==========================================

def main():

    require_root()

    print()
    print(f"{CYAN}{BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║                                          ║")
    print("║        NGINX WEBSITE DEPLOYMENT          ║")
    print("║                                          ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{RESET}")

    step("1. Website Configuration")

    domain = input(
        f"{CYAN}🌐 Domain: {RESET}"
    ).strip()

    site_path = input(
        f"{CYAN}📁 Site folder path: {RESET}"
    ).strip()

    if not domain:
        error("Domain is required.")
        sys.exit(1)

    if not os.path.isdir(site_path):
        error(f"Folder does not exist: {site_path}")
        sys.exit(1)

    site_path = os.path.abspath(site_path)

    print()
    print(f"{WHITE}{BOLD}Configuration:{RESET}")
    print(f"  {CYAN}Domain:{RESET} {domain}")
    print(f"  {CYAN}Path:{RESET}   {site_path}")

    confirm = input(
        f"\n{YELLOW}Continue? [y/N]: {RESET}"
    ).strip().lower()

    if confirm != "y":
        warning("Deployment cancelled.")
        return

    # 1. Install requirements
    install_packages()

    # 2. Detect PHP-FPM
    php_socket = detect_php()

    # 3. Permissions
    set_permissions(site_path)

    # 4. Nginx configuration
    create_nginx_config(
        domain,
        site_path,
        php_socket
    )

    # 5. Enable site
    enable_site(domain)

    # 6. SSL
    step("7. SSL Configuration")

    ssl = input(
        f"{CYAN}🔒 Configure SSL with Let's Encrypt? [Y/n]: {RESET}"
    ).strip().lower()

    if ssl != "n":
        configure_ssl(domain)
    else:
        warning("SSL configuration skipped.")

    # 7. Final test
    step("9. Finalizing Deployment")

    info("Running final Nginx configuration test...")

    run("nginx -t")

    info("Reloading Nginx...")

    run("systemctl reload nginx")

    success("Nginx reloaded successfully.")

    # ==========================================
    # Deployment Complete
    # ==========================================

    print()

    print(f"{GREEN}{BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║                                          ║")
    print("║       ✓ DEPLOYMENT COMPLETED             ║")
    print("║                                          ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{RESET}")

    print()
    print(f"{CYAN}{BOLD}🌐 Website:{RESET}")
    print(f"   {GREEN}http://{domain}{RESET}")

    if ssl != "n":
        print()
        print(f"{CYAN}{BOLD}🔒 HTTPS:{RESET}")
        print(f"   {GREEN}https://{domain}{RESET}")

    print()
    print(f"{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{GREEN}{BOLD}        Deployment finished! 🚀{RESET}")
    print(f"{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print()


if __name__ == "__main__":
    main()