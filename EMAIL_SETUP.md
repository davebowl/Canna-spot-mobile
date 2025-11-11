# 📧 Email Setup Guide - CannaSpot v3.6

## Why You Need This
Email verification and password reset features **will not work** until you configure SMTP. Users won't be able to verify their accounts or reset forgotten passwords.

---

## Quick Setup (Gmail)

### Important: Google App Passwords
Google App Passwords are intended for **older apps that don't support modern security**. CannaSpot uses modern Python SMTP with TLS, but Google may still require an App Password for third-party applications.

**Before using Gmail, consider:**
- ⚠️ App Passwords are less secure than modern OAuth2
- ⚠️ Gmail has daily sending limits (~500 emails/day)
- ✅ For production, use dedicated email services (SendGrid, Mailgun, Amazon SES)
- ✅ Gmail is fine for development/testing only

### Step 1: Enable 2-Factor Authentication (Required for App Passwords)
1. Go to your Google Account: https://myaccount.google.com/security
2. Under "Signing in to Google", enable **2-Step Verification**
3. Follow the prompts to set it up

### Step 2: Generate App Password (Only if needed)
1. Go to App Passwords: https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Enter: **CannaSpot**
5. Click **Generate**
6. Copy the 16-character password (looks like: `abcd efgh ijkl mnop`)

**Note**: If you don't see "App passwords", it means:
- 2-Step Verification is not enabled, OR
- Your account is managed by work/school, OR
- You have Advanced Protection enabled

### Step 3: Configure CannaSpot
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and update these lines:
   ```bash
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASS=abcdefghijklmnop  # Your 16-char app password (no spaces)
   SMTP_FROM=CannaSpot <your-email@gmail.com>
   SMTP_USE_TLS=true
   SMTP_USE_SSL=false
   ```

3. Restart your Flask app:
   ```bash
   python app.py
   ```

### Step 4: Test It
1. Register a new account
2. Check your email for the verification link
3. If you see the email, **you're done!** ✅

---

## Alternative Email Providers

### ⭐ Recommended for Production

**These services support modern authentication and are built for transactional emails:**

#### SendGrid (Best for Production)
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=SG.G2eIngIDTaeyVaTPKCVhQg.tQvm6fTvphOvcim51mhQQ_AeUKBdJ7BsgwIU1io8  # Generate at app.sendgrid.com
SMTP_FROM=CannaSpot <quick.parallel@outlook.com>
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```
**Free Tier**: 100 emails/day forever
**Pros**: Excellent deliverability, analytics, modern API
**Get started**: https://signup.sendgrid.com/

#### Mailgun
```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@your-domain.com  # From Mailgun dashboard
SMTP_PASS=your-mailgun-smtp-password
SMTP_FROM=CannaSpot <noreply@your-domain.com>
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```
**Free Tier**: 5,000 emails/month for 3 months
**Pros**: Pay-as-you-go, good documentation
**Get started**: https://www.mailgun.com/

#### Amazon SES (Simple Email Service)
```bash
SMTP_HOST=email-smtp.us-east-1.amazonaws.com  # Your region
SMTP_PORT=587
SMTP_USER=your-smtp-username  # From AWS Console
SMTP_PASS=your-smtp-password
SMTP_FROM=CannaSpot <noreply@your-domain.com>
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```
**Pricing**: $0.10 per 1,000 emails (very cheap)
**Pros**: Scalable, reliable, AWS integration
**Get started**: https://aws.amazon.com/ses/

---

### Web Host SMTP (cPanel, DirectAdmin, Plesk)

**Perfect for shared hosting!** Most web hosts provide free SMTP service with your hosting plan.

#### Finding Your Settings:

**cPanel:**
1. Login to cPanel
2. Go to "Email Accounts"
3. Find your email address (e.g., noreply@yourdomain.com)
4. Click "Connect Devices"
5. Use the SMTP settings shown

**DirectAdmin:**
1. Login to DirectAdmin
2. Go to "Email Accounts"
3. Click your email address
4. View "Email Client Configuration"

**Common Settings:**
```bash
SMTP_HOST=localhost  # or mail.yourdomain.com
SMTP_PORT=587  # TLS (recommended) or 465 for SSL
SMTP_USER=noreply@yourdomain.com  # Full email address
SMTP_PASS=your-email-password
SMTP_FROM=CannaSpot <noreply@yourdomain.com>
SMTP_USE_TLS=true  # Use false if port is 465
SMTP_USE_SSL=false  # Use true if port is 465
```

**Pros:**
- ✅ Free with hosting
- ✅ No third-party signup needed
- ✅ Good for low-medium volume
- ✅ Uses your own domain

**Cons:**
- ⚠️ Limited daily sending (usually 200-500/hour)
- ⚠️ Shared IP (may affect deliverability)
- ⚠️ Less analytics than dedicated services

**Best for:** Small to medium sites on shared hosting

---

### Personal Email Providers (Development Only)

⚠️ **Not recommended for production** - Use only for testing

### Outlook / Hotmail / Live.com
```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASS=your-password
SMTP_FROM=CannaSpot <your-email@outlook.com>
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```
**Note**: You may need to enable "Less secure app access" in Outlook settings.

### Yahoo Mail
```bash
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASS=your-app-password  # Generate at account.yahoo.com/security
SMTP_FROM=CannaSpot <your-email@yahoo.com>
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```
**Note**: Yahoo also requires an app password (not your regular password).

### Custom SMTP Server
```bash
SMTP_HOST=mail.yourdomain.com
SMTP_PORT=587  # or 465 for SSL
SMTP_USER=noreply@yourdomain.com
SMTP_PASS=your-password
SMTP_FROM=CannaSpot <noreply@yourdomain.com>
SMTP_USE_TLS=true  # or false if using SSL
SMTP_USE_SSL=false  # or true for port 465
```

---

## Troubleshooting

### "SMTP not configured" in console
- You haven't created a `.env` file yet
- Run: `cp .env.example .env` and fill in your SMTP settings

### "Authentication failed"
- **Gmail**: Make sure you're using an **App Password**, not your regular password
- **Yahoo**: Same - generate an app password
- **Outlook**: Try enabling "Less secure app access"
- Check that `SMTP_USER` and `SMTP_PASS` are correct

### "Connection timeout"
- Check your firewall isn't blocking port 587 or 465
- Try switching between TLS and SSL:
  - Port 587: `SMTP_USE_TLS=true`, `SMTP_USE_SSL=false`
  - Port 465: `SMTP_USE_TLS=false`, `SMTP_USE_SSL=true`

### Emails go to spam
- Set a proper `SMTP_FROM` name: `Your Site Name <email@domain.com>`
- Consider using a custom domain email instead of Gmail
- Add SPF/DKIM records if using your own domain

### Testing Email Manually
Run this in your Flask console:
```python
from app import send_email
send_email(
    subject="Test Email",
    to="your-email@example.com",
    text_body="This is a test email from CannaSpot.",
    html_body="<h1>Test Email</h1><p>This is a test from CannaSpot.</p>"
)
```

---

## Security Notes

⚠️ **Never commit your `.env` file to Git!** It contains sensitive credentials.

The `.env` file is already in `.gitignore`, but double-check:
```bash
git status  # .env should NOT appear here
```

If it does appear:
```bash
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Exclude .env from git"
```

---

## What Emails Are Sent?

1. **Welcome Email** - Sent when a new user registers
2. **Email Verification** - Contains link to verify email address
3. **Password Reset** - Contains link to reset forgotten password

All email templates are in `templates/email/`:
- `welcome.txt` / `welcome.html`
- `verify_email.txt` / `verify_email.html`
- `reset_password.txt` / `reset_password.html`

You can customize these templates to match your branding!

---

## Production Deployment

**Stop using Gmail for production!** Here's why:

### Why Not Gmail?
- ❌ Daily sending limit (~500 emails)
- ❌ App Passwords less secure than OAuth2
- ❌ Not designed for transactional emails
- ❌ Risk of account suspension
- ❌ No email analytics/tracking
- ❌ Poor deliverability for bulk sends

### Recommended Services:

| Service | Free Tier | Best For | Setup Time |
|---------|-----------|----------|------------|
| **SendGrid** | 100/day forever | Startups, small sites | 5 min |
| **Mailgun** | 5K/month (3 mo) | Medium sites | 10 min |
| **Amazon SES** | $0.10/1000 | Large scale | 15 min |
| **Postmark** | 100/month | High deliverability | 5 min |
| **Brevo (Sendinblue)** | 300/day | EU-based sites | 5 min |

### Quick SendGrid Setup (Recommended)

1. **Sign up**: https://signup.sendgrid.com/
2. **Verify your email**
3. **Create API Key**:
   - Settings → API Keys → Create API Key
   - Name: "CannaSpot SMTP"
   - Permissions: "Full Access" or "Mail Send"
   - Copy the key (starts with `SG.`)

4. **Update .env**:
   ```bash
   SMTP_HOST=smtp.sendgrid.net
   SMTP_PORT=587
   SMTP_USER=apikey
   SMTP_PASS=SG.G2eIngIDTaeyVaTPKCVhQg.tQvm6fTvphOvcim51mhQQ_AeUKBdJ7BsgwIU1io8
   SMTP_FROM=CannaSpot <noreply@ycheapdomains.lol>
   ```

5. **Verify sender** (required):
   - Settings → Sender Authentication
   - Verify single sender OR domain

6. **Test it**:
   ```bash
   python test_email.py your-email@example.com
   ```

**Done!** Much better than Gmail for production. ✅

---

## Best Practices

### Email Deliverability
- ✅ Use a custom domain email (`noreply@yourdomain.com`)
- ✅ Set up SPF, DKIM, and DMARC records
- ✅ Warm up your sending domain gradually
- ✅ Monitor bounce rates and complaints
- ✅ Use plain text + HTML versions

### Security
- ✅ Store SMTP credentials in `.env` (never in code)
- ✅ Use environment-specific configs (dev vs prod)
- ✅ Rotate API keys regularly
- ✅ Monitor for unauthorized access
- ✅ Use TLS/SSL for encryption

### Performance
- ✅ Send emails asynchronously (background jobs)
- ✅ Use email queues for bulk sends
- ✅ Implement retry logic for failures
- ✅ Cache email templates
- ✅ Monitor sending quotas

---

## Need Help?

If emails still aren't working:
1. Check the console output when you register/reset password
2. Look for `[email] Sent to...` or `[email] Failed to send...` messages
3. Verify your SMTP credentials are correct in `.env`
4. Make sure port 587/465 isn't blocked by your firewall/ISP
