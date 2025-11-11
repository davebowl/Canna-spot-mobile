"""
Populate recent videos with seed-to-harvest grow content
YouTube search: https://www.youtube.com/results?search_query=seed+to+harvest
"""
from app import app, db, User, Video
from datetime import datetime, timedelta
import secrets

# Sample seed-to-harvest grow videos data
seed_to_harvest_videos = [
    {
        "title": "Complete Cannabis Grow Guide: Seed to Harvest in 90 Days",
        "description": "Full walkthrough of growing cannabis from seed to harvest. Covers germination, vegetative stage, flowering, and harvest techniques.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    },
    {
        "title": "First Time Grower: Seed to Harvest Documentary",
        "description": "Follow along as a first-time grower documents their entire cannabis growing journey from planting seeds to final harvest.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg"
    },
    {
        "title": "Autoflower Seed to Harvest - 75 Day Time Lapse",
        "description": "Time lapse footage of an autoflower cannabis plant from seed germination through harvest in just 75 days.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
    },
    {
        "title": "Indoor Grow Room Setup: Seed to Harvest Guide",
        "description": "Complete indoor grow room setup and management from seed to harvest. Includes lighting, ventilation, nutrients, and training.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/sddefault.jpg"
    },
    {
        "title": "Organic Cannabis Growing: Seed to Harvest",
        "description": "Learn how to grow organic cannabis using living soil and natural nutrients from seed germination to harvest day.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    },
    {
        "title": "Hydroponic Cannabis: Complete Seed to Harvest",
        "description": "Full hydroponic cannabis grow from seed to harvest. DWC system setup, nutrient schedule, and harvest techniques.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
    },
    {
        "title": "Budget Grow: Seed to Harvest for Under $300",
        "description": "Affordable cannabis grow setup and complete seed to harvest using budget-friendly equipment and techniques.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg"
    },
    {
        "title": "LST Training Techniques: Seed to Harvest Results",
        "description": "Low stress training techniques demonstrated from seedling to harvest, maximizing yields through proper plant training.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/sddefault.jpg"
    },
    {
        "title": "Outdoor Cannabis Grow: Seed to Harvest 2024",
        "description": "Full outdoor cannabis growing season from seed planting in spring to fall harvest. Natural sunlight grow techniques.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    },
    {
        "title": "SCROG Method: Seed to Harvest Tutorial",
        "description": "Screen of green (SCROG) growing method from seed to harvest. Complete setup and training techniques for maximum yield.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
    },
    {
        "title": "Nutrient Schedule Guide: Seed to Harvest",
        "description": "Complete nutrient feeding schedule for cannabis from seedling through harvest. Includes flush timing and harvest window.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg"
    },
    {
        "title": "Clone to Harvest vs Seed to Harvest Comparison",
        "description": "Side by side comparison of growing from clones vs seeds, tracking both plants from start to harvest.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/sddefault.jpg"
    },
    {
        "title": "LED Grow Light Setup: Seed to Harvest Guide",
        "description": "Complete LED grow light setup and grow from seed germination to harvest using modern LED technology.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    },
    {
        "title": "Beginner Mistakes: Seed to Harvest Lessons Learned",
        "description": "Common beginner growing mistakes and lessons learned during a complete seed to harvest grow cycle.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
    },
    {
        "title": "Super Soil Grow: Seed to Harvest Organic Method",
        "description": "Water-only super soil cannabis grow from seed to harvest. Build your soil and let the plants thrive naturally.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg"
    },
    {
        "title": "Mainlining Cannabis: Seed to Harvest Training",
        "description": "Mainlining/manifolding cannabis plants from seed through harvest for symmetrical growth and big yields.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/sddefault.jpg"
    },
    {
        "title": "SOG Growing: Seed to Harvest Sea of Green",
        "description": "Sea of green growing method from seed to harvest. Multiple small plants for quick turnaround and consistent yields.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    },
    {
        "title": "Coco Coir Growing: Complete Seed to Harvest",
        "description": "Cannabis growing in coco coir from seed germination through harvest. Hand watering and feed-to-waste techniques.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
    },
    {
        "title": "Topping and FIM: Seed to Harvest Training Guide",
        "description": "Topping and FIM techniques demonstrated from seedling stage through harvest, comparing different training methods.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg"
    },
    {
        "title": "Stealth Grow Cabinet: Seed to Harvest in Small Space",
        "description": "Small stealth grow cabinet build and complete seed to harvest in a compact space with odor control.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/sddefault.jpg"
    }
]

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
    
    print(f"\n📺 Adding {len(seed_to_harvest_videos)} seed-to-harvest videos...")
    
    added = 0
    base_date = datetime.utcnow() - timedelta(days=60)
    
    for i, vid_data in enumerate(seed_to_harvest_videos):
        # Create video with staggered dates (most recent first)
        video = Video(
            title=vid_data["title"],
            filename="/uploads/videos/placeholder.mp4",  # Placeholder
            thumbnail=vid_data["thumbnail"],
            description=vid_data["description"],
            uploader_id=bot.id,
            created_at=base_date + timedelta(days=i*3)  # Space them out
        )
        db.session.add(video)
        added += 1
    
    db.session.commit()
    print(f"✅ Added {added} videos!")
    print(f"\nTotal videos in database: {Video.query.count()}")
    print("Visit http://localhost:5000 to see recent videos")
