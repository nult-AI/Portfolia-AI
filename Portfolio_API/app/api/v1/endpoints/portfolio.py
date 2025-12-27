from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.crud import crud
from app.schemas import schemas
from app.api import deps
from app.models.models import User

router = APIRouter()

def get_target_user(
    user_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(deps.get_optional_user)
) -> Optional[UUID]:
    # 1. If explicit user_id provided in query
    if user_id:
        return user_id
    
    # 2. If user is logged in, show their own portfolio
    if current_user:
        return current_user.id
    
    # 3. Public mode: Fallback to the very first user created in the system
    first_user = db.query(User).first()
    if first_user:
        return first_user.id
        
    return None

# =====================================================
# Profile Endpoints
# =====================================================
@router.get("/profile", response_model=schemas.Profile, summary="Get Profile")
def read_profile(
    db: Session = Depends(get_db),
    target_user_id: UUID = Depends(get_target_user)
):
    """Get the active portfolio profile for a specific user"""
    if not target_user_id:
        raise HTTPException(status_code=404, detail="No portfolio found in the system")

    db_profile = crud.get_profile(db, target_user_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found for this user")
    return db_profile

@router.post("/profile", response_model=schemas.Profile, status_code=status.HTTP_201_CREATED, summary="Create Profile")
def create_profile(
    profile: schemas.ProfileCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new portfolio profile for the current user"""
    return crud.create_profile(db, profile.model_dump(), current_user.id)

@router.put("/profile/{profile_id}", response_model=schemas.Profile, summary="Update Profile")
def update_profile(
    profile_id: UUID, 
    profile: schemas.ProfileUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Update an existing profile belonging to the current user"""
    db_profile = crud.update_profile(db, profile_id, profile.model_dump(exclude_unset=True), current_user.id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found or access denied")
    return db_profile

# =====================================================
# Skill Category Endpoints
# =====================================================
@router.get("/skills/categories", response_model=List[schemas.SkillCategory], summary="Get Skill Categories")
def read_skill_categories(
    include_inactive: bool = False, 
    db: Session = Depends(get_db),
    target_user_id: UUID = Depends(get_target_user)
):
    if not target_user_id:
         return []
    return crud.get_skill_categories(db, target_user_id, include_inactive)

@router.post("/skills/categories", response_model=schemas.SkillCategory, status_code=status.HTTP_201_CREATED, summary="Create Skill Category")
def create_skill_category(
    category: schemas.SkillCategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return crud.create_skill_category(db, category.model_dump(), current_user.id)

# =====================================================
# Skill Endpoints
# =====================================================
@router.get("/skills", response_model=List[schemas.Skill], summary="Get Skills")
def read_skills(category_id: UUID, db: Session = Depends(get_db)):
    return crud.get_skills(db, category_id)

@router.post("/skills", response_model=schemas.Skill, status_code=status.HTTP_201_CREATED, summary="Create Skill")
def create_skill(
    skill: schemas.SkillCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user) # Auth check
):
    # Additional check: Does the category belong to the user?
    from app.models.models import SkillCategory
    cat = db.query(SkillCategory).filter(SkillCategory.id == skill.category_id, SkillCategory.user_id == current_user.id).first()
    if not cat:
        raise HTTPException(status_code=403, detail="Access denied to this category")
    return crud.create_skill(db, skill.model_dump())

@router.delete("/skills/{skill_id}", response_model=schemas.MessageResponse, summary="Delete Skill")
def delete_skill(
    skill_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    success = crud.delete_skill(db, skill_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found or access denied")
    return {"message": "Skill deleted successfully", "success": True}

# =====================================================
# Other Skill Endpoints
# =====================================================
@router.get("/other-skills", response_model=List[schemas.OtherSkill], summary="Get Other Skills")
def read_other_skills(
    db: Session = Depends(get_db),
    target_user_id: UUID = Depends(get_target_user)
):
    if not target_user_id:
         return []
    return crud.get_other_skills(db, target_user_id)

@router.post("/other-skills", response_model=schemas.OtherSkill, status_code=status.HTTP_201_CREATED, summary="Create Other Skill")
def create_other_skill(
    skill: schemas.OtherSkillCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return crud.create_other_skill(db, skill.model_dump(), current_user.id)

# =====================================================
# Experience Endpoints
# =====================================================
@router.get("/experience", response_model=List[schemas.Experience], summary="Get Experiences")
def read_experiences(
    db: Session = Depends(get_db),
    target_user_id: UUID = Depends(get_target_user)
):
    if not target_user_id:
         return []
    return crud.get_experiences(db, target_user_id)

@router.post("/experience", response_model=schemas.Experience, status_code=status.HTTP_201_CREATED, summary="Create Experience")
def create_experience(
    experience: schemas.ExperienceCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return crud.create_experience(db, experience.model_dump(), current_user.id)

@router.put("/experience/{experience_id}", response_model=schemas.Experience, summary="Update Experience")
def update_experience(
    experience_id: UUID, 
    experience: schemas.ExperienceUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    db_exp = crud.update_experience(db, experience_id, experience.model_dump(exclude_unset=True), current_user.id)
    if not db_exp:
        raise HTTPException(status_code=404, detail="Experience not found or access denied")
    return db_exp

# =====================================================
# Education Endpoints
# =====================================================
@router.get("/education", response_model=List[schemas.Education], summary="Get Educations")
def read_educations(
    db: Session = Depends(get_db),
    target_user_id: UUID = Depends(get_target_user)
):
    if not target_user_id:
         return []
    return crud.get_educations(db, target_user_id)

@router.post("/education", response_model=schemas.Education, status_code=status.HTTP_201_CREATED, summary="Create Education")
def create_education(
    education: schemas.EducationCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return crud.create_education(db, education.model_dump(), current_user.id)

@router.put("/education/{education_id}", response_model=schemas.Education, summary="Update Education")
def update_education(
    education_id: UUID, 
    education: schemas.EducationUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    db_edu = crud.update_education(db, education_id, education.model_dump(exclude_unset=True), current_user.id)
    if not db_edu:
        raise HTTPException(status_code=404, detail="Education not found or access denied")
    return db_edu
