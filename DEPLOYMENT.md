# CannaSpot v3.6 - Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Environment Configuration
- [ ] Set `FLASK_ENV=production` environment variable
- [ ] Set strong `SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Configure `DATABASE_URL` for MySQL if not using SQLite
- [ ] Set up email server for notifications (optional)

### 2. Database Setup
- [x] Run migration script: `python migrate_db.py`
- [ ] Create admin account via `/install` page
- [ ] Backup database before deployment

### 3. File Permissions
```bash
chmod -R 755 .
chmod -R 777 uploads/
mkdir -p uploads/videos uploads/thumbnails uploads/avatars uploads/ads
```

### 4. Security
- [x] Debug mode disabled in production (`FLASK_ENV=production`)
- [ ] Change default SECRET_KEY
- [ ] Review upload file size limits (currently 512MB)
- [ ] Configure HTTPS/SSL certificates
- [ ] Set proper CORS headers if needed

### 5. Web Server Setup

#### Option A: DirectAdmin (Recommended for shared hosting)
See `deploy/apache_directadmin.conf` and `deploy/app.wsgi`

1. Upload files to domain directory
2. Create Python virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure Apache custom handlers
5. Set file permissions
6. Run `/install` to setup database

#### Option B: Gunicorn + Apache/Nginx
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Or use systemd service (see deploy/gunicorn.service)
sudo systemctl start cannaspot
sudo systemctl enable cannaspot
```

### 6. Features to Test Post-Deployment
- [ ] User registration and login
- [ ] Video upload and playback
- [ ] Server creation and channels
- [ ] Admin Bot (run setup bot on test server)
- [ ] Advertisement creation and display
- [ ] Posts creation and viewing
- [ ] WebRTC video chat
- [ ] Search functionality
- [ ] Playlists and subscriptions
- [ ] Shorts upload and viewing

### 7. Performance Optimization
- [ ] Enable caching (Redis/Memcached recommended)
- [ ] Configure CDN for static files (optional)
- [ ] Set up video transcoding for different qualities (optional)
- [ ] Enable gzip compression on web server
- [ ] Configure proper database indexes

### 8. Monitoring & Backup
- [ ] Set up error logging (Sentry, LogRocket, etc.)
- [ ] Configure automated database backups
- [ ] Monitor disk space for uploads directory
- [ ] Set up uptime monitoring
- [ ] Configure log rotation

### 9. Documentation
- [x] Admin features documented in `.github/copilot-instructions.md`
- [ ] Create user guide
- [ ] Document API endpoints (if exposing externally)

## 🚀 Quick Deploy Commands

### For DirectAdmin:
```bash
cd ~/domains/your-domain.com/public_html
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python migrate_db.py
# Access https://your-domain.com/install
```

### For VPS/Dedicated Server:
```bash
# Clone/upload project
cd /var/www/cannaspot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python migrate_db.py

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Or install systemd service
sudo cp deploy/gunicorn.service /etc/systemd/system/cannaspot.service
sudo systemctl daemon-reload
sudo systemctl start cannaspot
sudo systemctl enable cannaspot
```

## 📋 Post-Deployment Tasks

1. Visit `/install` to create admin account and configure database
2. Log in as admin
3. Go to Admin Panel and:
   - Create initial server categories
   - Add sponsor listings
   - Create first advertisements
   - Configure custom emojis
4. Test all major features
5. Create backup schedule
6. Monitor error logs for first 24 hours

## 🔧 Troubleshooting

### Database errors:
- Run `python migrate_db.py` again
- Check file permissions on `cannaspot.db`
- Verify DATABASE_URL is correct for MySQL

### File upload errors:
- Check `uploads/` directory permissions (777)
- Verify MAX_CONTENT_LENGTH in app.py
- Check web server upload limits

### 500 errors:
- Set `FLASK_ENV=development` temporarily to see full errors
- Check web server error logs
- Verify all dependencies installed

## 📞 Support
- Review `.github/copilot-instructions.md` for architecture details
- Check app.py for route documentation
- Database models in `models.py`

---

**Version:** 3.6  
**Last Updated:** November 11, 2025
