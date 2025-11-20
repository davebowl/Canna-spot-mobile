"""
Database Migration Script
Adds new columns to existing tables for v3.6 features
"""

import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'cannaspot.db')



def migrate():
    print("🔧 Starting database migration...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    migrations = []

    # Add pw_hash column to User table
    try:
        cursor.execute("SELECT pw_hash FROM user LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("User.pw_hash", "ALTER TABLE user ADD COLUMN pw_hash VARCHAR(256)"))

    # Add dname column to User table
    try:
        cursor.execute("SELECT dname FROM user LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("User.dname", "ALTER TABLE user ADD COLUMN dname VARCHAR(120)"))

    # Add admin column to User table
    try:
        cursor.execute("SELECT admin FROM user LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("User.admin", "ALTER TABLE user ADD COLUMN admin BOOLEAN DEFAULT 0"))

    # Add avatar column to User table
    try:
        cursor.execute("SELECT avatar FROM user LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("User.avatar", "ALTER TABLE user ADD COLUMN avatar VARCHAR(255)"))

    # Add p_html column to User table
    try:
        cursor.execute("SELECT p_html FROM user LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("User.p_html", "ALTER TABLE user ADD COLUMN p_html TEXT"))

    # Add status column to User table
    try:
        cursor.execute("SELECT status FROM user LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("User.status", "ALTER TABLE user ADD COLUMN status VARCHAR(20) DEFAULT 'online'"))

    # Add seen column to User table
    try:
        cursor.execute("SELECT seen FROM user LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("User.seen", "ALTER TABLE user ADD COLUMN seen DATETIME"))

    # Add created column to User table
    try:
        cursor.execute("SELECT created FROM user LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("User.created", "ALTER TABLE user ADD COLUMN created DATETIME"))

    # Add created column to Server table
    try:
        cursor.execute("SELECT created FROM server LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("Server.created", "ALTER TABLE server ADD COLUMN created DATETIME"))

    # Add uname column to User table
    try:
        cursor.execute("SELECT uname FROM user LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("User.uname", "ALTER TABLE user ADD COLUMN uname VARCHAR(80)"))
    
    # Add owner column to Server table
    try:
        cursor.execute("SELECT owner FROM server LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("Server.owner", "ALTER TABLE server ADD COLUMN owner INTEGER"))

    # Add icon column to Server table
    try:
        cursor.execute("SELECT icon FROM server LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("Server.icon", "ALTER TABLE server ADD COLUMN icon VARCHAR(255)"))

    # Add category and position to Channel table
    try:
        cursor.execute("SELECT category FROM channel LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("Channel.category", "ALTER TABLE channel ADD COLUMN category VARCHAR(100)"))
    
    try:
        cursor.execute("SELECT position FROM channel LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("Channel.position", "ALTER TABLE channel ADD COLUMN position INTEGER DEFAULT 0"))
    
    # Create Role table if it doesn't exist
    try:
        cursor.execute("SELECT * FROM role LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("Role table", """
            CREATE TABLE role (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id INTEGER NOT NULL,
                name VARCHAR(100) NOT NULL,
                color VARCHAR(7) DEFAULT '#99AAB5',
                position INTEGER DEFAULT 0,
                is_admin BOOLEAN DEFAULT 0,
                can_manage_channels BOOLEAN DEFAULT 0,
                can_manage_roles BOOLEAN DEFAULT 0,
                can_kick_members BOOLEAN DEFAULT 0,
                can_ban_members BOOLEAN DEFAULT 0,
                can_send_messages BOOLEAN DEFAULT 1,
                can_manage_messages BOOLEAN DEFAULT 0,
                can_mention_everyone BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (server_id) REFERENCES server(id)
            )
        """))
    
    # Create RoleMembership table if it doesn't exist
    try:
        cursor.execute("SELECT * FROM role_membership LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("RoleMembership table", """
            CREATE TABLE role_membership (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (role_id) REFERENCES role(id)
            )
        """))
    
    # Create Advertisement table if it doesn't exist
    try:
        cursor.execute("SELECT * FROM advertisement LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("Advertisement table", """
            CREATE TABLE advertisement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                content TEXT,
                image VARCHAR(255),
                link VARCHAR(500),
                placement VARCHAR(50) DEFAULT 'sidebar',
                is_active BOOLEAN DEFAULT 1,
                click_count INTEGER DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))
    
    # Create Post table if it doesn't exist
    try:
        cursor.execute("SELECT * FROM post LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("Post table", """
            CREATE TABLE post (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title VARCHAR(200) NOT NULL,
                content_raw TEXT NOT NULL,
                content_html TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """))
    
    # Create MusicBot table if it doesn't exist
    try:
        cursor.execute("SELECT * FROM music_bot LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("MusicBot table", """
            CREATE TABLE music_bot (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                is_playing BOOLEAN DEFAULT 0,
                is_paused BOOLEAN DEFAULT 0,
                current_song VARCHAR(500),
                current_song_title VARCHAR(200),
                loop_mode VARCHAR(20) DEFAULT 'off',
                is_shuffled BOOLEAN DEFAULT 0,
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (channel_id) REFERENCES channel(id)
            )
        """))
    
    # Add loop_mode and is_shuffled to existing music_bot table
    try:
        cursor.execute("SELECT loop_mode FROM music_bot LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("MusicBot.loop_mode", "ALTER TABLE music_bot ADD COLUMN loop_mode VARCHAR(20) DEFAULT 'off'"))
    
    try:
        cursor.execute("SELECT is_shuffled FROM music_bot LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("MusicBot.is_shuffled", "ALTER TABLE music_bot ADD COLUMN is_shuffled BOOLEAN DEFAULT 0"))
    
    # Create MusicQueue table if it doesn't exist
    try:
        cursor.execute("SELECT * FROM music_queue LIMIT 1")
    except sqlite3.OperationalError:
        migrations.append(("MusicQueue table", """
            CREATE TABLE music_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER NOT NULL,
                added_by INTEGER NOT NULL,
                song_url VARCHAR(500) NOT NULL,
                song_title VARCHAR(200),
                position INTEGER DEFAULT 0,
                is_played BOOLEAN DEFAULT 0,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (channel_id) REFERENCES channel(id),
                FOREIGN KEY (added_by) REFERENCES user(id)
            )
        """))
    
    # Execute migrations
    if migrations:
        print(f"📝 Found {len(migrations)} migration(s) to apply:")
        for name, sql in migrations:
            print(f"   - {name}")
            try:
                cursor.execute(sql)
                print(f"   ✅ {name} applied")
            except Exception as e:
                print(f"   ⚠️ {name} failed: {e}")
        
        conn.commit()
        print("✅ Migration complete!")
    else:
        print("✅ Database already up to date!")
    
    conn.close()

if __name__ == "__main__":
    migrate()
