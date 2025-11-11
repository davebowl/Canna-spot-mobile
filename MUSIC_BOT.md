# Music Bot Feature - CannaSpot v3.6

## Overview
Discord-style music bot that can be invited to voice channels to play music from YouTube URLs.

## Database Models

### MusicBot
- `channel_id`: Voice channel where bot is active
- `is_active`: Whether bot is currently in the channel
- `is_playing`: Whether currently playing a song
- `is_paused`: Whether playback is paused
- `current_song`: URL of current song
- `current_song_title`: Title of current song
- `joined_at`: When bot was invited
- `last_activity`: Last action timestamp

### MusicQueue
- `channel_id`: Voice channel
- `added_by`: User who added the song
- `song_url`: YouTube or other music URL
- `song_title`: Song title
- `position`: Queue position (FIFO)
- `is_played`: Whether song has been played
- `added_at`: When song was added

## API Endpoints

### POST /api/music/bot/invite/<channel_id>
Invite music bot to a voice channel. Creates or reactivates bot instance.

**Response:**
```json
{"success": true, "bot_id": 1}
```

### POST /api/music/bot/kick/<channel_id>
Remove bot from channel. Clears queue and deactivates bot.

### POST /api/music/bot/play/<channel_id>
Add song to queue and start playing if nothing is playing.

**Request:**
```json
{"url": "https://youtube.com/watch?v=...", "title": "Song Title"}
```

**Response:**
```json
{"success": true, "position": 1, "title": "Song Title"}
```

### POST /api/music/bot/skip/<channel_id>
Skip current song, play next in queue.

**Response:**
```json
{"success": true, "next_song": "Next Song Title"}
```

### POST /api/music/bot/pause/<channel_id>
Toggle pause/resume playback.

**Response:**
```json
{"success": true, "paused": true}
```

### POST /api/music/bot/stop/<channel_id>
Stop playback and clear entire queue.

### GET /api/music/bot/queue/<channel_id>
Get current queue and playback status.

**Response:**
```json
{
  "bot_active": true,
  "is_playing": true,
  "is_paused": false,
  "current_song": "Current Song Title",
  "queue": [
    {"title": "Song 1", "url": "...", "position": 1},
    {"title": "Song 2", "url": "...", "position": 2}
  ]
}
```

### GET /api/music/bot/status/<channel_id>
Get bot status (lightweight version of queue endpoint).

**Response:**
```json
{
  "active": true,
  "playing": true,
  "paused": false,
  "current_song": "Current Song Title"
}
```

## UI Components (voice.html)

### Music Bot Section
- **Header**: Shows "🎵 Music Bot" with Invite/Kick button
- **Now Playing**: Displays current song title and status (Playing/Paused/Idle)
- **Playback Controls**: Pause, Skip, Stop buttons
- **Add Song Form**: Input field for YouTube URLs + "Add to Queue" button
- **Queue Display**: Shows upcoming songs with position numbers

### Auto-Refresh
Queue and status automatically refresh every 5 seconds when bot is active.

## YouTube URL Parsing
Extracts video ID from YouTube URLs using regex:
- `youtube.com/watch?v=VIDEO_ID`
- `youtu.be/VIDEO_ID`

## Usage Flow

1. **Invite Bot**: User clicks "Invite Bot" in voice channel
2. **Add Songs**: Paste YouTube URLs and click "Add to Queue"
3. **Playback**: First song auto-plays, subsequent songs queue up
4. **Controls**: Use pause, skip, stop buttons to control playback
5. **Queue Management**: View upcoming songs in queue list
6. **Kick Bot**: Remove bot to clear queue and stop playback

## Future Enhancements
- YouTube Data API integration for automatic title fetching
- Embedded YouTube player for actual audio playback
- SoundCloud and Spotify support
- Volume controls
- Loop/repeat functionality
- Playlist import
- Search command instead of URL pasting
- Vote-to-skip system
- Now playing timestamps/progress bar

## Database Migration
Tables are automatically created via `migrate_db.py` script. Run if upgrading from older version:
```bash
python migrate_db.py
```

## Notes
- Requires user to be logged in (session-based auth)
- Bot persists in channel until kicked
- Queue cleared when bot is kicked
- Each voice channel can have one bot instance
- Songs are tracked by URL (no duplicate detection yet)
