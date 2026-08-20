# 🚀 Nginx Website Deployment

> Automated Nginx website deployment using Bash and Python.

---

## 🌍 Language / زبان

- 🇬🇧 [English](#-english)
- 🇮🇷 [فارسی](#-فارسی)

---

# 🇬🇧 English

<a name="-english"></a>

## 📌 Overview

This project automates the basic configuration of a website on an Nginx server.

It can:

- Install required packages
- Install Nginx
- Install Certbot
- Detect PHP-FPM
- Detect Laravel projects
- Configure Nginx Virtual Host
- Configure PHP-FPM
- Set website permissions
- Enable the website
- Disable the default Nginx configuration
- Test Nginx configuration
- Restart and reload Nginx
- Configure SSL using Let's Encrypt
- Redirect HTTP to HTTPS

---

## 🖥️ Requirements

The scripts are designed for:

- Ubuntu
- Debian
- Debian-based Linux distributions

You need:

- Root access
- A registered domain
- DNS configured for the server
- A website/project directory

For example:

```text
Domain:
example.com

Project:
 /var/www/example
```

Make sure the domain points to the server IP before requesting SSL.

---

# 📂 Project Structure

```text
.
├── deploy.sh
├── deploy.py
└── README.md
```

- `deploy.sh` → Shell/Bash deployment script
- `deploy.py` → Python deployment script
- `README.md` → Documentation

---

# 🐚 Shell / Bash Version

## 1. Give Execute Permission

```bash
chmod +x deploy.sh
```

## 2. Run the Script

```bash
sudo ./deploy.sh
```

Or:

```bash
sudo bash deploy.sh
```

---

## 3. Enter Domain

The script asks for your domain:

```text
🌐 Domain: example.com
```

Enter your actual domain.

Example:

```text
example.com
```

---

## 4. Enter Website Directory

Next, enter the project directory:

```text
📁 Site folder: /var/www/example
```

For example:

```text
/var/www/example
```

---

## 5. Confirm Deployment

The script displays the configuration:

```text
Configuration:

Domain: example.com
Path:   /var/www/example
```

Then:

```text
Continue? [y/N]:
```

Enter:

```text
y
```

---

## 6. Install Requirements

The script installs:

```text
nginx
curl
certbot
python3-certbot-nginx
```

It also runs:

```bash
apt update
```

---

## 7. Detect PHP-FPM

The script checks for PHP-FPM sockets inside:

```text
/run/php/
```

For example:

```text
/run/php/php8.3-fpm.sock
```

If PHP-FPM exists, Nginx will be configured to communicate with it.

---

## 8. Detect Laravel

If the project contains:

```text
artisan
public/
```

the script considers it a Laravel project.

The Nginx root will then become:

```text
/var/www/example/public
```

instead of:

```text
/var/www/example
```

This is the recommended configuration for Laravel.

---

## 9. Configure Permissions

The project ownership is changed to:

```text
www-data:www-data
```

For Laravel, these directories also receive writable permissions:

```text
storage/
bootstrap/cache/
```

---

## 10. Create Nginx Configuration

The configuration is created at:

```text
/etc/nginx/sites-available/example.com
```

Then a symbolic link is created:

```text
/etc/nginx/sites-enabled/example.com
```

---

## 11. Test Nginx

The script runs:

```bash
nginx -t
```

If the configuration is valid, deployment continues.

---

## 12. Start Nginx

The script enables Nginx at boot:

```bash
systemctl enable nginx
```

and restarts it:

```bash
systemctl restart nginx
```

---

## 13. Configure SSL

The script asks:

```text
🔒 Configure SSL with Let's Encrypt? [Y/n]:
```

Enter:

```text
Y
```

The script uses Certbot to create the SSL certificate.

It also configures HTTP → HTTPS redirection.

Your website will then be available at:

```text
https://example.com
```

---

# 🐍 Python Version

## 1. Run the Script

No special Python package is required.

Run:

```bash
sudo python3 deploy.py
```

---

## 2. Enter Domain

```text
🌐 Domain: example.com
```

---

## 3. Enter Website Directory

```text
📁 Site folder path: /var/www/example
```

---

## 4. Confirm

```text
Continue? [y/N]:
```

Enter:

```text
y
```

---

## 5. Automatic Installation

The Python script automatically installs:

```text
nginx
curl
certbot
python3-certbot-nginx
```

using:

```bash
apt
```

---

## 6. PHP-FPM Detection

The script searches for PHP-FPM sockets:

```text
/run/php/php*-fpm.sock
```

If one is found, it is automatically added to the Nginx configuration.

---

## 7. Laravel Detection

The script checks whether:

```text
artisan
```

and:

```text
public/
```

exist.

If both exist, it assumes the project is Laravel and uses:

```text
project/public
```

as the Nginx web root.

---

## 8. Configure Permissions

The script sets:

```text
www-data:www-data
```

as the project owner.

For Laravel:

```text
storage/
bootstrap/cache/
```

are configured as writable directories.

---

## 9. Configure Nginx

The Nginx configuration is created in:

```text
/etc/nginx/sites-available/
```

and enabled through:

```text
/etc/nginx/sites-enabled/
```

---

## 10. SSL

The script asks:

```text
🔒 Configure SSL with Let's Encrypt? [Y/n]:
```

If enabled, Certbot automatically configures HTTPS.

---

# 🔄 Deployment Flow

Both versions follow approximately the same process:

```text
Start
  │
  ▼
Check Root
  │
  ▼
Get Domain
  │
  ▼
Get Project Path
  │
  ▼
Install Requirements
  │
  ▼
Detect PHP-FPM
  │
  ▼
Detect Laravel
  │
  ▼
Configure Permissions
  │
  ▼
Create Nginx Configuration
  │
  ▼
Enable Website
  │
  ▼
Test Nginx
  │
  ▼
Restart Nginx
  │
  ▼
Configure SSL
  │
  ▼
Reload Nginx
  │
  ▼
Deployment Complete
```

---

# ⚠️ Important Notes

## DNS

Before using Let's Encrypt, make sure your domain points to the server.

For example:

```text
example.com → SERVER_IP
www.example.com → SERVER_IP
```

You can check it with:

```bash
dig example.com
```

or:

```bash
nslookup example.com
```

---

## Firewall

Make sure ports `80` and `443` are open.

For UFW:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

Then:

```bash
sudo ufw status
```

---

## Laravel

For Laravel projects, the recommended structure is:

```text
/var/www/example
├── app/
├── bootstrap/
├── config/
├── database/
├── public/
├── resources/
├── routes/
├── storage/
├── vendor/
├── artisan
└── .env
```

Nginx should point to:

```text
/var/www/example/public
```

not:

```text
/var/www/example
```

---

## 🔒 Security

Do not expose sensitive Laravel files directly through Nginx.

The Laravel `public/` directory is specifically designed to be the web root.

Never configure Nginx to expose the entire Laravel project unless you understand the security implications.

---

# 🛠️ Troubleshooting

## Check Nginx Status

```bash
systemctl status nginx
```

## Check Nginx Configuration

```bash
nginx -t
```

## Restart Nginx

```bash
systemctl restart nginx
```

## Reload Nginx

```bash
systemctl reload nginx
```

## View Nginx Error Logs

```bash
tail -f /var/log/nginx/error.log
```

## View Access Logs

```bash
tail -f /var/log/nginx/access.log
```

---

# 🔐 SSL Troubleshooting

Check Certbot certificates:

```bash
certbot certificates
```

Test automatic renewal:

```bash
certbot renew --dry-run
```

---

# 🇮🇷 فارسی

<a name="-فارسی"></a>

## 📌 معرفی

این پروژه مراحل کانفیگ و Deploy سایت روی Nginx را با استفاده از Bash یا Python به‌صورت خودکار انجام می‌دهد.

### امکانات

دو نسخه دارد:

- `deploy.sh` → نسخه Bash/Shell
- `deploy.py` → نسخه Python

اسکریپت می‌تواند مراحل اصلی زیر را انجام دهد:

- نصب Nginx
- نصب Certbot
- نصب وابستگی‌های موردنیاز
- تشخیص PHP-FPM
- تشخیص پروژه Laravel
- ساخت Virtual Host
- تنظیم PHP-FPM
- تنظیم Permission
- فعال‌سازی سایت
- حذف کانفیگ پیش‌فرض Nginx
- تست کانفیگ Nginx
- Restart و Reload کردن Nginx
- دریافت SSL از Let's Encrypt
- انتقال HTTP به HTTPS

---

# 💻 پیش‌نیازها

سیستم‌عامل پیشنهادی:

- Ubuntu
- Debian
- سایر توزیع‌های مبتنی بر Debian

همچنین نیاز دارید:

- دسترسی Root
- یک Domain
- تنظیم DNS دامنه
- مسیر پروژه روی سرور

مثال:

```text
Domain:
example.com

Project:
 /var/www/example
```

قبل از گرفتن SSL مطمئن شوید دامنه به IP سرور اشاره می‌کند.

---

# 📂 ساختار پروژه

```text
.
├── deploy.sh
├── deploy.py
└── README.md
```

توضیح فایل‌ها:

```text
deploy.sh
```

نسخه Shell/Bash اسکریپت است.

```text
deploy.py
```

نسخه Python اسکریپت است.

```text
README.md
```

مستندات پروژه است.

---

# 🐚 استفاده از نسخه Shell

## 1. دادن Permission اجرا

```bash
chmod +x deploy.sh
```

## 2. اجرای اسکریپت

```bash
sudo ./deploy.sh
```

یا:

```bash
sudo bash deploy.sh
```

---

## 3. وارد کردن دامنه

اسکریپت دامنه را می‌پرسد:

```text
🌐 Domain: example.com
```

دامنه خودتان را وارد کنید.

مثلاً:

```text
example.com
```

---

## 4. وارد کردن مسیر سایت

مسیر پروژه را وارد کنید:

```text
📁 Site folder: /var/www/example
```

مثلاً:

```text
/var/www/example
```

---

## 5. تأیید

اسکریپت اطلاعات را نمایش می‌دهد:

```text
Configuration:

Domain: example.com
Path:   /var/www/example
```

سپس:

```text
Continue? [y/N]:
```

برای ادامه بنویسید:

```text
y
```

---

## 6. نصب پکیج‌ها

اسکریپت پکیج‌های زیر را نصب می‌کند:

```text
nginx
curl
certbot
python3-certbot-nginx
```

و ابتدا:

```bash
apt update
```

را اجرا می‌کند.

---

## 7. تشخیص PHP-FPM

اسکریپت مسیر زیر را بررسی می‌کند:

```text
/run/php/
```

مثلاً:

```text
/run/php/php8.3-fpm.sock
```

اگر PHP-FPM پیدا شود، مسیر Socket آن در کانفیگ Nginx قرار می‌گیرد.

---

## 8. تشخیص Laravel

اگر این دو مورد وجود داشته باشند:

```text
artisan
public/
```

اسکریپت پروژه را Laravel تشخیص می‌دهد.

در این حالت Web Root می‌شود:

```text
/var/www/example/public
```

که برای Laravel روش صحیح‌تری است.

---

## 9. تنظیم Permission

مالک پروژه روی:

```text
www-data:www-data
```

قرار می‌گیرد.

در پروژه‌های Laravel نیز این دو مسیر قابل نوشتن می‌شوند:

```text
storage/
bootstrap/cache/
```

---

## 10. ساخت کانفیگ Nginx

کانفیگ سایت در این مسیر ساخته می‌شود:

```text
/etc/nginx/sites-available/example.com
```

سپس سایت با Symlink فعال می‌شود:

```text
/etc/nginx/sites-enabled/example.com
```

---

## 11. تست Nginx

اسکریپت اجرا می‌کند:

```bash
nginx -t
```

اگر کانفیگ صحیح باشد، ادامه می‌دهد.

---

## 12. اجرای Nginx

Nginx با این دستور فعال می‌شود:

```bash
systemctl enable nginx
```

و سپس Restart می‌شود:

```bash
systemctl restart nginx
```

---

## 13. فعال‌سازی SSL

اسکریپت می‌پرسد:

```text
🔒 Configure SSL with Let's Encrypt? [Y/n]:
```

اگر:

```text
Y
```

وارد کنید، Certbot SSL را تنظیم می‌کند.

همچنین HTTP به HTTPS Redirect می‌شود.

در نهایت سایت از طریق:

```text
https://example.com
```

قابل دسترسی خواهد بود.

---

# 🐍 استفاده از نسخه Python

## 1. اجرای اسکریپت

نیازی به نصب کتابخانه Python اضافی نیست.

اجرا:

```bash
sudo python3 deploy.py
```

---

## 2. وارد کردن Domain

```text
🌐 Domain: example.com
```

---

## 3. وارد کردن مسیر پروژه

```text
📁 Site folder path: /var/www/example
```

---

## 4. تأیید

```text
Continue? [y/N]:
```

برای ادامه:

```text
y
```

---

## 5. نصب خودکار نیازمندی‌ها

نسخه Python به‌صورت خودکار این موارد را نصب می‌کند:

```text
nginx
curl
certbot
python3-certbot-nginx
```

---

## 6. تشخیص PHP-FPM

اسکریپت فایل‌های زیر را بررسی می‌کند:

```text
/run/php/php*-fpm.sock
```

در صورت پیدا شدن، Socket مربوطه در کانفیگ Nginx قرار می‌گیرد.

---

## 7. تشخیص Laravel

وجود:

```text
artisan
```

و:

```text
public/
```

بررسی می‌شود.

در صورت وجود هر دو، Web Root روی:

```text
project/public
```

قرار می‌گیرد.

---

## 8. تنظیم Permission

مالک پروژه:

```text
www-data:www-data
```

خواهد شد.

برای Laravel نیز:

```text
storage/
bootstrap/cache/
```

تنظیم می‌شوند.

---

## 9. تنظیم Nginx

کانفیگ در:

```text
/etc/nginx/sites-available/
```

ساخته شده و در:

```text
/etc/nginx/sites-enabled/
```

فعال می‌شود.

---

## 10. فعال‌سازی SSL

اسکریپت از شما می‌پرسد:

```text
🔒 Configure SSL with Let's Encrypt? [Y/n]:
```

در صورت تأیید، Certbot SSL را تنظیم می‌کند.

---

# 🔄 روند کلی Deploy

هر دو نسخه تقریباً این مراحل را طی می‌کنند:

```text
شروع
 │
 ▼
بررسی Root
 │
 ▼
دریافت Domain
 │
 ▼
دریافت مسیر پروژه
 │
 ▼
نصب نیازمندی‌ها
 │
 ▼
تشخیص PHP-FPM
 │
 ▼
تشخیص Laravel
 │
 ▼
تنظیم Permission
 │
 ▼
ساخت کانفیگ Nginx
 │
 ▼
فعال‌سازی سایت
 │
 ▼
تست Nginx
 │
 ▼
Restart Nginx
 │
 ▼
تنظیم SSL
 │
 ▼
Reload Nginx
 │
 ▼
پایان Deploy
```

---

# ⚠️ نکات مهم

## DNS

قبل از فعال‌سازی SSL، دامنه باید به IP سرور اشاره کند.

مثلاً:

```text
example.com → SERVER_IP
www.example.com → SERVER_IP
```

برای بررسی:

```bash
dig example.com
```

یا:

```bash
nslookup example.com
```

---

## Firewall

پورت‌های زیر باید باز باشند:

```text
80
443
```

برای UFW:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

بررسی:

```bash
sudo ufw status
```

---

## Laravel

ساختار معمول پروژه Laravel:

```text
/var/www/example
├── app/
├── bootstrap/
├── config/
├── database/
├── public/
├── resources/
├── routes/
├── storage/
├── vendor/
├── artisan
└── .env
```

Nginx باید به این مسیر اشاره کند:

```text
/var/www/example/public
```

و نه:

```text
/var/www/example
```

---

## 🔒 نکته امنیتی

در Laravel نباید کل پروژه مستقیماً توسط Nginx قابل دسترسی باشد.

فقط `public/` باید Web Root باشد.

به این شکل فایل‌هایی مثل:

```text
.env
artisan
composer.json
composer.lock
```

مستقیماً از طریق وب قابل دسترسی نخواهند بود.

---

# 🛠️ رفع مشکلات

## بررسی وضعیت Nginx

```bash
systemctl status nginx
```

## تست کانفیگ Nginx

```bash
nginx -t
```

## Restart

```bash
systemctl restart nginx
```

## Reload

```bash
systemctl reload nginx
```

## مشاهده Error Log

```bash
tail -f /var/log/nginx/error.log
```

## مشاهده Access Log

```bash
tail -f /var/log/nginx/access.log
```

---

# 🔐 رفع مشکلات SSL

مشاهده Certificateها:

```bash
certbot certificates
```

تست Renewal:

```bash
certbot renew --dry-run
```

---

# 🚀 Quick Start

## Bash

```bash
chmod +x deploy.sh
sudo ./deploy.sh
```

## Python

```bash
sudo python3 deploy.py
```

سپس:

```text
Domain: example.com
Site folder: /var/www/example
```

و در نهایت:

```text
https://example.com
```

---

# 📄 License

This project is provided for educational and personal use.

این پروژه برای استفاده آموزشی و شخصی ارائه شده است.
