import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# single shared SQLAlchemy object for the app to initialize
db = SQLAlchemy()


class SiteSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(120), default="CannaSpot")
    maintenance_mode = db.Column(db.String(10), default="off")
    custom_message = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    dname = db.Column(db.String(120))
    pw_hash = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)
    p_html = db.Column(db.Text)
    status = db.Column(db.String(20), default="online")  # online, offline, too_stoned
    seen = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime, default=datetime.utcnow)


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))
    icon = db.Column(db.String(255))  # Path to custom server icon image
    created = db.Column(db.DateTime, default=datetime.utcnow)


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server = db.Column(db.Integer, db.ForeignKey("server.id"))
    name = db.Column(db.String(120))
    voice = db.Column(db.Boolean, default=False)  # True for voice channels
    cat = db.Column(db.String(100))  # Category name for grouping
    pos = db.Column(db.Integer, default=0)  # Display order
    created = db.Column(db.DateTime, default=datetime.utcnow)


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    server = db.Column(db.Integer, db.ForeignKey("server.id"))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(7), default="#99AAB5")  # Hex color
    position = db.Column(db.Integer, default=0)  # Higher = more powerful
    # Permissions
    is_admin = db.Column(db.Boolean, default=False)
    can_manage_channels = db.Column(db.Boolean, default=False)
    can_manage_roles = db.Column(db.Boolean, default=False)
    can_kick_members = db.Column(db.Boolean, default=False)
    can_ban_members = db.Column(db.Boolean, default=False)
    can_send_messages = db.Column(db.Boolean, default=True)
    can_manage_messages = db.Column(db.Boolean, default=False)
    can_mention_everyone = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class RoleMembership(db.Model):
    """Links users to roles within a server"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(255))
    description = db.Column(db.Text)
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_live = db.Column(db.Boolean, default=False)  # True if this video is a live stream


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"))
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(140))
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PlaylistVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    position = db.Column(db.Integer)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscriber_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    subscribed_to_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class VideoLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class WatchLater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class Short(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(255))
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255))  # Optional link to related content
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class VoiceParticipant(db.Model):
    """Tracks users currently in voice channels"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_muted = db.Column(db.Boolean, default=False)


class Friendship(db.Model):
    """Tracks friend relationships between users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, accepted, blocked
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime)


class DirectMessage(db.Model):
    """Direct messages between friends"""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class RtcSignal(db.Model):
    """Lightweight signaling messages for WebRTC using HTTP polling.
    Stores SDP offers/answers and ICE candidates addressed to a user in a room.
    """
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(120), index=True, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # null for broadcast
    kind = db.Column(db.String(20), nullable=False)  # offer, answer, candidate, join, leave
    payload = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class RtcParticipant(db.Model):
    """Tracks room participants to coordinate peers without websockets."""
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(120), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class VideoComment(db.Model):
    """Comments on videos with emoji support"""
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class CustomEmoji(db.Model):
    """Custom emojis managed by admins"""
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, default="custom")  # custom, smileys, cannabis, etc
    emoji_char = db.Column(db.String(10))  # The actual emoji character(s) - optional if using image
    image_path = db.Column(db.String(255))  # Path to uploaded emoji image
    label = db.Column(db.String(100))  # Optional description
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Advertisement(db.Model):
    """Small ads displayed throughout the site"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)  # Short description or HTML snippet
    image = db.Column(db.String(255))  # Optional ad image
    link = db.Column(db.String(500))  # Optional clickable link
    placement = db.Column(db.String(50), default="sidebar")  # sidebar, feed, footer, watch
    is_active = db.Column(db.Boolean, default=True)
    click_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MusicBot(db.Model):
    """Music bot for voice channels"""
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_playing = db.Column(db.Boolean, default=False)
    is_paused = db.Column(db.Boolean, default=False)
    current_song = db.Column(db.String(500))  # URL or title of current song
    current_song_title = db.Column(db.String(200))
    loop_mode = db.Column(db.String(20), default="off")  # off, one, all
    is_shuffled = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)


class MusicQueue(db.Model):
    """Queue of songs for music bot"""
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    song_url = db.Column(db.String(500), nullable=False)
    song_title = db.Column(db.String(200))
    position = db.Column(db.Integer, default=0)
    is_played = db.Column(db.Boolean, default=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


def hash_pw(pw: str) -> str:
    import hashlib
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


def safe_slug(name: str) -> str:
    import re, secrets
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    if not s:
        s = secrets.token_hex(3)
    return s


class EmailVerification(db.Model):
    """Tracks email verification state for users without altering the User schema."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    verified_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content_raw = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
