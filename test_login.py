#!/usr/bin/env python3
"""Check users and help with login"""

from app import app, db, User
import hashlib

with app.app_context():
    users = User.query.all()
    
    if not users:
        print("❌ No users found in database!")
    else:
        print(f"✅ Found {len(users)} user(s):\n")
        for u in users:
            admin_flag = " [ADMIN]" if u.is_admin else ""
            print(f"Username: {u.username}{admin_flag}")
            print(f"Email: {u.email}")
            print(f"Display: {u.display}")
            print(f"Password hash: {u.password_hash[:20]}...")
            print()
        
        # Test login
        test_username = input("\nEnter username to test: ").strip()
        test_password = input("Enter password to test: ").strip()
        
        user = User.query.filter_by(username=test_username).first()
        if not user:
            print(f"\n❌ User '{test_username}' not found!")
        else:
            test_hash = hashlib.sha256(test_password.encode("utf-8")).hexdigest()
            if user.password_hash == test_hash:
                print(f"\n✅ Password CORRECT! Login should work.")
            else:
                print(f"\n❌ Password INCORRECT!")
                print(f"Expected hash: {user.password_hash}")
                print(f"Your hash:     {test_hash}")
