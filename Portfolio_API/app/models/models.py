import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class DataverseMixin:
    """Dataverse-compatible audit fields"""
    created_on = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    modified_on = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    state_code = Column(Integer, default=0, nullable=False)  # 0: Active, 1: Inactive
    status_code = Column(Integer, default=1, nullable=False)  # 1: Active, 2: Inactive

class User(Base, DataverseMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    google_id = Column(String(255), unique=True)
    picture_url = Column(String(500))

    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")
    experience = relationship("Experience", back_populates="user", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="user", cascade="all, delete-orphan")
    skill_categories = relationship("SkillCategory", back_populates="user", cascade="all, delete-orphan")
    other_skills = relationship("OtherSkill", back_populates="user", cascade="all, delete-orphan")

class Profile(Base, DataverseMixin):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Initially nullable for migration
    name = Column(String(255), nullable=False)
    role = Column(String(255))
    bio = Column(Text)
    email = Column(String(255))
    phone = Column(String(50))
    location = Column(String(255))
    skype = Column(String(255))
    linkedin_url = Column(String(255))
    github_url = Column(String(255))
    profile_image_url = Column(String(255))

    user = relationship("User", back_populates="profiles")

class SkillCategory(Base, DataverseMixin):
    __tablename__ = "skill_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    name = Column(String(100), nullable=False) # Removed unique=True because multiple users can have a category with same name
    display_order = Column(Integer, default=0)

    user = relationship("User", back_populates="skill_categories")
    skills = relationship("Skill", back_populates="category", cascade="all, delete-orphan")

class Skill(Base, DataverseMixin):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("skill_categories.id"))
    
    category = relationship("SkillCategory", back_populates="skills")

class OtherSkill(Base, DataverseMixin):
    __tablename__ = "other_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    name = Column(String(255), nullable=False)

    user = relationship("User", back_populates="other_skills")

class Experience(Base, DataverseMixin):
    __tablename__ = "experiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    company_name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    period_display = Column(String(100))
    tech_stack = Column(Text)
    
    user = relationship("User", back_populates="experience")
    duties = relationship("ExperienceDuty", back_populates="experience", cascade="all, delete-orphan")
    domains = relationship("ExperienceDomain", back_populates="experience", cascade="all, delete-orphan")

class ExperienceDuty(Base, DataverseMixin):
    __tablename__ = "experience_duties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(Text, nullable=False)
    experience_id = Column(UUID(as_uuid=True), ForeignKey("experiences.id"))

    experience = relationship("Experience", back_populates="duties")

class ExperienceDomain(Base, DataverseMixin):
    __tablename__ = "experience_domains"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    experience_id = Column(UUID(as_uuid=True), ForeignKey("experiences.id"))

    experience = relationship("Experience", back_populates="domains")

class Education(Base, DataverseMixin):
    __tablename__ = "educations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    school = Column(String(255), nullable=False)
    degree = Column(String(200))
    major = Column(String(200))
    education_year = Column(String(50))

    user = relationship("User", back_populates="education")
