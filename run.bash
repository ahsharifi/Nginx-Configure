#!/bin/bash

set -e

# ==========================================
# Colors
# ==========================================

RESET='\033[0m'

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'

BOLD='\033[1m'


# ==========================================
# Functions
# ==========================================

info() {
    echo -e "${CYAN}[INFO]${RESET} $1"
}

success() {
    echo -e "${GREEN}[✓]${RESET} $1"
}

warning() {
    echo -e "${YELLOW}[!]${RESET} $1"
}

error() {
    echo -e "${RED}[✗]${RESET} $1"
}

step() {
    echo ""
    echo -e "${MAGENTA}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${WHITE}${BOLD}$1${RESET}"
    echo -e "${MAGENTA}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
}


# ==========================================
# Root Check
# ==========================================

if [ "$EUID" -ne 0 ]; then

    error "This script must be run as root."

    echo ""
    echo -e "${YELLOW}Example:${RESET}"
    echo -e "  ${CYAN}sudo bash deploy.sh${RESET}"

    exit 1
fi


# ==========================================
# Banner
# ==========================================

clear

echo ""
echo -e "${CYAN}${BOLD}"
echo "╔══════════════════════════════════════════╗"
echo "║                                          ║"
echo "║         NGINX WEBSITE DEPLOYMENT         ║"
echo "║                                          ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${RESET}"


# ==========================================
# Get Information
# ==========================================

step "1. Website Configuration"

read -p "$(echo -e "${CYAN}🌐 Domain:${RESET} ")" DOMAIN

read -p "$(echo -e "${CYAN}📁 Site folder:${RESET} ")" SITE_PATH


if [ -z "$DOMAIN" ]; then
    error "Domain is required."
    exit 1
fi


if [ ! -d "$SITE_PATH" ]; then
    error "Folder does not exist: $SITE_PATH"
    exit 1
fi


SITE_PATH=$(realpath "$SITE_PATH")


echo ""
echo -e "${WHITE}${BOLD}Configuration:${RESET}"
echo -e "  ${CYAN}Domain:${RESET} $DOMAIN"
echo -e "  ${CYAN}Path:${RESET}   $SITE_PATH"


echo ""

read -p "$(echo -e "${YELLOW}Continue? [y/N]:${RESET} ")" CONFIRM


if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    warning "Deployment cancelled."
    exit 0
fi


# ==========================================
# Update
# ==========================================

step "2. Updating System"

info "Updating package list..."

apt update

success "Package list updated."


# ==========================================
# Install
# ==========================================

step "3. Installing Requirements"

info "Installing Nginx..."
apt install -y nginx

success "Nginx installed."

info "Installing Certbot..."
apt install -y certbot python3-certbot-nginx

success "Certbot installed."


# ==========================================
# PHP Detection
# ==========================================

step "4. Detecting PHP-FPM"

PHP_SOCKET=$(find /run/php -name "php*-fpm.sock" 2>/dev/null | head -n 1 || true)


if [ -n "$PHP_SOCKET" ]; then

    success "PHP-FPM detected."

    echo -e "  ${CYAN}Socket:${RESET} $PHP_SOCKET"

else

    warning "PHP-FPM was not detected."

fi


# ==========================================
# Detect Laravel
# ==========================================

step "5. Detecting Project Type"


if [ -d "$SITE_PATH/public" ] && [ -f "$SITE_PATH/artisan" ]; then

    WEB_ROOT="$SITE_PATH/public"

    success "Laravel project detected."

    echo -e "  ${CYAN}Web Root:${RESET} $WEB_ROOT"

else

    WEB_ROOT="$SITE_PATH"

    info "Standard website detected."

    echo -e "  ${CYAN}Web Root:${RESET} $WEB_ROOT"

fi


# ==========================================
# Permissions
# ==========================================

step "6. Configuring Permissions"

info "Changing ownership..."

chown -R www-data:www-data "$SITE_PATH"


if [ -d "$SITE_PATH/storage" ]; then
    chmod -R 775 "$SITE_PATH/storage"
fi


if [ -d "$SITE_PATH/bootstrap/cache" ]; then
    chmod -R 775 "$SITE_PATH/bootstrap/cache"
fi


success "Permissions configured."


# ==========================================
# Nginx Config
# ==========================================

step "7. Creating Nginx Configuration"

CONFIG_FILE="/etc/nginx/sites-available/$DOMAIN"


cat > "$CONFIG_FILE" <<EOF
server {
    listen 80;
    listen [::]:80;

    server_name $DOMAIN www.$DOMAIN;

    root $WEB_ROOT;

    index index.php index.html index.htm;

    location / {
        try_files \$uri \$uri/ /index.php?\$query_string;
    }
EOF


if [ -n "$PHP_SOCKET" ]; then

cat >> "$CONFIG_FILE" <<EOF

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:$PHP_SOCKET;
    }
EOF

fi


cat >> "$CONFIG_FILE" <<EOF

    location ~ /\.ht {
        deny all;
    }
}
EOF


success "Nginx configuration created."

echo -e "  ${CYAN}Config:${RESET} $CONFIG_FILE"


# ==========================================
# Enable Site
# ==========================================

step "8. Enabling Website"

ln -sf \
    "/etc/nginx/sites-available/$DOMAIN" \
    "/etc/nginx/sites-enabled/$DOMAIN"


if [ -f "/etc/nginx/sites-enabled/default" ]; then
    rm -f "/etc/nginx/sites-enabled/default"
fi


success "Website enabled."


# ==========================================
# Nginx Test
# ==========================================

step "9. Testing Nginx"

if nginx -t; then
    success "Nginx configuration is valid."
else
    error "Nginx configuration is invalid."
    exit 1
fi


# ==========================================
# Start Nginx
# ==========================================

step "10. Starting Nginx"

systemctl enable nginx
systemctl restart nginx

success "Nginx is running."


# ==========================================
# SSL
# ==========================================

step "11. SSL Configuration"

read -p "$(echo -e "${CYAN}🔒 Enable HTTPS with Let's Encrypt? [Y/n]:${RESET} ")" SSL


if [[ "$SSL" != "n" && "$SSL" != "N" ]]; then

    info "Requesting SSL certificate..."

    certbot --nginx \
        -d "$DOMAIN" \
        -d "www.$DOMAIN" \
        --non-interactive \
        --agree-tos \
        --register-unsafely-without-email \
        --redirect

    success "SSL configured."

else

    warning "SSL skipped."

fi


# ==========================================
# Final
# ==========================================

step "12. Finalizing"

nginx -t

systemctl reload nginx

success "Nginx reloaded."


# ==========================================
# Success Banner
# ==========================================

echo ""

echo -e "${GREEN}${BOLD}"
echo "╔══════════════════════════════════════════╗"
echo "║                                          ║"
echo "║        ✓ DEPLOYMENT COMPLETED           ║"
echo "║                                          ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${RESET}"

echo ""
echo -e "${CYAN}${BOLD}🌐 Website:${RESET}"
echo -e "   ${GREEN}http://$DOMAIN${RESET}"

if [[ "$SSL" != "n" && "$SSL" != "N" ]]; then
    echo ""
    echo -e "${CYAN}${BOLD}🔒 HTTPS:${RESET}"
    echo -e "   ${GREEN}https://$DOMAIN${RESET}"
fi

echo ""
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${GREEN}${BOLD}        Deployment finished! 🚀${RESET}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""