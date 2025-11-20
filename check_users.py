#!/usr/bin/env python3
"""Check what users exist in the database"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import app, db, User

with app.app_context():
    users = User.query.all()
    
    if not users:
        print("✅ No users found in database - /install should work")
    else:
        print(f"❌ Found {len(users)} user(s) in database:")
        print("\nExisting users:")
        for u in users:
            admin_flag = " [ADMIN]" if getattr(u, "is_admin", False) else ""
            print(f"  - {u.uname} ({u.email}){admin_flag} - ID: {u.id}")
        print("\nThis is why /install redirects to /installed")
        print("\nOptions:")
        print("1. Use /installed page instead")
        print("2. Reset database (WARNING: deletes all data)")
        print("3. Login with existing admin account")
