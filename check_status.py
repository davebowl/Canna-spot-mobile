"""
CannaSpot System Status Checker
Verifies all critical components are properly configured.

Usage:
    python check_status.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_var(name, required=True):
    """Check if environment variable is set"""
    value = os.environ.get(name)
    if value:
        # Mask sensitive values
        if 'PASS' in name or 'KEY' in name:
            display = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
        else:
            display = value
        print(f"  ✅ {name} = {display}")
        return True
    else:
        status = "⚠️ " if required else "ℹ️ "
        print(f"  {status} {name} = NOT SET")
        return not required

def check_directory(path, name):
    """Check if directory exists"""
    if os.path.exists(path) and os.path.isdir(path):
        print(f"  ✅ {name}: {path}")
        return True
    else:
        print(f"  ❌ {name}: {path} (NOT FOUND)")
        return False

def check_file(path, name):
    """Check if file exists"""
    if os.path.exists(path) and os.path.isfile(path):
        size = os.path.getsize(path)
        print(f"  ✅ {name}: {path} ({size} bytes)")
        return True
    else:
        print(f"  ⚠️  {name}: {path} (NOT FOUND)")
        return False

def check_python_package(package):
    """Check if Python package is installed"""
    try:
        __import__(package)
        print(f"  ✅ {package}")
        return True
    except ImportError:
        print(f"  ❌ {package} (NOT INSTALLED)")
        return False

def main():
    print("\n" + "="*70)
    print("🌿 CannaSpot v3.6 - System Status Check")
    print("="*70)
    
    all_good = True
    
    # Check .env file
    print("\n📄 Configuration File:")
    env_exists = check_file('.env', '.env file')
    if not env_exists:
        print("  ⚠️  Run: cp .env.example .env")
        all_good = False
    
    # Check environment variables
    print("\n🔧 Environment Variables:")
    all_good &= check_env_var('SECRET_KEY', required=True)
    all_good &= check_env_var('DATABASE_URL', required=False)
    
    print("\n📧 SMTP Email Configuration:")
    smtp_host = check_env_var('SMTP_HOST', required=False)
    smtp_user = check_env_var('SMTP_USER', required=False)
    smtp_pass = check_env_var('SMTP_PASS', required=False)
    check_env_var('SMTP_PORT', required=False)
    check_env_var('SMTP_FROM', required=False)
    
    if not (smtp_host and smtp_user and smtp_pass):
        print("  ⚠️  Email features won't work without SMTP config")
        print("  💡 Run: python setup_email.py")
    
    # Check Python dependencies
    print("\n📦 Python Packages:")
    packages = [
        'flask',
        'flask_sqlalchemy',
        'sqlalchemy',
        'dotenv',
        'itsdangerous',
        'werkzeug',
        'markupsafe'
    ]
    for pkg in packages:
        all_good &= check_python_package(pkg)
    
    # Check directories
    print("\n📁 Directories:")
    all_good &= check_directory('templates', 'Templates')
    all_good &= check_directory('static', 'Static files')
    all_good &= check_directory('uploads', 'Uploads')
    check_directory('uploads/videos', 'Video uploads')
    check_directory('uploads/thumbnails', 'Thumbnails')
    check_directory('uploads/avatars', 'Avatars')
    
    # Check critical files
    print("\n📝 Critical Files:")
    all_good &= check_file('app.py', 'Main application')
    all_good &= check_file('models.py', 'Database models')
    check_file('requirements.txt', 'Dependencies')
    
    # Check templates
    print("\n🎨 Key Templates:")
    templates = [
        'base.html',
        'watch.html',
        'slots.html',
        'voice.html',
        'register.html',
        'login.html'
    ]
    for tmpl in templates:
        check_file(f'templates/{tmpl}', tmpl)
    
    # Check email templates
    print("\n📧 Email Templates:")
    email_templates = [
        'welcome.txt', 'welcome.html',
        'verify_email.txt', 'verify_email.html',
        'reset_password.txt', 'reset_password.html'
    ]
    for tmpl in email_templates:
        check_file(f'templates/email/{tmpl}', tmpl)
    
    # Database check
    print("\n💾 Database:")
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///cannaspot.db')
    if 'sqlite' in db_url:
        db_path = db_url.replace('sqlite:///', '')
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            print(f"  ✅ SQLite database: {db_path} ({size:,} bytes)")
        else:
            print(f"  ℹ️  Database not initialized: {db_path}")
            print(f"  💡 Visit http://localhost:5000/install to set up")
    else:
        print(f"  ℹ️  Using external database: {db_url.split('@')[-1] if '@' in db_url else 'configured'}")
    
    # Summary
    print("\n" + "="*70)
    if all_good:
        print("✅ All critical components are configured!")
        print("\nNext steps:")
        print("  1. python app.py                    # Start the server")
        print("  2. Visit http://localhost:5000      # Open in browser")
        
        if not (smtp_host and smtp_user and smtp_pass):
            print("\n⚠️  Optional: Configure email for verification & password reset")
            print("  → python setup_email.py")
    else:
        print("⚠️  Some components need attention (see above)")
        print("\nRecommended actions:")
        print("  1. pip install -r requirements.txt  # Install missing packages")
        print("  2. cp .env.example .env             # Create config file")
        print("  3. python setup_email.py            # Configure email")
    
    print("="*70 + "\n")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Error during status check: {e}")
        sys.exit(1)
