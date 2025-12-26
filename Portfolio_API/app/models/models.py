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

class Profile(Base, DataverseMixin):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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

class SkillCategory(Base, DataverseMixin):
    __tablename__ = "skill_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    display_order = Column(Integer, default=0)

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
    name = Column(String(255), nullable=False)

class Experience(Base, DataverseMixin):
    __tablename__ = "experiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    period_display = Column(String(100))
    tech_stack = Column(Text)
    
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
    school = Column(String(255), nullable=False)
    degree = Column(String(200))
    major = Column(String(200))
    education_year = Column(String(50))
