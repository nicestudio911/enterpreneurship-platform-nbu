#!/usr/bin/env python3
"""
Script to seed the database with entrepreneur competitions
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models.competition import Competition

# Initialize database
init_db()

# List of competitions to add
competitions = [
    "Hult Prize",
    "Startup World Cup",
    "MIT $100K Entrepreneurship Competition",
    "Global Student Entrepreneur Awards (GSEA)",
    "Hello Tomorrow Global Challenge",
    "Slush 100 Pitching Competition",
    "TechCrunch Disrupt Startup Battlefield",
    "MassChallenge",
    "Web Summit PITCH",
    "Startup Grind Global Pitch Competition",
    "IBM Call for Code",
    "Microsoft Imagine Cup (tech-focused)",
    "European Innovation Council (EIC) Accelerator",
    "ClimateLaunchpad (green startups)",
    "XPRIZE Challenges",
    "Chivas Venture",
    "Seedstars World Competition",
    "She Loves Tech Global Competition (female-led)",
    "Youth Entrepreneurship Challenge by JA Worldwide",
    "UN World Tourism Startup Competition",
]

def seed_competitions():
    db = SessionLocal()
    try:
        # Check which competitions already exist
        existing_competitions = {c.name for c in db.query(Competition).all()}
        
        added_count = 0
        for comp_name in competitions:
            if comp_name not in existing_competitions:
                competition = Competition(
                    name=comp_name,
                    description=f"Information about {comp_name} competition. Prompts and instructions will be added separately.",
                    advice_prompt=None,  # Will be added later
                    file_generation_prompt=None  # Will be added later
                )
                db.add(competition)
                added_count += 1
                print(f"Added: {comp_name}")
            else:
                print(f"Already exists: {comp_name}")
        
        db.commit()
        print(f"\nSuccessfully added {added_count} new competitions!")
        print(f"Total competitions in database: {db.query(Competition).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding competitions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_competitions()

