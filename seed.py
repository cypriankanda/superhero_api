from app import create_app
from models import db, Hero, Power, HeroPower

# Create the Flask app using the factory
app = create_app()

# Push app context so we can work with db
with app.app_context():
    # Optional: Drop all tables if reseeding
    # db.drop_all()
    # db.create_all()

    print("Seeding data...")

    # Clear existing data
    HeroPower.query.delete()
    Hero.query.delete()
    Power.query.delete()

    # Add heroes
    h1 = Hero(name="Superman", super_name="Clark Kent")
    h2 = Hero(name="Batman", super_name="Bruce Wayne")
    h3 = Hero(name="Wonder Woman", super_name="Diana Prince")

    db.session.add_all([h1, h2, h3])
    db.session.commit()

    # Add powers
    p1 = Power(name="Flight", description="Fly through the sky")
    p2 = Power(name="Super Strength", description="Lift heavy objects")
    p3 = Power(name="Invisibility", description="Become unseen")

    db.session.add_all([p1, p2, p3])
    db.session.commit()

    # Add HeroPowers
    hp1 = HeroPower(strength="Strong", hero_id=h1.id, power_id=p1.id)
    hp2 = HeroPower(strength="Average", hero_id=h1.id, power_id=p2.id)
    hp3 = HeroPower(strength="Weak", hero_id=h2.id, power_id=p3.id)

    db.session.add_all([hp1, hp2, hp3])
    db.session.commit()

    print("✅ Done seeding!")
