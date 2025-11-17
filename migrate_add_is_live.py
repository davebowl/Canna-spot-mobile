from models import db, Video
from app import app
from sqlalchemy import text
with app.app_context():
    # Only add column if it doesn't exist
    try:
        db.session.execute(text('ALTER TABLE video ADD COLUMN is_live BOOLEAN DEFAULT 0'))
        db.session.commit()
        print("Added is_live column to video table.")
    except Exception as e:
        print(f"Could not add is_live column (may already exist): {e}")