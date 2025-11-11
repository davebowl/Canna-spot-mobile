#!/usr/bin/env python3
"""
Reset database for fresh installation test
Creates backup before deleting data
"""

import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cannaspot.db")
INSTANCE_DB_PATH = os.path.join(BASE_DIR, "instance", "cannaspot.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

def reset_for_install():
    """Backup and reset database for fresh installation"""
    
    # Create backup directory
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Backup database if it exists (check both locations)
    db_backed_up = False
    if os.path.exists(DB_PATH):
        backup_db = os.path.join(BACKUP_DIR, f"cannaspot_pre_test_{timestamp}.db")
        shutil.copy2(DB_PATH, backup_db)
        print(f"✅ Database backed up to: {backup_db}")
        os.remove(DB_PATH)
        print(f"✅ Deleted root database")
        db_backed_up = True
    
    if os.path.exists(INSTANCE_DB_PATH):
        backup_db = os.path.join(BACKUP_DIR, f"cannaspot_instance_pre_test_{timestamp}.db")
        shutil.copy2(INSTANCE_DB_PATH, backup_db)
        print(f"✅ Instance database backed up to: {backup_db}")
        os.remove(INSTANCE_DB_PATH)
        print(f"✅ Deleted instance database")
        db_backed_up = True
    
    if not db_backed_up:
        print("ℹ️  No database found to backup")
    
    # Backup uploads if they exist
    if os.path.exists(UPLOAD_DIR) and any(os.scandir(UPLOAD_DIR)):
        backup_uploads = os.path.join(BACKUP_DIR, f"uploads_pre_test_{timestamp}")
        shutil.copytree(UPLOAD_DIR, backup_uploads, dirs_exist_ok=True)
        print(f"✅ Uploads backed up to: {backup_uploads}")
        
        # Clear uploads but keep directories
        for root, dirs, files in os.walk(UPLOAD_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"⚠️  Could not delete {file}: {e}")
        print(f"✅ Cleared uploads directory")
    else:
        print("ℹ️  No uploads found to backup")
    
    print("\n" + "="*60)
    print("🎉 Database reset complete!")
    print("="*60)
    print("\nYou can now test the installation:")
    print("1. Start the server: python app.py")
    print("2. Visit: http://localhost:5000/welcome")
    print("3. Click 'Continue to Installation'")
    print("4. Complete the installation wizard")
    print("\n💾 Your data is safely backed up in the 'backups' folder")

if __name__ == "__main__":
    print("🔄 Resetting database for installation test...")
    print("=" * 60)
    
    response = input("\n⚠️  This will delete all current data (but create backups).\nContinue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        reset_for_install()
    else:
        print("❌ Reset cancelled")
