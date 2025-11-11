# 🔧 CheapDomains.lol Deployment Fix

## Issue
Your Flask app works locally (✅ /install route exists), but cheapdomains.lol returns 404 errors.

## Root Cause
CheapDomains.lol likely uses **cPanel** or **DirectAdmin** with Apache/LiteSpeed, which requires specific WSGI configuration.

---

## Solution 1: Python App Setup (Recommended)

### Step 1: Access cPanel/DirectAdmin
1. Log into your hosting control panel
2. Look for "Setup Python App" or "Python Selector"

### Step 2: Create Python Application
```
Application Root: public_html
Application URL: / (or your domain)
Python Version: 3.11 or 3.9+
Application Entry Point: wsgi.py
Application Callable: application
```

### Step 3: Install Dependencies
In the terminal (SSH or web terminal):
```bash
cd ~/public_html
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Restart Application
Click "Restart" button in Python App interface

---

## Solution 2: Passenger WSGI (Alternative)

If using Passenger (Phusion Passenger):

### Create passenger_wsgi.py:
```python
import sys
import os

# Add your application directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import application
from wsgi import application
```

### Restart with .htaccess:
Add to `.htaccess`:
```apache
PassengerEnabled on
PassengerAppRoot /home/username/public_html
PassengerPython /home/username/public_html/venv/bin/python
```

---

## Solution 3: CGI Mode (If no Python app support)

### Create index.cgi:
```python
#!/home/username/public_html/venv/bin/python
import sys
import os
from wsgiref.handlers import CGIHandler

sys.path.insert(0, os.path.dirname(__file__))
from wsgi import application

CGIHandler().run(application)
```

### Make executable:
```bash
chmod +x index.cgi
```

### Update .htaccess:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.cgi/$1 [QSA,L]
```

---

## Solution 4: Contact Support

If none of the above work:

### Check with cheapdomains.lol support:
1. What Python application server they use (WSGI, Passenger, CGI)?
2. Do they support Flask applications?
3. What's the correct configuration for Python apps?

### Common hosting panels:
- **cPanel**: Setup Python App
- **DirectAdmin**: Python Setup
- **Plesk**: Python Environment
- **Custom**: May need manual configuration

---

## Quick Diagnostic Steps

### 1. Check Python Support:
```bash
ssh user@cheapdomains.lol
python3 --version
which python3
```

### 2. Check File Permissions:
```bash
chmod 755 wsgi.py
chmod 644 .htaccess
chmod 755 venv/bin/python
```

### 3. Check Error Logs:
Look for:
- `/home/username/logs/error_log`
- `/home/username/public_html/error_log`
- cPanel → Errors

### 4. Test WSGI Directly:
```bash
cd ~/public_html
source venv/bin/activate
python wsgi.py
```

---

## Environment Variables for Production

Since you're on shared hosting, set these in your control panel:

```bash
SECRET_KEY=<generate-new-64-char-key>
DATABASE_URL=mysql+pymysql://dbuser:dbpass@localhost/dbname
FLASK_ENV=production
```

Or create `.env` file (make sure `.htaccess` protects it):
```bash
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0...
DATABASE_URL=mysql+pymysql://your_db_user:your_db_pass@localhost/your_db_name
SMTP_HOST=mail.cheapdomains.lol
SMTP_PORT=587
SMTP_USER=noreply@yourdomain.com
SMTP_PASS=your_email_password
```

---

## Verify Deployment

Once configured, test:

### 1. Health Check:
```
http://cheapdomains.lol/health
```
Should return JSON with "status": "healthy"

### 2. Install Page:
```
http://cheapdomains.lol/install
```
Should show installation form

### 3. Check Logs:
Review error logs for any Python errors

---

## Most Likely Solution for CheapDomains.lol

Based on the hosting name, they likely use:
1. **cPanel** with mod_wsgi
2. **DirectAdmin** with LSAPI
3. **Custom panel** with Passenger

### Try this first:
1. Log into control panel
2. Find "Python" or "Setup Python App"
3. Create new application pointing to your domain
4. Set entry point to `wsgi:application`
5. Install requirements
6. Restart application

---

## Need More Help?

### Provide these details:
1. What control panel does cheapdomains.lol use?
2. What's in the error logs?
3. Can you run `python wsgi.py` via SSH?
4. What Python version is available?

### Test Files Created:
- `check_routes.py` - Verifies Flask app loads
- `wsgi.py` - WSGI entry point
- `Procfile` - For cloud platforms

Run `python check_routes.py` to verify app works locally.

---

**Next Step**: Contact cheapdomains.lol support and ask:
> "How do I deploy a Flask (Python WSGI) application on my hosting plan?"

They should provide specific instructions for their platform.
