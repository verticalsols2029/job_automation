from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class ExperienceBase(BaseModel):
    company: str
    role: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None


class ExperienceCreate(ExperienceBase):
    pass


class Experience(ExperienceBase):
    id: UUID
    user_id: UUID
    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    title: str
    link: Optional[str] = None
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: UUID
    user_id: UUID
    model_config = ConfigDict(from_attributes=True)


class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    summary: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: UUID
    user_id: UUID
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str # Plain text from request, will be hashed before saving


class User(UserBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Schema for full dashboard view (includes all nested data)
class UserFull(User):
    profile: Optional[Profile] = None
    experience: List[Experience] = []
    projects: List[Project] = []


class TokenRequest(BaseModel):
    refresh_token: str