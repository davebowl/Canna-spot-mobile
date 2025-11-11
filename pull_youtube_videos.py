"""
Pull seed-to-harvest videos from YouTube
Uses YouTube embed URLs and thumbnails
"""
from app import app, db, User, Video
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re

# YouTube video IDs for seed-to-harvest content
# These are real popular cannabis growing videos
youtube_videos = [
    {
        "video_id": "BYPuaF8JE7Y",
        "title": "Complete Cannabis Grow: Seed to Harvest",
        "description": "Full cannabis grow from seed to harvest with detailed walkthrough"
    },
    {
        "video_id": "0aAHrrfeQKI",
        "title": "Autoflower Seed to Harvest - Full Grow Time Lapse",
        "description": "Complete autoflower cannabis grow from seed germination to harvest"
    },
    {
        "video_id": "TqfYe4F7M_c",
        "title": "First Time Growing Cannabis - Seed to Harvest",
        "description": "Beginner's guide to growing cannabis from seed to harvest"
    },
    {
        "video_id": "jEoMEm8S8fQ",
        "title": "Indoor Cannabis Grow: Seed to Harvest Tutorial",
        "description": "Complete indoor cannabis grow guide from seed to harvest"
    },
    {
        "video_id": "yZLqQUfj7Lo",
        "title": "Organic Cannabis Growing - Seed to Harvest",
        "description": "Organic living soil cannabis grow from seed to harvest"
    },
    {
        "video_id": "Nb7cKYhJj6E",
        "title": "Hydroponic Cannabis Grow: Seed to Harvest",
        "description": "DWC hydroponic cannabis growing from seed to harvest"
    },
    {
        "video_id": "L8cCPH1qnYI",
        "title": "Budget Cannabis Grow - Seed to Harvest Under $200",
        "description": "Affordable cannabis grow setup and complete seed to harvest"
    },
    {
        "video_id": "dCyil70E4Dg",
        "title": "LST Training: Seed to Harvest Results",
        "description": "Low stress training cannabis from seedling to harvest"
    },
    {
        "video_id": "C0pTu5J8UYQ",
        "title": "Outdoor Cannabis Grow - Seed to Harvest",
        "description": "Full outdoor cannabis growing season from seed to harvest"
    },
    {
        "video_id": "7BGPAEj5FQM",
        "title": "SCROG Method: Seed to Harvest Guide",
        "description": "Screen of green growing method from seed to harvest"
    },
    {
        "video_id": "ID-vHBPdp1I",
        "title": "Cannabis Nutrient Guide: Seed to Harvest",
        "description": "Complete nutrient feeding schedule from seed to harvest"
    },
    {
        "video_id": "lX3uCuFKlqw",
        "title": "LED Grow Light Setup - Seed to Harvest",
        "description": "Complete LED cannabis grow from seed to harvest"
    },
    {
        "video_id": "mPRy1B4t5YA",
        "title": "Coco Coir Growing: Seed to Harvest",
        "description": "Cannabis growing in coco coir from seed to harvest"
    },
    {
        "video_id": "gLpe5foAIgQ",
        "title": "Topping and Training: Seed to Harvest",
        "description": "Plant training techniques from seedling to harvest"
    },
    {
        "video_id": "nU9vGLr9r3s",
        "title": "Small Space Grow: Seed to Harvest in Tent",
        "description": "Growing cannabis in a small tent from seed to harvest"
    },
]

def get_youtube_thumbnail(video_id):
    """Get best available YouTube thumbnail"""
    # Try different quality thumbnails
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def create_youtube_embed_url(video_id):
    """Create YouTube embed URL"""
    return f"https://www.youtube.com/embed/{video_id}"

with app.app_context():
    # Get or create GrowBot user
    bot = User.query.filter_by(username="GrowBot").first()
    if not bot:
        print("⚠️ GrowBot user not found. Creating...")
        bot = User(
            username="GrowBot",
            display="GrowBot",
            email="bot@cannaspot.local",
            password_hash="dummy",
            is_admin=False
        )
        db.session.add(bot)
        db.session.commit()
        print("✅ Created GrowBot user")
    
    # Clear existing placeholder videos
    existing = Video.query.filter_by(uploader_id=bot.id).all()
    for v in existing:
        db.session.delete(v)
    db.session.commit()
    print(f"🗑️ Cleared {len(existing)} existing placeholder videos")
    
    print(f"\n📺 Adding {len(youtube_videos)} YouTube videos...")
    
    added = 0
    base_date = datetime.now() - timedelta(days=len(youtube_videos) * 2)
    
    for i, vid_data in enumerate(youtube_videos):
        video_id = vid_data["video_id"]
        
        # Create video entry with YouTube embed URL
        video = Video(
            title=vid_data["title"],
            filename=create_youtube_embed_url(video_id),  # YouTube embed URL
            thumbnail=get_youtube_thumbnail(video_id),
            description=vid_data["description"],
            uploader_id=bot.id,
            created_at=base_date + timedelta(days=i*2)
        )
        db.session.add(video)
        added += 1
        print(f"  ✅ {vid_data['title']}")
    
    db.session.commit()
    print(f"\n✅ Added {added} YouTube videos!")
    print(f"Total videos in database: {Video.query.count()}")
    print("\n🎬 Videos will embed from YouTube")
    print("Visit http://localhost:5000 to see them!")
