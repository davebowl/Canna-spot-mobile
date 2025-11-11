# 📋 LiteSpeed Deployment Checklist - CannaSpot v3.6

## Pre-Deployment (Do This First)

- [ ] Have DirectAdmin login credentials
- [ ] Have domain name configured and pointing to server
- [ ] Have SSH access to server
- [ ] Have FTP/SFTP access configured
- [ ] Verified Python 3.8+ is available on server

---

## Step 1: Prepare Files Locally

- [ ] Run `python check_status.py` - verify all files present
- [ ] Create `.env` file with production settings:
  - [ ] Generate secure SECRET_KEY
  - [ ] Configure database (MySQL recommended)
  - [ ] Add SMTP credentials (production email service)
  - [ ] Set MAX_CONTENT_LENGTH
- [ ] Test locally one more time with `python app.py`
- [ ] Create zip of all files (exclude `__pycache__`, `*.pyc`, `cannaspot.db`)

---

## Step 2: Upload to Server

### Via DirectAdmin File Manager:
- [ ] Log into DirectAdmin
- [ ] Navigate to File Manager
- [ ] Go to `domains/your-domain.com/public_html`
- [ ] Upload zip file
- [ ] Extract all files
- [ ] Verify all folders present:
  - [ ] templates/
  - [ ] static/
  - [ ] uploads/ (with subdirectories)
  - [ ] deploy/

### Via FTP/SFTP:
- [ ] Connect to server
- [ ] Navigate to `public_html`
- [ ] Upload all project files
- [ ] Preserve directory structure

---

## Step 3: Server Configuration

### SSH into Server:
```bash
ssh username@your-domain.com
cd ~/domains/your-domain.com/public_html
```

- [ ] Set correct permissions:
  ```bash
  chmod 755 .
  chmod -R 755 static/
  chmod -R 777 uploads/
  chmod 644 .htaccess
  chmod 644 .user.ini
  chmod 755 wsgi.py
  chmod 755 *.sh
  ```

- [ ] Verify `.env` file exists and is NOT publicly accessible:
  ```bash
  ls -la .env
  ```

---

## Step 4: Python Environment

- [ ] Check Python version:
  ```bash
  python3 --version  # Should be 3.8+
  ```

- [ ] Create virtual environment:
  ```bash
  python3 -m venv venv
  ```

- [ ] Activate venv:
  ```bash
  source venv/bin/activate
  ```

- [ ] Upgrade pip:
  ```bash
  pip install --upgrade pip
  ```

- [ ] Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify installations:
  ```bash
  pip list | grep -i flask
  pip list | grep -i sqlalchemy
  ```

---

## Step 5: Database Setup

### Option A: SQLite (Quick Start)
- [ ] No setup needed - will auto-create
- [ ] After first run, set permissions:
  ```bash
  chmod 666 cannaspot.db
  ```

### Option B: MySQL (Production)
- [ ] Create database in DirectAdmin → MySQL Management
  - Database name: `username_cannaspot`
  - Username: `username_canna`
  - Set strong password
  - Grant all privileges
  
- [ ] Update `.env`:
  ```bash
  DATABASE_URL=mysql+pymysql://username_canna:PASSWORD@localhost/username_cannaspot
  ```

- [ ] Install MySQL driver:
  ```bash
  pip install pymysql
  ```

- [ ] Test connection:
  ```bash
  python3 -c "from app import db; print('Database connected!')"
  ```

---

## Step 6: LiteSpeed Configuration

### Method 1: Python WSGI App (Recommended)

- [ ] Verify `wsgi.py` exists in `public_html`
- [ ] Verify `.htaccess` routes to `wsgi.py`
- [ ] In DirectAdmin → Python Setup:
  - [ ] Entry point: `wsgi.py`
  - [ ] Python version: 3.8+
  - [ ] Application root: `/home/username/domains/your-domain.com/public_html`
  - [ ] Restart application

### Method 2: Gunicorn + Proxy

- [ ] Edit `start_gunicorn.sh` with your actual path
- [ ] Start Gunicorn:
  ```bash
  ./start_gunicorn.sh
  ```
- [ ] Verify it's running:
  ```bash
  ps aux | grep gunicorn
  curl http://127.0.0.1:8000
  ```

- [ ] Set up auto-start (crontab):
  ```bash
  crontab -e
  ```
  Add:
  ```
  @reboot cd /home/username/domains/your-domain.com/public_html && ./start_gunicorn.sh
  ```

---

## Step 7: SSL Certificate

- [ ] In DirectAdmin → SSL Certificates
- [ ] Select Let's Encrypt
- [ ] Generate certificate for domain
- [ ] Enable "Secure SSL"
- [ ] Force HTTPS (uncomment in `.htaccess`):
  ```apache
  RewriteCond %{HTTPS} off
  RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  ```

---

## Step 8: Initialize Application

- [ ] Visit: `https://your-domain.com/install`
- [ ] Complete setup wizard:
  - [ ] Choose database type
  - [ ] Create admin account
  - [ ] Set up initial server
- [ ] Verify installation success

---

## Step 9: Test All Features

### Basic Tests:
- [ ] Home page loads: `https://your-domain.com`
- [ ] Register new account
- [ ] Check email for verification (verify SMTP working)
- [ ] Login to account
- [ ] Upload test video (check 512MB limit)
- [ ] Play video
- [ ] Visit casino: `/slots`
- [ ] Join voice channel: `/voice/...`
- [ ] Admin panel: `/admin`

### Upload Tests:
- [ ] Video upload (<100MB)
- [ ] Thumbnail upload
- [ ] Avatar upload
- [ ] Check files appear in `uploads/` directory

### Email Tests:
- [ ] Registration sends welcome email
- [ ] Verification link works
- [ ] Forgot password sends reset email
- [ ] Reset link works

---

## Step 10: Security Hardening

- [ ] Verify `.env` is NOT publicly accessible:
  ```bash
  curl https://your-domain.com/.env  # Should return 403/404
  ```

- [ ] Verify `.htaccess` protects sensitive files:
  ```bash
  curl https://your-domain.com/app.py  # Should return 403
  curl https://your-domain.com/.git/  # Should return 403
  ```

- [ ] Check upload directory security:
  ```bash
  curl https://your-domain.com/uploads/  # Should NOT list files
  ```

- [ ] Review security headers:
  ```bash
  curl -I https://your-domain.com | grep -i "x-"
  ```

- [ ] Ensure HTTPS is enforced (no HTTP access)

- [ ] Set up database backups (DirectAdmin → Backups)

---

## Step 11: Performance Optimization

- [ ] Enable LiteSpeed Cache (already in `.htaccess`)
- [ ] Verify Gzip compression working:
  ```bash
  curl -H "Accept-Encoding: gzip" -I https://your-domain.com
  ```
- [ ] Test upload speed with large file
- [ ] Monitor server resources (CPU/RAM)
- [ ] Set up log rotation if needed

---

## Step 12: Monitoring & Maintenance

- [ ] Check error logs regularly:
  ```bash
  tail -f ~/domains/your-domain.com/public_html/error.log
  ```

- [ ] Monitor disk space (uploads folder):
  ```bash
  du -sh uploads/
  ```

- [ ] Set up automated backups:
  - Database (daily)
  - Uploads folder (weekly)
  - `.env` file (keep secure copy)

- [ ] Create maintenance page (optional)

---

## Troubleshooting

### App Returns 500 Error:
```bash
# Check error log
tail -50 error.log

# Check Python app status
ps aux | grep python

# Restart app
# DirectAdmin: Python Setup → Restart
# Gunicorn: ./stop_gunicorn.sh && ./start_gunicorn.sh
```

### Database Connection Failed:
```bash
# Test database
mysql -u username_canna -p username_cannaspot

# Verify DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

### Uploads Not Working:
```bash
# Fix permissions
chmod -R 777 uploads/
chown -R username:username uploads/

# Check disk space
df -h
```

### Email Not Sending:
```bash
# Test SMTP from server
python3 test_email.py your-email@example.com

# Check .env has SMTP settings
cat .env | grep SMTP
```

---

## Quick Command Reference

```bash
# Activate venv
source venv/bin/activate

# Check app status
python3 check_status.py

# View logs
tail -f error.log
tail -f access.log

# Restart Gunicorn
./stop_gunicorn.sh && ./start_gunicorn.sh

# Database backup (MySQL)
mysqldump -u username_canna -p username_cannaspot > backup.sql

# Check disk usage
du -sh uploads/
df -h
```

---

## Success Criteria

✅ All items checked above
✅ Site accessible via HTTPS
✅ Admin can log in
✅ Videos can be uploaded and played
✅ Emails are being sent
✅ No errors in error.log
✅ SSL certificate valid
✅ Upload limits working (512MB)

---

## Post-Deployment

- [ ] Update DNS records if needed
- [ ] Set up CDN (CloudFlare, etc.) - optional
- [ ] Configure email SPF/DKIM records
- [ ] Add site to Google Search Console
- [ ] Set up monitoring (UptimeRobot, etc.)
- [ ] Create admin documentation
- [ ] Train content moderators

---

**Deployment Complete!** 🎉

Your CannaSpot instance is now live at: `https://your-domain.com`

Next steps: Start uploading content and invite users!
