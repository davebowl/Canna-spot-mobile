from app import app, db
from sqlalchemy import text

with app.app_context():
    # SQLite doesn't support ALTER COLUMN, so we need to recreate the table
    try:
        # Create new table with correct schema
        db.session.execute(text('''
            CREATE TABLE custom_emoji_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category VARCHAR(50) NOT NULL DEFAULT 'custom',
                emoji_char VARCHAR(10),
                image_path VARCHAR(255),
                label VARCHAR(100),
                sort_order INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''))
        print("✅ Created new custom_emoji table")
        
        # Copy existing data
        db.session.execute(text('''
            INSERT INTO custom_emoji_new (id, category, emoji_char, label, sort_order, is_active, created_at)
            SELECT id, category, emoji_char, label, sort_order, is_active, created_at
            FROM custom_emoji
        '''))
        print("✅ Copied existing emoji data")
        
        # Drop old table
        db.session.execute(text('DROP TABLE custom_emoji'))
        print("✅ Dropped old table")
        
        # Rename new table
        db.session.execute(text('ALTER TABLE custom_emoji_new RENAME TO custom_emoji'))
        print("✅ Renamed new table")
        
        db.session.commit()
        print("\n✅ Database updated successfully! emoji_char is now optional.")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")
        print("\nTrying alternative approach...")
        
        # Alternative: Just drop and recreate
        try:
            db.session.execute(text('DROP TABLE IF EXISTS custom_emoji'))
            db.session.commit()
            print("✅ Dropped old table")
            
            # Let SQLAlchemy create it fresh
            from models import CustomEmoji
            db.create_all()
            print("✅ Created fresh custom_emoji table with correct schema")
        except Exception as e2:
            print(f"❌ Alternative failed: {e2}")
