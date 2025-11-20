#!/usr/bin/env python3
"""Reset password for user david"""

import sys
from app import app, db, User
import hashlib

if len(sys.argv) < 2:
    print("Usage: python reset_password.py <username_or_email> [new_password] [--admin]")
    sys.exit(1)

target = sys.argv[1]
new_password = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else "test123"
make_admin = '--admin' in sys.argv

with app.app_context():
    user = User.query.filter((User.uname == target) | (User.email == target)).first()
    if not user:
        print(f"❌ User '{target}' not found!")
    else:
        # Set default username if missing
        if not user.uname or user.uname == "None":
            # Use email prefix as username
            user.uname = user.email.split('@')[0]
            print(f"   Username was missing, set to: {user.uname}")

        print(f"✅ Found user: {user.uname}")
        print(f"   Email: {user.email}")
        print(f"   Admin: {user.admin}")

        user.pw_hash = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
        if make_admin:
            user.admin = True
            print("   User promoted to ADMIN.")
        db.session.commit()

        print(f"\n✅ Password reset to: {new_password}")
        print(f"\nNow you can login with:")
        print(f"   Username: {user.uname}")
        print(f"   Password: {new_password}")
