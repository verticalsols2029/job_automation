from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, Profile, ApplicationPreferences, Experience, Project, Education, Skill
from app.schemas.user import (
    UserFull, ProfileCreate, 
    Profile as ProfileSchema, ApplicationPreferencesCreate, 
    ApplicationPreferences as PreferencesSchema,
    ExperienceCreate, Experience as ExperienceSchema,
    ProjectCreate, Project as ProjectSchema,
    EducationCreate, Education as EducationSchema,
    SkillCreate, Skill as SkillSchema
)

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserFull)
async def get_user_profile(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    # Eagerly load all relationships to prevent async lazy-loading crashes
    query = select(User).where(User.id == current_user.id).options(
        selectinload(User.profile),
        selectinload(User.experience),
        selectinload(User.projects),
        selectinload(User.education),
        selectinload(User.skills),
        selectinload(User.preferences)
    )
    
    result = await db.execute(query)
    user_data = result.scalar_one_or_none()
    
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return user_data


@router.patch("/basics", response_model=ProfileSchema)
async def upsert_profile_basics(
    profile_in: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Profile).where(Profile.user_id == current_user.id)
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if profile:
        update_data = profile_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(profile, key, value)
    else:
        profile = Profile(**profile_in.model_dump(), user_id=current_user.id)
        db.add(profile)

    await db.commit()
    await db.refresh(profile)
    return profile


@router.patch("/preferences", response_model=PreferencesSchema)
async def upsert_preferences(
    prefs_in: ApplicationPreferencesCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(ApplicationPreferences).where(ApplicationPreferences.user_id == current_user.id)
    result = await db.execute(query)
    preferences = result.scalar_one_or_none()

    if preferences:
        # Update existing
        update_data = prefs_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(preferences, key, value)
    else:
        # Create new
        preferences = ApplicationPreferences(**prefs_in.model_dump(), user_id=current_user.id)
        db.add(preferences)

    await db.commit()
    await db.refresh(preferences)
    return preferences


# --- EXPERIENCE ---

@router.post("/experience", response_model=ExperienceSchema)
async def add_experience(
    item_in: ExperienceCreate, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    new_item = Experience(**item_in.model_dump(), user_id=current_user.id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.patch("/experience/{item_id}", response_model=ExperienceSchema)
async def update_experience(
    item_id: UUID,
    item_in: ExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Experience).where(Experience.id == item_id, Experience.user_id == current_user.id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
        
    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
        
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/experience/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    item_id: UUID, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    query = select(Experience).where(Experience.id == item_id, Experience.user_id == current_user.id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
        
    await db.delete(item)
    await db.commit()


# --- PROJECTS ---

@router.post("/projects", response_model=ProjectSchema)
async def add_project(
    item_in: ProjectCreate, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    new_item = Project(**item_in.model_dump(), user_id=current_user.id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.patch("/projects/{item_id}", response_model=ProjectSchema)
async def update_project(
    item_id: UUID,
    item_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Project).where(Project.id == item_id, Project.user_id == current_user.id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
        
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/projects/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    item_id: UUID, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    query = select(Project).where(Project.id == item_id, Project.user_id == current_user.id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
    await db.delete(item)
    await db.commit()


# --- EDUCATION ---

@router.post("/education", response_model=EducationSchema)
async def add_education(
    item_in: EducationCreate, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    new_item = Education(**item_in.model_dump(), user_id=current_user.id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.patch("/education/{item_id}", response_model=EducationSchema)
async def update_education(
    item_id: UUID,
    item_in: EducationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Education).where(Education.id == item_id, Education.user_id == current_user.id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")
        
    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
        
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/education/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    item_id: UUID, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    query = select(Education).where(Education.id == item_id, Education.user_id == current_user.id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")
        
    await db.delete(item)
    await db.commit()


# --- SKILLS ---

@router.post("/skills", response_model=SkillSchema)
async def add_skill(
    item_in: SkillCreate, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    new_item = Skill(**item_in.model_dump(), user_id=current_user.id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.patch("/skills/{item_id}", response_model=SkillSchema)
async def update_skill(
    item_id: UUID,
    item_in: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Skill).where(Skill.id == item_id, Skill.user_id == current_user.id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
        
    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
        
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/skills/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    item_id: UUID, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    query = select(Skill).where(Skill.id == item_id, Skill.user_id == current_user.id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
        
    await db.delete(item)
    await db.commit()