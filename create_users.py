from app import app, db, User, hash_pw

with app.app_context():
    # Create admin user
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            display="Admin",
            email="admin@cannaspot.local",
            password_hash=hash_pw("admin123"),
            is_admin=True
        )
        db.session.add(admin)
        print("✅ Created admin user")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("⚠️ Admin user already exists")
    
    # Create regular user
    regular = User.query.filter_by(username="user").first()
    if not regular:
        regular = User(
            username="user",
            display="Regular User",
            email="user@cannaspot.local",
            password_hash=hash_pw("user123"),
            is_admin=False
        )
        db.session.add(regular)
        print("✅ Created regular user")
        print("   Username: user")
        print("   Password: user123")
    else:
        print("⚠️ Regular user already exists")
    
    # Update david to be regular user (not admin)
    david = User.query.filter_by(username="david").first()
    if david:
        david.is_admin = False
        print("✅ Updated david to regular user (removed admin)")
    
    db.session.commit()
    print("\n📋 User Summary:")
    print(f"   Total users: {User.query.count()}")
    print(f"   Admin users: {User.query.filter_by(is_admin=True).count()}")
    print(f"   Regular users: {User.query.filter_by(is_admin=False).count()}")
