from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# =====================================================
# Skill Schemas
# =====================================================
class SkillBase(BaseSchema):
    name: str

class SkillCreate(SkillBase):
    category_id: UUID

class SkillUpdate(BaseSchema):
    name: Optional[str] = None
    category_id: Optional[UUID] = None

class Skill(SkillBase):
    id: UUID
    category_id: UUID
    state_code: int = 0
    status_code: int = 1
    created_on: datetime
    modified_on: datetime

class SkillCategoryBase(BaseSchema):
    name: str
    display_order: int = 0

class SkillCategoryCreate(SkillCategoryBase):
    pass

class SkillCategoryUpdate(BaseSchema):
    name: Optional[str] = None
    display_order: Optional[int] = None

class SkillCategory(SkillCategoryBase):
    id: UUID
    skills: List[Skill] = []
    state_code: int = 0
    status_code: int = 1
    created_on: datetime
    modified_on: datetime

# =====================================================
# Other Skills Schemas
# =====================================================
class OtherSkillBase(BaseSchema):
    name: str

class OtherSkillCreate(OtherSkillBase):
    pass

class OtherSkillUpdate(BaseSchema):
    name: Optional[str] = None

class OtherSkill(OtherSkillBase):
    id: UUID
    state_code: int = 0
    status_code: int = 1
    created_on: datetime
    modified_on: datetime

# =====================================================
# Experience Schemas
# =====================================================
class ExperienceDutyBase(BaseSchema):
    description: str

class ExperienceDuty(ExperienceDutyBase):
    id: UUID

class ExperienceDomainBase(BaseSchema):
    name: str

class ExperienceDomain(ExperienceDomainBase):
    id: UUID

class ExperienceBase(BaseSchema):
    company_name: str
    role: str
    period_display: str
    tech_stack: str

class ExperienceCreate(ExperienceBase):
    duties: List[str] = []
    domains: List[str] = []

class ExperienceUpdate(BaseSchema):
    company_name: Optional[str] = None
    role: Optional[str] = None
    period_display: Optional[str] = None
    tech_stack: Optional[str] = None
    duties: Optional[List[str]] = None
    domains: Optional[List[str]] = None

class Experience(ExperienceBase):
    id: UUID
    duties: List[ExperienceDuty] = []
    domains: List[ExperienceDomain] = []
    state_code: int = 0
    status_code: int = 1
    created_on: datetime
    modified_on: datetime

# =====================================================
# Education Schemas
# =====================================================
class EducationBase(BaseSchema):
    school: str
    degree: str
    major: str
    education_year: Optional[str] = None

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseSchema):
    school: Optional[str] = None
    degree: Optional[str] = None
    major: Optional[str] = None
    education_year: Optional[str] = None

class Education(EducationBase):
    id: UUID
    state_code: int = 0
    status_code: int = 1
    created_on: datetime
    modified_on: datetime

# =====================================================
# Profile Schemas
# =====================================================
class ProfileBase(BaseSchema):
    name: str
    role: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    skype: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    profile_image_url: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseSchema):
    name: Optional[str] = None
    role: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    skype: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    profile_image_url: Optional[str] = None

class Profile(ProfileBase):
    id: UUID
    state_code: int = 0
    status_code: int = 1
    created_on: datetime
    modified_on: datetime

# =====================================================
# CV Extraction Schemas
# =====================================================
class SkillCategoryExtraction(BaseSchema):
    category_name: str
    skills: List[str]

class CVExtractionResponse(BaseSchema):
    profile: Optional[ProfileCreate] = None
    experiences: List[ExperienceCreate] = []
    educations: List[EducationCreate] = []
    skill_categories: List[SkillCategoryExtraction] = []
    other_skills: List[str] = []

# =====================================================
# Response Schemas
# =====================================================
class MessageResponse(BaseSchema):
    message: str
    success: bool = True
