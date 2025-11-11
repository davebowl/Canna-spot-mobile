from app import app, db, User

with app.app_context():
    # Make david an admin
    username = "david"
    
    user = User.query.filter_by(username=username).first()
    if user:
        user.is_admin = True
        db.session.commit()
        print(f"✅ {username} is now an admin!")
        print(f"Visit: http://localhost:5000/theGspot")
    else:
        print(f"❌ User '{username}' not found")
