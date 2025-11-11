# 🚀 LiteSpeed Deployment Guide - CannaSpot v3.6

## LiteSpeed + DirectAdmin Installation

### Prerequisites
- DirectAdmin control panel
- LiteSpeed Web Server (LSWS)
- Python 3.8+ support
- SSH access to your server
- Domain name pointed to your server

---

## Part 1: Upload Files

### 1. Connect via FTP/SFTP
Use FileZilla, WinSCP, or DirectAdmin File Manager

### 2. Upload to Document Root
Upload all files to: `/home/username/domains/your-domain.com/public_html/`

**Directory structure after upload:**
```
public_html/
├── app.py
├── models.py
├── init_db.py
├── requirements.txt
├── .env.example
├── templates/
├── static/
├── uploads/
│   ├── videos/
│   ├── thumbnails/
│   └── avatars/
└── deploy/
```

### 3. Set Permissions
```bash
cd ~/domains/your-domain.com/public_html
chmod 755 .
chmod -R 755 static/
chmod -R 777 uploads/
```

---

## Part 2: Python Environment Setup

### 1. SSH into Your Server
```bash
ssh username@your-domain.com
cd ~/domains/your-domain.com/public_html
```

### 2. Create Virtual Environment
```bash
# Check Python version
python3 --version  # Should be 3.8 or higher

# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # For running the app
```

### 4. Configure Environment
```bash
# Copy example config
cp .env.example .env

# Generate secret key
python3 -c "import secrets; print(f'SECRET_KEY={secrets.token_hex(32)}')"

# Edit .env with nano or vi
nano .env
```

**Required .env settings:**
```bash
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=sqlite:///cannaspot.db  # Or MySQL connection string
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=CannaSpot <your-email@gmail.com>
```

---

## Part 3: LiteSpeed Configuration

### Option A: Python WSGI App (Recommended for LiteSpeed)

#### 1. Create .htaccess
Create `public_html/.htaccess`:
```apache
RewriteEngine On
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ /wsgi.py/$1 [QSA,L]
```

#### 2. Create wsgi.py Entry Point
Create `public_html/wsgi.py`:
```python
import sys
import os

# Add application directory
sys.path.insert(0, os.path.dirname(__file__))

# Load virtual environment
activate_this = os.path.join(os.path.dirname(__file__), 'venv/bin/activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})

# Import Flask app
from app import app as application

# For LiteSpeed WSGI
if __name__ == '__main__':
    application.run()
```

#### 3. Set Permissions
```bash
chmod 755 wsgi.py
```

#### 4. Configure in DirectAdmin
1. Go to **DirectAdmin** → **Python Setup**
2. Create new Python app:
   - **Entry point**: `wsgi.py`
   - **Python version**: 3.8+
   - **Application root**: `/home/username/domains/your-domain.com/public_html`
3. Restart Python app

---

### Option B: Gunicorn + Reverse Proxy (Alternative)

#### 1. Create Gunicorn Startup Script
Create `public_html/start_gunicorn.sh`:
```bash
#!/bin/bash
cd /home/username/domains/your-domain.com/public_html
source venv/bin/activate
gunicorn -w 4 -b 127.0.0.1:8000 app:app --timeout 300
```

Make executable:
```bash
chmod +x start_gunicorn.sh
```

#### 2. Create .htaccess for Reverse Proxy
Create `public_html/.htaccess`:
```apache
RewriteEngine On

# Serve static files directly
RewriteCond %{REQUEST_URI} ^/static/
RewriteRule ^ - [L]

RewriteCond %{REQUEST_URI} ^/uploads/
RewriteRule ^ - [L]

# Proxy everything else to Gunicorn
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ http://127.0.0.1:8000/$1 [P,L]
```

#### 3. Start Gunicorn
```bash
./start_gunicorn.sh &
```

#### 4. Keep Gunicorn Running (systemd or cron)
Add to crontab:
```bash
crontab -e
```
Add line:
```cron
@reboot cd /home/username/domains/your-domain.com/public_html && ./start_gunicorn.sh
```

---

## Part 4: Database Setup

### Option 1: SQLite (Default - Easiest)
```bash
cd ~/domains/your-domain.com/public_html

# Database will be created automatically
# Just ensure permissions
chmod 666 cannaspot.db  # After first run
```

### Option 2: MySQL (Recommended for Production)

#### 1. Create Database in DirectAdmin
1. Go to **MySQL Management**
2. Create database: `username_cannaspot`
3. Create user: `username_canna`
4. Set password and grant all privileges

#### 2. Update .env
```bash
DATABASE_URL=mysql+pymysql://username_canna:password@localhost/username_cannaspot
```

#### 3. Install MySQL driver
```bash
source venv/bin/activate
pip install pymysql
```

---

## Part 5: Initialize Application

### 1. Run Initial Setup
```bash
cd ~/domains/your-domain.com/public_html
source venv/bin/activate
python3 init_db.py  # Initialize database
```

### 2. Visit Install Page
Navigate to: `https://your-domain.com/install`

Complete the setup wizard:
- Choose database type
- Create admin account
- Set up initial server

---

## Part 6: SSL/HTTPS Setup

### 1. In DirectAdmin
1. Go to **SSL Certificates**
2. Select **Let's Encrypt**
3. Generate certificate for your domain
4. Enable "Secure SSL"

### 2. Force HTTPS (Optional)
Add to `.htaccess` at top:
```apache
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

---

## Part 7: File Upload Configuration

### 1. Increase Upload Limits
Create/edit `public_html/.user.ini`:
```ini
upload_max_filesize = 512M
post_max_size = 512M
max_execution_time = 600
max_input_time = 600
memory_limit = 256M
```

### 2. LiteSpeed Limits
In DirectAdmin → **Domain Setup**:
- Set max upload size to 512MB

---

## Part 8: Performance Optimization

### 1. Enable LiteSpeed Cache
Create `public_html/.htaccess` additions:
```apache
<IfModule LiteSpeed>
    # Cache static files
    CacheLookup on
    
    # Don't cache these
    RewriteRule ^(api|admin) - [E=Cache-Control:no-cache]
</IfModule>
```

### 2. Enable Gzip Compression
```apache
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css application/javascript
</IfModule>
```

---

## Troubleshooting

### App Not Loading
```bash
# Check Python app logs
tail -f ~/domains/your-domain.com/public_html/error.log

# Restart Python app (DirectAdmin)
# Or restart Gunicorn:
pkill gunicorn
./start_gunicorn.sh &
```

### Database Errors
```bash
# Check database exists
ls -la cannaspot.db

# Reinitialize
rm cannaspot.db
python3 init_db.py
```

### Upload Errors
```bash
# Fix permissions
chmod -R 777 uploads/
chown -R username:username uploads/
```

### Python Module Not Found
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

---

## Security Checklist

- [ ] Generated strong `SECRET_KEY` in `.env`
- [ ] `.env` file NOT publicly accessible (should be outside public_html or protected)
- [ ] SSL certificate installed
- [ ] HTTPS forced via redirect
- [ ] Database credentials secure
- [ ] File upload directory has no execution permissions
- [ ] Error pages don't expose sensitive info
- [ ] Admin panel accessible only to admins

---

## Production .env Template

```bash
# Production Configuration
SECRET_KEY=your-64-character-random-hex-string-here
DATABASE_URL=mysql+pymysql://username_canna:password@localhost/username_cannaspot

# SMTP (use production email service)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=your-sendgrid-api-key
SMTP_FROM=CannaSpot <noreply@your-domain.com>
SMTP_USE_TLS=true

# Upload limits
MAX_CONTENT_LENGTH=536870912

# Production mode
FLASK_ENV=production
```

---

## Deployment Checklist

- [ ] Files uploaded to server
- [ ] Permissions set (755 for dirs, 777 for uploads)
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured
- [ ] Database initialized (`python3 init_db.py` OR visit `/install`)
- [ ] WSGI/Gunicorn running
- [ ] `.htaccess` configured
- [ ] SSL certificate installed
- [ ] Domain resolves to server
- [ ] Uploads working (test video upload)
- [ ] Email working (test registration)

---

## Support URLs

After deployment, test these:
- `https://your-domain.com` - Home page
- `https://your-domain.com/install` - First-time setup
- `https://your-domain.com/register` - User registration
- `https://your-domain.com/upload` - Video upload
- `https://your-domain.com/slots` - Casino games
- `https://your-domain.com/admin` - Admin panel

---

## Quick Commands Reference

```bash
# Activate venv
source venv/bin/activate

# Check status
python3 check_status.py

# Test email
python3 test_email.py your-email@example.com

# Restart app
pkill gunicorn && ./start_gunicorn.sh &

# Check logs
tail -f error.log

# Update code
git pull  # If using git
pip install -r requirements.txt
```

---

**Ready to deploy!** Start with Part 1 and work through each section. 🚀
