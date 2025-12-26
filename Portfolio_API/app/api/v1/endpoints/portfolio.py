from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.crud import crud
from app.schemas import schemas

router = APIRouter()

# =====================================================
# Profile Endpoints
# =====================================================
@router.get("/profile", response_model=schemas.Profile, summary="Get Profile")
def read_profile(db: Session = Depends(get_db)):
    """Get the active portfolio profile"""
    db_profile = crud.get_profile(db)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.post("/profile", response_model=schemas.Profile, status_code=status.HTTP_201_CREATED, summary="Create Profile")
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    """Create a new portfolio profile"""
    return crud.create_profile(db, profile.model_dump())

@router.put("/profile/{profile_id}", response_model=schemas.Profile, summary="Update Profile")
def update_profile(profile_id: UUID, profile: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    """Update an existing profile"""
    db_profile = crud.update_profile(db, profile_id, profile.model_dump(exclude_unset=True))
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.delete("/profile/{profile_id}", response_model=schemas.MessageResponse, summary="Delete Profile")
def delete_profile(profile_id: UUID, db: Session = Depends(get_db)):
    """Soft delete a profile"""
    success = crud.delete_profile(db, profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully", "success": True}

# =====================================================
# Skill Category Endpoints
# =====================================================
@router.get("/skills/categories", response_model=List[schemas.SkillCategory], summary="Get Skill Categories")
def read_skill_categories(include_inactive: bool = False, db: Session = Depends(get_db)):
    """Get all skill categories with their skills"""
    return crud.get_skill_categories(db, include_inactive)

@router.get("/skills/categories/{category_id}", response_model=schemas.SkillCategory, summary="Get Skill Category")
def read_skill_category(category_id: UUID, db: Session = Depends(get_db)):
    """Get a specific skill category by ID"""
    db_category = crud.get_skill_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Skill category not found")
    return db_category

@router.post("/skills/categories", response_model=schemas.SkillCategory, status_code=status.HTTP_201_CREATED, summary="Create Skill Category")
def create_skill_category(category: schemas.SkillCategoryCreate, db: Session = Depends(get_db)):
    """Create a new skill category"""
    return crud.create_skill_category(db, category.model_dump())

@router.put("/skills/categories/{category_id}", response_model=schemas.SkillCategory, summary="Update Skill Category")
def update_skill_category(category_id: UUID, category: schemas.SkillCategoryUpdate, db: Session = Depends(get_db)):
    """Update an existing skill category"""
    db_category = crud.update_skill_category(db, category_id, category.model_dump(exclude_unset=True))
    if not db_category:
        raise HTTPException(status_code=404, detail="Skill category not found")
    return db_category

@router.delete("/skills/categories/{category_id}", response_model=schemas.MessageResponse, summary="Delete Skill Category")
def delete_skill_category(category_id: UUID, db: Session = Depends(get_db)):
    """Soft delete a skill category"""
    success = crud.delete_skill_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill category not found")
    return {"message": "Skill category deleted successfully", "success": True}

# =====================================================
# Skill Endpoints
# =====================================================
@router.get("/skills", response_model=List[schemas.Skill], summary="Get Skills")
def read_skills(category_id: UUID = None, db: Session = Depends(get_db)):
    """Get all skills, optionally filtered by category"""
    return crud.get_skills(db, category_id)

@router.post("/skills", response_model=schemas.Skill, status_code=status.HTTP_201_CREATED, summary="Create Skill")
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    """Create a new skill"""
    return crud.create_skill(db, skill.model_dump())

@router.delete("/skills/{skill_id}", response_model=schemas.MessageResponse, summary="Delete Skill")
def delete_skill(skill_id: UUID, db: Session = Depends(get_db)):
    """Soft delete a skill"""
    success = crud.delete_skill(db, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"message": "Skill deleted successfully", "success": True}

# =====================================================
# Other Skill Endpoints
# =====================================================
@router.get("/other-skills", response_model=List[schemas.OtherSkill], summary="Get Other Skills")
def read_other_skills(db: Session = Depends(get_db)):
    """Get all other skills"""
    return crud.get_other_skills(db)

@router.post("/other-skills", response_model=schemas.OtherSkill, status_code=status.HTTP_201_CREATED, summary="Create Other Skill")
def create_other_skill(skill: schemas.OtherSkillCreate, db: Session = Depends(get_db)):
    """Create a new other skill"""
    return crud.create_other_skill(db, skill.model_dump())

@router.put("/other-skills/{skill_id}", response_model=schemas.OtherSkill, summary="Update Other Skill")
def update_other_skill(skill_id: UUID, skill: schemas.OtherSkillUpdate, db: Session = Depends(get_db)):
    """Update an existing other skill"""
    db_skill = crud.update_other_skill(db, skill_id, skill.model_dump(exclude_unset=True))
    if not db_skill:
        raise HTTPException(status_code=404, detail="Other skill not found")
    return db_skill

@router.delete("/other-skills/{skill_id}", response_model=schemas.MessageResponse, summary="Delete Other Skill")
def delete_other_skill(skill_id: UUID, db: Session = Depends(get_db)):
    """Soft delete an other skill"""
    success = crud.delete_other_skill(db, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Other skill not found")
    return {"message": "Other skill deleted successfully", "success": True}

# =====================================================
# Experience Endpoints
# =====================================================
@router.get("/experience", response_model=List[schemas.Experience], summary="Get Experiences")
def read_experiences(db: Session = Depends(get_db)):
    """Get all work experiences"""
    return crud.get_experiences(db)

@router.get("/experience/{experience_id}", response_model=schemas.Experience, summary="Get Experience")
def read_experience(experience_id: UUID, db: Session = Depends(get_db)):
    """Get a specific experience by ID"""
    db_experience = crud.get_experience(db, experience_id)
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return db_experience

@router.post("/experience", response_model=schemas.Experience, status_code=status.HTTP_201_CREATED, summary="Create Experience")
def create_experience(experience: schemas.ExperienceCreate, db: Session = Depends(get_db)):
    """Create a new work experience"""
    experience_dict = experience.model_dump()
    duties = experience_dict.pop('duties', [])
    domains = experience_dict.pop('domains', [])
    return crud.create_experience(db, experience_dict, duties, domains)

@router.put("/experience/{experience_id}", response_model=schemas.Experience, summary="Update Experience")
def update_experience(experience_id: UUID, experience: schemas.ExperienceUpdate, db: Session = Depends(get_db)):
    """Update an existing experience"""
    db_experience = crud.update_experience(db, experience_id, experience.model_dump(exclude_unset=True))
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return db_experience

@router.delete("/experience/{experience_id}", response_model=schemas.MessageResponse, summary="Delete Experience")
def delete_experience(experience_id: UUID, db: Session = Depends(get_db)):
    """Soft delete an experience"""
    success = crud.delete_experience(db, experience_id)
    if not success:
        raise HTTPException(status_code=404, detail="Experience not found")
    return {"message": "Experience deleted successfully", "success": True}

# =====================================================
# Education Endpoints
# =====================================================
@router.get("/education", response_model=List[schemas.Education], summary="Get Educations")
def read_educations(db: Session = Depends(get_db)):
    """Get all education entries"""
    return crud.get_educations(db)

@router.get("/education/{education_id}", response_model=schemas.Education, summary="Get Education")
def read_education(education_id: UUID, db: Session = Depends(get_db)):
    """Get a specific education by ID"""
    db_education = crud.get_education(db, education_id)
    if not db_education:
        raise HTTPException(status_code=404, detail="Education not found")
    return db_education

@router.post("/education", response_model=schemas.Education, status_code=status.HTTP_201_CREATED, summary="Create Education")
def create_education(education: schemas.EducationCreate, db: Session = Depends(get_db)):
    """Create a new education entry"""
    return crud.create_education(db, education.model_dump())

@router.put("/education/{education_id}", response_model=schemas.Education, summary="Update Education")
def update_education(education_id: UUID, education: schemas.EducationUpdate, db: Session = Depends(get_db)):
    """Update an existing education"""
    db_education = crud.update_education(db, education_id, education.model_dump(exclude_unset=True))
    if not db_education:
        raise HTTPException(status_code=404, detail="Education not found")
    return db_education

@router.delete("/education/{education_id}", response_model=schemas.MessageResponse, summary="Delete Education")
def delete_education(education_id: UUID, db: Session = Depends(get_db)):
    """Soft delete an education"""
    success = crud.delete_education(db, education_id)
    if not success:
        raise HTTPException(status_code=404, detail="Education not found")
    return {"message": "Education deleted successfully", "success": True}
