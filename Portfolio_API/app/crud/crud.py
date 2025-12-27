from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.models.models import (
    User, Profile, SkillCategory, Skill, OtherSkill,
    Experience, ExperienceDuty, ExperienceDomain, Education
)

# =====================================================
# User CRUD
# =====================================================
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

# =====================================================
# Profile CRUD
# =====================================================
def get_profile(db: Session, user_id: UUID) -> Optional[Profile]:
    """Get the active profile for a user"""
    return db.query(Profile).filter(Profile.user_id == user_id, Profile.state_code == 0).first()

def create_profile(db: Session, profile_data: dict, user_id: UUID) -> Profile:
    """Create a new profile for a user"""
    db_profile = Profile(**profile_data, user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile_id: UUID, profile_data: dict, user_id: UUID) -> Optional[Profile]:
    """Update an existing profile belonging to a specific user"""
    db_profile = db.query(Profile).filter(Profile.id == profile_id, Profile.user_id == user_id).first()
    if db_profile:
        for key, value in profile_data.items():
            setattr(db_profile, key, value)
        db.commit()
        db.refresh(db_profile)
    return db_profile

# =====================================================
# Skill Category CRUD
# =====================================================
def get_skill_categories(db: Session, user_id: UUID, include_inactive: bool = False) -> List[SkillCategory]:
    """Get all skill categories for a user"""
    query = db.query(SkillCategory).filter(SkillCategory.user_id == user_id)
    if not include_inactive:
        query = query.filter(SkillCategory.state_code == 0)
    return query.order_by(SkillCategory.display_order).all()

def create_skill_category(db: Session, category_data: dict, user_id: UUID) -> SkillCategory:
    """Create a new skill category for a user"""
    db_category = SkillCategory(**category_data, user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# =====================================================
# Skill CRUD
# =====================================================
def get_skills(db: Session, category_id: UUID) -> List[Skill]:
    """Get all skills for a category"""
    return db.query(Skill).filter(Skill.category_id == category_id, Skill.state_code == 0).all()

def create_skill(db: Session, skill_data: dict) -> Skill:
    """Create a new skill in a category"""
    # Note: Skill is linked to Category, which belongs to User
    db_skill = Skill(**skill_data)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# =====================================================
# Other Skill CRUD
# =====================================================
def get_other_skills(db: Session, user_id: UUID) -> List[OtherSkill]:
    """Get all other skills for a user"""
    return db.query(OtherSkill).filter(OtherSkill.user_id == user_id, OtherSkill.state_code == 0).all()

def create_other_skill(db: Session, skill_data: dict, user_id: UUID) -> OtherSkill:
    """Create a new other skill for a user"""
    db_skill = OtherSkill(**skill_data, user_id=user_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# =====================================================
# Experience CRUD
# =====================================================
def get_experiences(db: Session, user_id: UUID) -> List[Experience]:
    """Get all experiences for a user"""
    return db.query(Experience).filter(Experience.user_id == user_id, Experience.state_code == 0).order_by(Experience.created_on.desc()).all()

def create_experience(db: Session, experience_data: dict, user_id: UUID) -> Experience:
    """Create a new experience for a user"""
    duties = experience_data.pop('duties', [])
    domains = experience_data.pop('domains', [])
    
    db_experience = Experience(**experience_data, user_id=user_id)
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    
    for duty_desc in duties:
        db.add(ExperienceDuty(description=duty_desc, experience_id=db_experience.id))
    
    for domain_name in domains:
        db.add(ExperienceDomain(name=domain_name, experience_id=db_experience.id))
    
    db.commit()
    db.refresh(db_experience)
    return db_experience

# =====================================================
# Education CRUD
# =====================================================
def get_educations(db: Session, user_id: UUID) -> List[Education]:
    """Get all educations for a user"""
    return db.query(Education).filter(Education.user_id == user_id, Education.state_code == 0).all()

def create_education(db: Session, education_data: dict, user_id: UUID) -> Education:
    """Create a new education for a user"""
    db_education = Education(**education_data, user_id=user_id)
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education

# =====================================================
# CV Replacement
# =====================================================
def bulk_replace_cv_data(db: Session, extraction: dict, user_id: UUID):
    """Replace all data for a specific user"""
    
    # 1. Profile
    if extraction.get('profile'):
        existing = get_profile(db, user_id)
        if existing:
            for key, val in extraction['profile'].items():
                if val is not None: setattr(existing, key, val)
        else:
            create_profile(db, extraction['profile'], user_id)

    # 2. Experiences
    db.query(Experience).filter(Experience.user_id == user_id, Experience.state_code == 0).update(
        {Experience.state_code: 1, Experience.status_code: 2}, synchronize_session=False
    )
    for exp_data in extraction.get('experiences', []):
        create_experience(db, exp_data, user_id)

    # 3. Educations
    db.query(Education).filter(Education.user_id == user_id, Education.state_code == 0).update(
        {Education.state_code: 1, Education.status_code: 2}, synchronize_session=False
    )
    for edu_data in extraction.get('educations', []):
        create_education(db, edu_data, user_id)

    # 4. Skills
    # Deactivate all skills belonging to any category of this user
    # Note: We use a subquery to avoid direct join in update() which is not always supported
    category_ids_subquery = db.query(SkillCategory.id).filter(SkillCategory.user_id == user_id).subquery()
    db.query(Skill).filter(Skill.category_id.in_(category_ids_subquery)).update(
        {Skill.state_code: 1}, synchronize_session=False
    )
    
    # Deactivate all skill categories of this user
    db.query(SkillCategory).filter(SkillCategory.user_id == user_id).update(
        {SkillCategory.state_code: 1}, synchronize_session=False
    )
    for i, cat in enumerate(extraction.get('skill_categories', [])):
        db_cat = create_skill_category(db, {"name": cat['category_name'], "display_order": i}, user_id)
        for s in cat['skills']:
            create_skill(db, {"name": s, "category_id": db_cat.id})

    # 5. Other Skills
    db.query(OtherSkill).filter(OtherSkill.user_id == user_id).update({OtherSkill.state_code: 1}, synchronize_session=False)
    for s_name in extraction.get('other_skills', []):
        create_other_skill(db, {"name": s_name}, user_id)

    db.commit()
    return True

# ... Add missing update/delete functions with user_id check ...
def update_experience(db: Session, experience_id: UUID, experience_data: dict, user_id: UUID) -> Optional[Experience]:
    db_exp = db.query(Experience).filter(Experience.id == experience_id, Experience.user_id == user_id).first()
    if db_exp:
        for key, val in experience_data.items():
            if key not in ['duties', 'domains']: setattr(db_exp, key, val)
        
        if 'duties' in experience_data:
            db.query(ExperienceDuty).filter(ExperienceDuty.experience_id == experience_id).delete()
            for d in experience_data['duties']: db.add(ExperienceDuty(description=d, experience_id=experience_id))
            
        if 'domains' in experience_data:
            db.query(ExperienceDomain).filter(ExperienceDomain.experience_id == experience_id).delete()
            for d in experience_data['domains']: db.add(ExperienceDomain(name=d, experience_id=experience_id))
        
        db.commit()
        db.refresh(db_exp)
    return db_exp

def delete_experience(db: Session, experience_id: UUID, user_id: UUID) -> bool:
    db_exp = db.query(Experience).filter(Experience.id == experience_id, Experience.user_id == user_id).first()
    if db_exp:
        db_exp.state_code = 1
        db.commit()
        return True
    return False

def update_education(db: Session, education_id: UUID, education_data: dict, user_id: UUID) -> Optional[Education]:
    db_edu = db.query(Education).filter(Education.id == education_id, Education.user_id == user_id).first()
    if db_edu:
        for key, val in education_data.items(): setattr(db_edu, key, val)
        db.commit()
        db.refresh(db_edu)
    return db_edu

def delete_education(db: Session, education_id: UUID, user_id: UUID) -> bool:
    db_edu = db.query(Education).filter(Education.id == education_id, Education.user_id == user_id).first()
    if db_edu:
        db_edu.state_code = 1
        db.commit()
        return True
    return False

def update_other_skill(db: Session, skill_id: UUID, skill_data: dict, user_id: UUID) -> Optional[OtherSkill]:
    db_skill = db.query(OtherSkill).filter(OtherSkill.id == skill_id, OtherSkill.user_id == user_id).first()
    if db_skill:
        for key, val in skill_data.items(): setattr(db_skill, key, val)
        db.commit()
        db.refresh(db_skill)
    return db_skill

def delete_other_skill(db: Session, skill_id: UUID, user_id: UUID) -> bool:
    db_skill = db.query(OtherSkill).filter(OtherSkill.id == skill_id, OtherSkill.user_id == user_id).first()
    if db_skill:
        db_skill.state_code = 1
        db.commit()
        return True
    return False

def delete_skill_category(db: Session, category_id: UUID, user_id: UUID) -> bool:
    db_cat = db.query(SkillCategory).filter(SkillCategory.id == category_id, SkillCategory.user_id == user_id).first()
    if db_cat:
        db_cat.state_code = 1
        db.commit()
        return True
    return False

def delete_skill(db: Session, skill_id: UUID, user_id: UUID) -> bool:
    # Check if skill belongs to a category owned by user
    db_skill = db.query(Skill).join(SkillCategory).filter(Skill.id == skill_id, SkillCategory.user_id == user_id).first()
    if db_skill:
        db_skill.state_code = 1
        db.commit()
        return True
    return False
