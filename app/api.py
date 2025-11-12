from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import crud, schemas
from .database import get_session

router = APIRouter()

@router.post(
    "/templates",
    response_model=schemas.BaseResponse[schemas.TemplatePublic],
    status_code=status.HTTP_201_CREATED,
    tags=["Templates"]
)
async def create_template(
    template: schemas.TemplateCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new template.
    
    - Checks if a template with this name already exists.
    - If not, creates it with version 1.
    """
    # Check if a template with this name already exists
    existing_template = await crud.get_template_by_name(
        db, name=template.name, language=template.language
    )
    if existing_template:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Template with name '{template.name}' and language '{template.language}' already exists."
        )
    
    # Create the new template
    new_template = await crud.create_template(db=db, template=template)
    
    return schemas.BaseResponse(
        success=True,
        message="Template created successfully.",
        data=new_template
    )

@router.get(
    "/templates/{name}",
    response_model=schemas.BaseResponse[schemas.TemplatePublic],
    status_code=status.HTTP_200_OK,
    tags=["Templates"]
)
async def get_latest_template(
    name: str,
    language: str = "en",
    db: AsyncSession = Depends(get_session)
):
    """
    Get the *latest version* of a template by its unique name.
    
    - This is the main endpoint your teammates will use.
    - We will add caching to this later to make it fast.
    """
    template = await crud.get_template_by_name(db, name=name, language=language)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with name '{name}' and language '{language}' not found."
        )
        
    return schemas.BaseResponse(
        success=True,
        message="Template retrieved successfully.",
        data=template
    )

@router.put(
    "/templates/{name}",
    response_model=schemas.BaseResponse[schemas.TemplatePublic],
    status_code=status.HTTP_200_OK,
    tags=["Templates"]
)
async def update_template(
    name: str,
    template_update: schemas.TemplateUpdate,
    language: str = "en",
    db: AsyncSession = Depends(get_session)
):
    """
    Update a template by creating a new version.
    
    - Fulfills the "version history" requirement.
    - It finds the latest version.
    - It creates a *new row* in the database with (version + 1).
    """
    # Find the latest version of the template
    latest_template = await crud.get_template_by_name(db, name=name, language=language)
    
    if not latest_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with name '{name}' and language '{language}' not found. Cannot update."
        )
    
    # Create a new version
    new_version = await crud.create_new_template_version(
        db=db,
        latest_template=latest_template,
        template_update=template_update
    )
    
    # TODO: Invalidate the cache for this template
    
    return schemas.BaseResponse(
        success=True,
        message=f"Template updated to version {new_version.version} successfully.",
        data=new_version
    )