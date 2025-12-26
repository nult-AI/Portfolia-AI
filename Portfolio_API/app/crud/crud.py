from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.models.models import (
    Profile, SkillCategory, Skill, OtherSkill,
    Experience, ExperienceDuty, ExperienceDomain, Education
)

# =====================================================
# Profile CRUD
# =====================================================
def get_profile(db: Session) -> Optional[Profile]:
    """Get the first active profile"""
    return db.query(Profile).filter(Profile.state_code == 0).first()

def create_profile(db: Session, profile_data: dict) -> Profile:
    """Create a new profile"""
    db_profile = Profile(**profile_data)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile_id: UUID, profile_data: dict) -> Optional[Profile]:
    """Update an existing profile"""
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if db_profile:
        for key, value in profile_data.items():
            setattr(db_profile, key, value)
        db.commit()
        db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: UUID) -> bool:
    """Soft delete a profile by setting state_code to 1"""
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if db_profile:
        db_profile.state_code = 1
        db_profile.status_code = 2
        db.commit()
        return True
    return False

# =====================================================
# Skill Category CRUD
# =====================================================
def get_skill_categories(db: Session, include_inactive: bool = False) -> List[SkillCategory]:
    """Get all skill categories ordered by display_order"""
    query = db.query(SkillCategory)
    if not include_inactive:
        query = query.filter(SkillCategory.state_code == 0)
    return query.order_by(SkillCategory.display_order).all()

def get_skill_category(db: Session, category_id: UUID) -> Optional[SkillCategory]:
    """Get a specific skill category by ID"""
    return db.query(SkillCategory).filter(SkillCategory.id == category_id).first()

def create_skill_category(db: Session, category_data: dict) -> SkillCategory:
    """Create a new skill category"""
    db_category = SkillCategory(**category_data)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_skill_category(db: Session, category_id: UUID, category_data: dict) -> Optional[SkillCategory]:
    """Update an existing skill category"""
    db_category = db.query(SkillCategory).filter(SkillCategory.id == category_id).first()
    if db_category:
        for key, value in category_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_skill_category(db: Session, category_id: UUID) -> bool:
    """Soft delete a skill category"""
    db_category = db.query(SkillCategory).filter(SkillCategory.id == category_id).first()
    if db_category:
        db_category.state_code = 1
        db_category.status_code = 2
        db.commit()
        return True
    return False

# =====================================================
# Skill CRUD
# =====================================================
def get_skills(db: Session, category_id: Optional[UUID] = None) -> List[Skill]:
    """Get all skills, optionally filtered by category"""
    query = db.query(Skill).filter(Skill.state_code == 0)
    if category_id:
        query = query.filter(Skill.category_id == category_id)
    return query.all()

def create_skill(db: Session, skill_data: dict) -> Skill:
    """Create a new skill"""
    db_skill = Skill(**skill_data)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def delete_skill(db: Session, skill_id: UUID) -> bool:
    """Soft delete a skill"""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill:
        db_skill.state_code = 1
        db_skill.status_code = 2
        db.commit()
        return True
    return False

# =====================================================
# Other Skill CRUD
# =====================================================
def get_other_skills(db: Session) -> List[OtherSkill]:
    """Get all other skills"""
    return db.query(OtherSkill).filter(OtherSkill.state_code == 0).all()

def create_other_skill(db: Session, skill_data: dict) -> OtherSkill:
    """Create a new other skill"""
    db_skill = OtherSkill(**skill_data)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def update_other_skill(db: Session, skill_id: UUID, skill_data: dict) -> Optional[OtherSkill]:
    """Update an existing other skill"""
    db_skill = db.query(OtherSkill).filter(OtherSkill.id == skill_id).first()
    if db_skill:
        for key, value in skill_data.items():
            setattr(db_skill, key, value)
        db.commit()
        db.refresh(db_skill)
    return db_skill

def delete_other_skill(db: Session, skill_id: UUID) -> bool:
    """Soft delete an other skill"""
    db_skill = db.query(OtherSkill).filter(OtherSkill.id == skill_id).first()
    if db_skill:
        db_skill.state_code = 1
        db_skill.status_code = 2
        db.commit()
        return True
    return False

# =====================================================
# Experience CRUD
# =====================================================
def get_experiences(db: Session) -> List[Experience]:
    """Get all active experiences ordered by creation date descending"""
    return db.query(Experience).filter(Experience.state_code == 0).order_by(Experience.created_on.desc()).all()

def get_experience(db: Session, experience_id: UUID) -> Optional[Experience]:
    """Get a specific experience by ID"""
    return db.query(Experience).filter(Experience.id == experience_id).first()

def create_experience(db: Session, experience_data: dict, duties: List[str] = None, domains: List[str] = None) -> Experience:
    """Create a new experience with duties and domains"""
    # Extract duties and domains from data if present
    duties = duties or experience_data.pop('duties', [])
    domains = domains or experience_data.pop('domains', [])
    
    db_experience = Experience(**experience_data)
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    
    # Add duties
    for duty_desc in duties:
        db_duty = ExperienceDuty(description=duty_desc, experience_id=db_experience.id)
        db.add(db_duty)
    
    # Add domains
    for domain_name in domains:
        db_domain = ExperienceDomain(name=domain_name, experience_id=db_experience.id)
        db.add(db_domain)
    
    db.commit()
    db.refresh(db_experience)
    return db_experience

def update_experience(db: Session, experience_id: UUID, experience_data: dict) -> Optional[Experience]:
    """Update an existing experience along with duties and domains"""
    db_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if db_experience:
        # Update main fields
        for key, value in experience_data.items():
            if key not in ['duties', 'domains']:
                setattr(db_experience, key, value)
        
        # Update duties if provided
        if 'duties' in experience_data:
            # Delete old duties
            db.query(ExperienceDuty).filter(ExperienceDuty.experience_id == experience_id).delete()
            # Add new duties
            for duty_desc in experience_data['duties']:
                db_duty = ExperienceDuty(description=duty_desc, experience_id=experience_id)
                db.add(db_duty)
        
        # Update domains if provided
        if 'domains' in experience_data:
            # Delete old domains
            db.query(ExperienceDomain).filter(ExperienceDomain.experience_id == experience_id).delete()
            # Add new domains
            for domain_name in experience_data['domains']:
                db_domain = ExperienceDomain(name=domain_name, experience_id=experience_id)
                db.add(db_domain)
                
        db.commit()
        db.refresh(db_experience)
    return db_experience

def delete_experience(db: Session, experience_id: UUID) -> bool:
    """Soft delete an experience"""
    db_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if db_experience:
        db_experience.state_code = 1
        db_experience.status_code = 2
        db.commit()
        return True
    return False

# =====================================================
# Education CRUD
# =====================================================
def get_educations(db: Session) -> List[Education]:
    """Get all active educations"""
    return db.query(Education).filter(Education.state_code == 0).all()

def get_education(db: Session, education_id: UUID) -> Optional[Education]:
    """Get a specific education by ID"""
    return db.query(Education).filter(Education.id == education_id).first()

def create_education(db: Session, education_data: dict) -> Education:
    """Create a new education"""
    db_education = Education(**education_data)
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education

def update_education(db: Session, education_id: UUID, education_data: dict) -> Optional[Education]:
    """Update an existing education"""
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if db_education:
        for key, value in education_data.items():
            setattr(db_education, key, value)
        db.commit()
        db.refresh(db_education)
    return db_education

def delete_education(db: Session, education_id: UUID) -> bool:
    """Soft delete an education"""
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if db_education:
        db_education.state_code = 1
        db_education.status_code = 2
        db.commit()
        return True
    return False

def bulk_replace_cv_data(db: Session, extraction: dict):
    """Replace all active CV data with new extraction data"""
    
    # 1. Update/Create Profile
    if extraction.get('profile'):
        existing_profile = db.query(Profile).filter(Profile.state_code == 0).first()
        if existing_profile:
            # Update
            for key, value in extraction['profile'].items():
                if value is not None:
                    setattr(existing_profile, key, value)
        else:
            db_profile = Profile(**extraction['profile'])
            db.add(db_profile)

    # 2. Replace Experiences (Soft delete existing)
    if 'experiences' in extraction and extraction['experiences']:
        db.query(Experience).filter(Experience.state_code == 0).update(
            {Experience.state_code: 1, Experience.status_code: 2}, 
            synchronize_session=False
        )
        for exp_data in extraction['experiences']:
            create_experience(db, exp_data)

    # 3. Replace Educations
    if 'educations' in extraction and extraction['educations']:
        db.query(Education).filter(Education.state_code == 0).update(
            {Education.state_code: 1, Education.status_code: 2}, 
            synchronize_session=False
        )
        for edu_data in extraction['educations']:
            create_education(db, edu_data)

    # 4. Replace Skill Categories and Skills
    if 'skill_categories' in extraction and extraction['skill_categories']:
        # Deactivate all skills and categories
        db.query(Skill).filter(Skill.state_code == 0).update(
            {Skill.state_code: 1, Skill.status_code: 2}, 
            synchronize_session=False
        )
        db.query(SkillCategory).filter(SkillCategory.state_code == 0).update(
            {SkillCategory.state_code: 1, SkillCategory.status_code: 2}, 
            synchronize_session=False
        )
        for i, cat_data in enumerate(extraction['skill_categories']):
            db_category = SkillCategory(name=cat_data['category_name'], display_order=i)
            db.add(db_category)
            db.flush() # Get ID
            for skill_name in cat_data['skills']:
                db_skill = Skill(name=skill_name, category_id=db_category.id)
                db.add(db_skill)

    # 5. Replace Other Skills
    if 'other_skills' in extraction and extraction['other_skills']:
        db.query(OtherSkill).filter(OtherSkill.state_code == 0).update(
            {OtherSkill.state_code: 1, OtherSkill.status_code: 2}, 
            synchronize_session=False
        )
        for os_name in extraction['other_skills']:
            db_other_skill = OtherSkill(name=os_name)
            db.add(db_other_skill)
    
    db.commit()
    return True
