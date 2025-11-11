# 🌿 CannaSpot v3.6 - Cannabis Community Platform

**A feature-rich video hosting & community platform with Discord-style servers, music bot, casino games, and live voice chat.**

---

## � Quick Links

- **Local Development**: See below for setup
- **Email Configuration**: [EMAIL_SETUP.md](EMAIL_SETUP.md)
- **LiteSpeed Deployment**: [LITESPEED_DEPLOY.md](LITESPEED_DEPLOY.md)
- **Deployment Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- **Quick Deploy**: [DEPLOY_QUICK.md](DEPLOY_QUICK.md)
- **Feature Roadmap**: [TODO.md](TODO.md)

---

## 🚀 Quick Start (Local Development)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email (REQUIRED)
Email verification and password reset **will not work** without SMTP configuration.

#### Quick Gmail Setup (5 minutes)
1. **Copy the example config**:
   ```bash
   cp .env.example .env
   ```

2. **Get a Gmail App Password**:
   - Enable 2FA: https://myaccount.google.com/security
   - Generate App Password: https://myaccount.google.com/apppasswords
   - Copy the 16-character password

3. **Edit `.env` file** with your details:
   ```bash
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASS=your-16-char-app-password
   SMTP_FROM=CannaSpot <your-email@gmail.com>
   ```

4. **Test it**:
   ```bash
   python test_email.py your-email@gmail.com
   ```

📖 **Full guide**: See [EMAIL_SETUP.md](EMAIL_SETUP.md)

## 3. Initialize Database
```bash
python app.py
```
On first run, visit `/install` to:
- Configure database (SQLite or MySQL)
- Create admin account
- Set up initial server structure

## 4. Access Your Site
- **Local**: http://localhost:5000
- **Install page**: http://localhost:5000/install

---

## Features Checklist

### ✅ Completed
- [x] Video hosting platform (upload, watch, thumbnails)
- [x] Discord-style servers with text/voice channels
- [x] Music bot (YouTube playback, queue management)
- [x] Casino with 9 slot games (sound effects, animations)
- [x] User authentication (registration, login, profiles)
- [x] Social features (friends, messages, subscriptions)
- [x] Live video chat (WebRTC voice channels)
- [x] Admin panel (ad management, user control)
- [x] Email system (verification, password reset)

### 🔄 In Progress
- [ ] Video comments system (UI exists, backend pending)
- [ ] View counter for videos
- [ ] Remaining casino games (Poker, Wheel, Blackjack)
- [ ] Real-time WebSocket notifications

### 📋 Planned
- [ ] Video recommendations algorithm
- [ ] Server permissions/roles system
- [ ] Mobile app

---

## Project Structure
```
canna-spot-v3.6/
├── app.py                 # Main Flask application (2260 lines)
├── models.py              # Database models (SQLAlchemy)
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
├── .env.example           # Configuration template
├── .env                   # YOUR CONFIG (create from .env.example)
├── EMAIL_SETUP.md         # Email configuration guide
├── test_email.py          # Email testing script
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Main layout
│   ├── watch.html         # Video player
│   ├── slots.html         # Casino games
│   ├── voice.html         # Voice channels
│   └── email/             # Email templates
├── static/
│   ├── css/               # Stylesheets
│   └── js/                # Client-side scripts
└── uploads/               # User-generated content
    ├── videos/
    ├── thumbnails/
    └── avatars/
```

---

## Environment Variables

Required in `.env`:
```bash
SECRET_KEY=your-random-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=CannaSpot <your-email@gmail.com>
```

Optional:
```bash
DATABASE_URL=mysql+pymysql://user:pass@localhost/cannaspot
MAX_CONTENT_LENGTH=536870912  # 512MB
```

---

## Development vs Production

### Development (default)
```bash
python app.py
# Runs on http://localhost:5000
# Debug mode enabled
# SQLite database
```

### Production Deployment
See deployment configs in `deploy/`:
- `apache_directadmin.conf` - DirectAdmin hosting
- `app.wsgi` - WSGI configuration
- `gunicorn.service` - Systemd service

For production:
1. Set a strong `SECRET_KEY`
2. Use MySQL database
3. Configure proper SMTP (not Gmail)
4. Disable debug mode
5. Set up SSL/HTTPS

---

## Troubleshooting

### "SMTP not configured"
- You haven't created a `.env` file
- Run: `cp .env.example .env` and configure SMTP

### "Template not found"
- Check templates/ directory exists
- Restart Flask app

### "Database errors"
- Delete `cannaspot.db` and restart
- Visit `/install` to reinitialize

### "Port 5000 already in use"
- Kill existing process: `pkill -f "python app.py"`
- Or change port in app.py

---

## Support

Need help? Check:
1. [EMAIL_SETUP.md](EMAIL_SETUP.md) - Email configuration
2. Console output - Look for error messages
3. Browser console - Check for JavaScript errors
4. Database logs - Check SQLite/MySQL logs

---

## License & Credits

CannaSpot v3.6 - Community-focused video platform
Built with Flask, SQLAlchemy, and modern web technologies.
