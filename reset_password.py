#!/usr/bin/env python3
"""Reset password for user david"""

from app import app, db, User
import hashlib

with app.app_context():
    user = User.query.filter_by(username='david').first()
    
    if not user:
        print("❌ User 'david' not found!")
    else:
        print(f"✅ Found user: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Admin: {user.is_admin}")
        
        # Set a simple password for testing
        new_password = "test123"
        user.password_hash = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
        db.session.commit()
        
        print(f"\n✅ Password reset to: {new_password}")
        print(f"\nNow you can login with:")
        print(f"   Username: david")
        print(f"   Password: {new_password}")
