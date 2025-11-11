from app import app, db
from models import Sponsor
from sqlalchemy import inspect

with app.app_context():
    db.create_all()
    print("✅ Tables created:", inspect(db.engine).get_table_names())
    
    # Add sample sponsors if none exist
    if Sponsor.query.count() == 0:
        sponsors = [
            Sponsor(name="GrowLight Pro", url="https://example.com/growlight", logo=None),
            Sponsor(name="Nutrients Plus", url="https://example.com/nutrients", logo=None),
            Sponsor(name="Hydro Systems", url="https://example.com/hydro", logo=None),
            Sponsor(name="Cannabis Seeds Co", url="https://example.com/seeds", logo=None),
            Sponsor(name="Grow Tent Master", url="https://example.com/tents", logo=None),
            Sponsor(name="420 Equipment", url="https://example.com/equipment", logo=None),
        ]
        for sponsor in sponsors:
            db.session.add(sponsor)
        db.session.commit()
        print("✅ Added 6 sample sponsors")
