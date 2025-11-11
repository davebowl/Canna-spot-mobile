import sys
import os

# Add application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Activate virtual environment if it exists
venv_activate = os.path.join(os.path.dirname(__file__), 'venv/bin/activate_this.py')
if os.path.exists(venv_activate):
    with open(venv_activate) as f:
        exec(f.read(), {'__file__': venv_activate})

# Load environment variables from .env (optional in production)
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, use environment variables directly
    pass

# Import Flask application
from app import app as application

# Create tables on startup (only if they don't exist)
with application.app_context():
    try:
        from models import db
        # Try to create all tables (handles missing DB gracefully)
        db.create_all()
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        print(f"✅ Database ready ({len(existing_tables)} tables exist)")
    except Exception as e:
        print(f"⚠️ Database error: {e}")
        print("Note: SQLite resets on each deployment. Use PostgreSQL for production.")

# WSGI entry point for LiteSpeed
if __name__ == '__main__':
    application.run()
