import sqlite3

conn = sqlite3.connect('cannaspot.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("📋 Database Tables:")
for table in tables:
    print(f"   - {table[0]}")

# Check specifically for music bot tables
music_bot_exists = 'music_bot' in [t[0] for t in tables]
music_queue_exists = 'music_queue' in [t[0] for t in tables]

print(f"\n🎵 Music Bot Tables:")
print(f"   music_bot: {'✅' if music_bot_exists else '❌'}")
print(f"   music_queue: {'✅' if music_queue_exists else '❌'}")

conn.close()
