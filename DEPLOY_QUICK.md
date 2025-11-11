# 🚀 Quick Deploy Guide - LiteSpeed

## 1️⃣ Upload Files (5 min)
```bash
# Via FTP/SFTP to: public_html/
# Upload all project files
```

## 2️⃣ SSH Setup (10 min)
```bash
ssh username@your-domain.com
cd ~/domains/your-domain.com/public_html

# Create venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set permissions
chmod 755 wsgi.py
chmod -R 777 uploads/
```

## 3️⃣ Configure (5 min)
```bash
# Edit .env with production settings
nano .env

# Add:
# - SECRET_KEY (generate with: python3 -c "import secrets; print(secrets.token_hex(32))")
# - DATABASE_URL (MySQL recommended)
# - SMTP credentials
```

## 4️⃣ DirectAdmin Setup (5 min)
1. **Python Setup** → Create app:
   - Entry point: `wsgi.py`
   - Python 3.8+
2. **SSL** → Let's Encrypt → Generate
3. **MySQL** → Create database (if using MySQL)

## 5️⃣ Initialize (2 min)
Visit: `https://your-domain.com/install`
- Create admin account
- Done! ✅

---

## Files You Need:
- ✅ `wsgi.py` - WSGI entry point
- ✅ `.htaccess` - URL routing & security
- ✅ `.user.ini` - PHP/upload limits
- ✅ `.env` - Your configuration
- ✅ `requirements.txt` - Python packages

## Test URLs:
- `https://your-domain.com` - Home
- `https://your-domain.com/install` - Setup
- `https://your-domain.com/register` - Sign up
- `https://your-domain.com/upload` - Upload video
- `https://your-domain.com/slots` - Casino
- `https://your-domain.com/admin` - Admin panel

---

**Full Guide**: See `LITESPEED_DEPLOY.md`
**Checklist**: See `DEPLOYMENT_CHECKLIST.md`
