from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # Add view_count column to Video table
        db.session.execute(text('ALTER TABLE video ADD COLUMN view_count INTEGER DEFAULT 0'))
        db.session.commit()
        print("✅ Added view_count column to video table")
    except Exception as e:
        print(f"⚠️ Column might already exist or error: {e}")
        db.session.rollback()
    
    print("\n✅ Database migration complete!")
