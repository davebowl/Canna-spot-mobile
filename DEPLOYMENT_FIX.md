# 🚨 Deployment Fix Guide - CannaSpot v3.6

## Issue Identified
**Error**: Service unhealthy - deployment c3fc06dc failed to complete

## Root Causes Fixed
1. ✅ **Missing Procfile** - Added to specify web process
2. ✅ **WSGI configuration** - Updated to handle production environments
3. ✅ **Environment variables** - Made .env optional for cloud deployments
4. ✅ **Database initialization** - Auto-creates tables on startup
5. ✅ **Health check endpoint** - Added `/health` for platform monitoring
6. ✅ **Python version** - Specified via runtime.txt
7. ✅ **Dependencies** - Added missing cryptography package

---

## Files Created/Updated

### 1. **Procfile** (NEW)
```
web: gunicorn --bind 0.0.0.0:$PORT wsgi:application --timeout 120 --workers 4
```
- Tells the platform how to start your app
- Uses gunicorn with 4 workers
- Binds to the PORT environment variable (auto-provided by most platforms)

### 2. **runtime.txt** (NEW)
```
python-3.11.9
```
- Specifies Python version for deployment platform

### 3. **wsgi.py** (UPDATED)
- Now handles missing .env file gracefully
- Auto-creates database tables on startup
- Works with both DirectAdmin and cloud platforms

### 4. **app.py** (UPDATED)
- Added `/health` endpoint for deployment health checks
- Returns database status and upload directory verification

### 5. **requirements.txt** (UPDATED)
- Added `cryptography==43.0.3` (needed for SMTP/SSL)

---

## Environment Variables Required

Set these in your deployment platform's environment settings:

### Required:
```bash
SECRET_KEY=your-secret-key-here-64-chars-minimum
DATABASE_URL=your-database-connection-string
```

### Optional (Email):
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=no-reply@cannaspot.com
SMTP_USE_TLS=true
```

### Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Deployment Platform Instructions

### For Render.com:
1. Connect your GitHub repository
2. Set **Build Command**: `pip install -r requirements.txt`
3. Set **Start Command**: `gunicorn --bind 0.0.0.0:$PORT wsgi:application --timeout 120 --workers 4`
4. Add environment variables in dashboard
5. Deploy!

### For Railway.app:
1. Connect your GitHub repository
2. Railway auto-detects Procfile
3. Add environment variables in dashboard
4. Deploy!

### For Heroku:
1. Connect your GitHub repository
2. Heroku auto-detects Procfile and runtime.txt
3. Add environment variables: `heroku config:set SECRET_KEY=...`
4. Deploy: `git push heroku main`

### For Fly.io:
1. Install flyctl CLI
2. Run `fly launch`
3. Set secrets: `fly secrets set SECRET_KEY=...`
4. Deploy: `fly deploy`

---

## Database Setup

### SQLite (Default - Not recommended for production)
- Auto-creates `cannaspot.db` in project root
- Works locally but may not persist on cloud platforms

### PostgreSQL (Recommended for production)
```bash
# DATABASE_URL format:
postgresql://username:password@host:port/database

# Example:
postgresql://cannaspot_user:secret123@db.example.com:5432/cannaspot_db
```

### MySQL
```bash
# DATABASE_URL format:
mysql+pymysql://username:password@host:port/database

# Example:
mysql+pymysql://cannaspot_user:secret123@mysql.example.com:3306/cannaspot_db
```

---

## Post-Deployment Steps

### 1. Verify Health
Visit: `https://your-app-url.com/health`

Expected response:
```json
{
  "status": "healthy",
  "version": "3.6",
  "database": "healthy",
  "upload_dirs": {
    "videos": true,
    "thumbnails": true,
    "avatars": true
  }
}
```

### 2. Initialize Database
Visit: `https://your-app-url.com/install`

- Create admin account
- Set up initial server structure

### 3. Test Core Features
- [ ] User registration
- [ ] Login/logout
- [ ] Video upload (if file storage configured)
- [ ] Server creation
- [ ] Admin panel access

---

## Troubleshooting

### Error: "Application failed to respond"
**Solution**: Check that PORT environment variable is being used
```python
# In Procfile:
gunicorn --bind 0.0.0.0:$PORT wsgi:application
```

### Error: "Database connection failed"
**Solution**: Verify DATABASE_URL is correct
```bash
# Test connection:
python -c "from sqlalchemy import create_engine; create_engine('YOUR_DATABASE_URL').connect()"
```

### Error: "Module not found"
**Solution**: Ensure all dependencies in requirements.txt
```bash
pip install -r requirements.txt
```

### Error: "Permission denied" for uploads
**Solution**: Cloud platforms often use ephemeral storage. Options:
1. Use cloud storage (AWS S3, Cloudinary, etc.)
2. Store files in database (not recommended for videos)
3. Use platform's persistent storage volumes

---

## File Storage Options

### Option 1: Local Storage (Default)
- Works for development
- May not persist on cloud platforms (Heroku, Railway)
- Files lost on each deployment

### Option 2: Cloud Storage (Recommended)
Install additional packages:
```bash
pip install boto3  # For AWS S3
pip install cloudinary  # For Cloudinary
```

Update app.py to use cloud storage for uploads.

### Option 3: Persistent Volumes
Some platforms offer persistent storage:
- Railway: Volumes (paid)
- Render: Persistent Disks (paid)
- Fly.io: Volumes

---

## Environment Variable Examples

### Development (.env file):
```bash
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///cannaspot.db
SMTP_HOST=
SMTP_PORT=587
```

### Production (Platform dashboard):
```bash
FLASK_ENV=production
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
DATABASE_URL=postgresql://user:pass@host:5432/cannaspot
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=SG.xxxxxxxxxxxxxx
SMTP_FROM=no-reply@cannaspot.com
SMTP_USE_TLS=true
```

---

## Quick Deployment Checklist

- [x] ✅ Procfile created
- [x] ✅ runtime.txt created
- [x] ✅ wsgi.py updated
- [x] ✅ Health endpoint added
- [x] ✅ requirements.txt complete
- [ ] 🔲 Set SECRET_KEY environment variable
- [ ] 🔲 Set DATABASE_URL environment variable
- [ ] 🔲 Configure SMTP (optional but recommended)
- [ ] 🔲 Push to GitHub
- [ ] 🔲 Connect repository to deployment platform
- [ ] 🔲 Deploy and verify /health endpoint
- [ ] 🔲 Visit /install to set up admin account

---

## Next Steps

1. **Commit these changes:**
```bash
git add .
git commit -m "Fix deployment: Add Procfile, health check, update WSGI"
git push origin main
```

2. **Redeploy on your platform:**
   - Platform should auto-detect changes
   - New deployment will use updated configuration

3. **Monitor deployment:**
   - Check platform logs for errors
   - Visit /health endpoint to verify
   - Test /install page

4. **Configure production settings:**
   - Set strong SECRET_KEY
   - Use production database (PostgreSQL recommended)
   - Configure email service (SendGrid, Mailgun, etc.)

---

## Support

If deployment still fails:
1. Check platform logs for specific error messages
2. Verify all environment variables are set
3. Test database connection separately
4. Ensure Python version matches runtime.txt
5. Check that requirements.txt installs successfully locally

**All fixes applied and ready for redeployment!** 🚀
