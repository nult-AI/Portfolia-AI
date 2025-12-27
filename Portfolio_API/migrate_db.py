"""
Database migration script to update schema to Dataverse-compatible format
Run this script once to recreate all tables with new schema
"""
from app.core.database import engine, Base
from app.models.models import (
    User, Profile, SkillCategory, Skill, OtherSkill,
    Experience, ExperienceDuty, ExperienceDomain, Education
)

def migrate_database():
    print("Starting database migration...")
    
    # Drop all tables
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables with new schema
    print("Creating tables with Dataverse-compatible schema...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Migration completed successfully!")
    print("\nCreated tables:")
    print("  - profiles")
    print("  - skill_categories")
    print("  - skills")
    print("  - other_skills")
    print("  - experiences")
    print("  - experience_duties")
    print("  - experience_domains")
    print("  - educations")

if __name__ == "__main__":
    migrate_database()
