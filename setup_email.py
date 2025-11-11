"""
Interactive Email Configuration Setup
Run this to easily configure SMTP settings for CannaSpot.

Usage:
    python setup_email.py
"""

import os
import secrets

def generate_secret_key():
    """Generate a secure random secret key"""
    return secrets.token_hex(32)

def setup_gmail():
    """Guide user through Gmail SMTP setup"""
    print("\n" + "="*60)
    print("📧 Gmail SMTP Setup")
    print("="*60)
    print("\n⚠️  IMPORTANT WARNINGS:")
    print("  - Gmail is NOT recommended for production")
    print("  - Daily limit: ~500 emails")
    print("  - Requires App Password (less secure)")
    print("  - Risk of account suspension")
    print("\n✅ For production, use:")
    print("  - SendGrid (100/day free)")
    print("  - Mailgun (5K/month free trial)")
    print("  - Amazon SES ($0.10 per 1K emails)")
    print("\n📖 See EMAIL_SETUP.md for production setup guides")
    
    print("\n" + "-"*60)
    cont = input("\nContinue with Gmail anyway? (y/N): ").strip().lower()
    if cont != 'y':
        print("Setup cancelled. Please choose option 3 for production SMTP.")
        return None
    
    print("\nBefore continuing, you need:")
    print("1. A Gmail account with 2-Factor Authentication enabled")
    print("2. An App Password generated for CannaSpot")
    print("\nHow to get an App Password:")
    print("  → Go to: https://myaccount.google.com/apppasswords")
    print("  → Select 'Mail' app and 'Other' device")
    print("  → Name it 'CannaSpot' and click Generate")
    print("  → Copy the 16-character password\n")
    
    input("Press Enter when you're ready to continue...")
    
    email = input("\n📨 Gmail address: ").strip()
    app_password = input("🔑 App Password (16 chars, no spaces): ").strip().replace(" ", "")
    
    if len(app_password) != 16:
        print(f"\n⚠️  Warning: App Password should be 16 characters (you entered {len(app_password)})")
    
    return {
        'SMTP_HOST': 'smtp.gmail.com',
        'SMTP_PORT': '587',
        'SMTP_USER': email,
        'SMTP_PASS': app_password,
        'SMTP_FROM': f'CannaSpot <{email}>',
        'SMTP_USE_TLS': 'true',
        'SMTP_USE_SSL': 'false'
    }

def setup_outlook():
    """Guide user through Outlook SMTP setup"""
    print("\n" + "="*60)
    print("📧 Outlook SMTP Setup")
    print("="*60)
    
    email = input("\n📨 Outlook/Hotmail address: ").strip()
    password = input("🔑 Password: ").strip()
    
    return {
        'SMTP_HOST': 'smtp-mail.outlook.com',
        'SMTP_PORT': '587',
        'SMTP_USER': email,
        'SMTP_PASS': password,
        'SMTP_FROM': f'CannaSpot <{email}>',
        'SMTP_USE_TLS': 'true',
        'SMTP_USE_SSL': 'false'
    }

def setup_custom():
    """Guide user through custom SMTP setup"""
    print("\n" + "="*60)
    print("📧 Custom SMTP Setup")
    print("="*60)
    
    print("\nChoose your SMTP type:")
    print("  1. Web Host Email (cPanel/DirectAdmin/Plesk)")
    print("  2. Other Custom SMTP Server")
    
    choice = input("\nYour choice (1-2): ").strip()
    
    if choice == '1':
        print("\n" + "="*60)
        print("🌐 Web Host SMTP Setup")
        print("="*60)
        print("\nCommon settings for web hosting:")
        print("  - Host: 'localhost' or 'mail.yourdomain.com'")
        print("  - Port: 587 (TLS) or 465 (SSL)")
        print("  - Username: Full email address (e.g., noreply@yourdomain.com)")
        print("  - Password: Email account password")
        print("\n📖 Check your hosting control panel for exact settings")
        print("   (cPanel → Email Accounts, DirectAdmin → Email Accounts)\n")
        
        host = input("🌐 SMTP Host (localhost or mail.yourdomain.com): ").strip() or "localhost"
        port = input("🔌 SMTP Port (587 or 465): ").strip() or "587"
        email = input("📨 Email address (e.g., noreply@yourdomain.com): ").strip()
        password = input("🔑 Email password: ").strip()
        
        use_ssl = port == "465"
        use_tls = port == "587"
    else:
        print("\n" + "="*60)
        print("📧 Custom SMTP Server")
        print("="*60)
        
        host = input("\n🌐 SMTP Host (e.g., smtp.example.com): ").strip()
        port = input("🔌 SMTP Port (usually 587 or 465): ").strip() or "587"
        email = input("📨 Email address: ").strip()
        password = input("🔑 Password: ").strip()
        
        use_ssl = port == "465"
        use_tls = port == "587"
    
    return {
        'SMTP_HOST': host,
        'SMTP_PORT': port,
        'SMTP_USER': email,
        'SMTP_PASS': password,
        'SMTP_FROM': f'CannaSpot <{email}>',
        'SMTP_USE_TLS': 'true' if use_tls else 'false',
        'SMTP_USE_SSL': 'true' if use_ssl else 'false'
    }

def write_env_file(smtp_config, secret_key):
    """Write configuration to .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    # Read existing .env if it exists
    existing_config = {}
    if os.path.exists(env_path):
        print(f"\n⚠️  .env file already exists!")
        overwrite = input("Overwrite it? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Cancelled. Your existing .env was not modified.")
            return False
        
        # Preserve non-SMTP settings
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if not key.startswith('SMTP_') and key != 'SECRET_KEY':
                        existing_config[key] = value
    
    # Write new .env
    with open(env_path, 'w') as f:
        f.write("# CannaSpot v3.6 - Configuration\n")
        f.write("# Auto-generated by setup_email.py\n\n")
        
        f.write("# Flask Secret Key\n")
        f.write(f"SECRET_KEY={secret_key}\n\n")
        
        f.write("# Database\n")
        db_url = existing_config.get('DATABASE_URL', 'sqlite:///cannaspot.db')
        f.write(f"DATABASE_URL={db_url}\n\n")
        
        f.write("# SMTP Email Configuration\n")
        for key, value in smtp_config.items():
            f.write(f"{key}={value}\n")
        f.write("\n")
        
        f.write("# Other Settings\n")
        for key, value in existing_config.items():
            if key not in ['DATABASE_URL', 'SECRET_KEY']:
                f.write(f"{key}={value}\n")
    
    print(f"\n✅ Configuration saved to: {env_path}")
    return True

def main():
    print("\n" + "="*60)
    print("🌿 CannaSpot Email Configuration Wizard")
    print("="*60)
    print("\nThis wizard will help you configure email settings.")
    print("You'll need SMTP credentials from your email provider.\n")
    
    print("Choose your email provider:")
    print("  1. Gmail (⚠️  DEV ONLY - not for production)")
    print("  2. Outlook / Hotmail (⚠️  DEV ONLY)")
    print("  3. Production SMTP (SendGrid, Mailgun, SES, etc.)")
    print("  4. Skip (email features won't work)")
    
    choice = input("\nYour choice (1-4): ").strip()
    
    if choice == '1':
        smtp_config = setup_gmail()
        if smtp_config is None:
            return
    elif choice == '2':
        smtp_config = setup_outlook()
    elif choice == '3':
        smtp_config = setup_custom()
    elif choice == '4':
        print("\n⚠️  Skipping email configuration.")
        print("You can configure it later by editing .env file.")
        smtp_config = {
            'SMTP_HOST': '',
            'SMTP_PORT': '587',
            'SMTP_USER': '',
            'SMTP_PASS': '',
            'SMTP_FROM': 'CannaSpot <noreply@cannaspot.local>',
            'SMTP_USE_TLS': 'true',
            'SMTP_USE_SSL': 'false'
        }
    else:
        print("Invalid choice. Exiting.")
        return
    
    # Generate or preserve secret key
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    secret_key = generate_secret_key()
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('SECRET_KEY='):
                    existing_key = line.split('=', 1)[1].strip()
                    if existing_key and existing_key != 'dev-secret-change-this-in-production':
                        secret_key = existing_key
                        break
    
    # Write configuration
    if write_env_file(smtp_config, secret_key):
        print("\n" + "="*60)
        print("🎉 Setup Complete!")
        print("="*60)
        
        if choice != '4':
            print("\nNext steps:")
            print("  1. Test your email configuration:")
            test_email = smtp_config.get('SMTP_USER', 'your-email@example.com')
            print(f"     python test_email.py {test_email}")
            print("\n  2. Start CannaSpot:")
            print("     python app.py")
            print("\n  3. Register a new account and check for verification email")
        else:
            print("\n⚠️  Email is not configured. To enable it later:")
            print("  1. Edit .env file and add your SMTP settings")
            print("  2. Or run this setup wizard again: python setup_email.py")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Please check your inputs and try again.")
