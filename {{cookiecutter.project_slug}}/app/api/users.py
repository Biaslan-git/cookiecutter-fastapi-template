"""
User API endpoints
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_user_service
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def create_user(
    user_data: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Create a new user with the following information:
    
    - **email**: valid email address
    - **username**: 3-100 characters
    - **password**: minimum 6 characters
    """
    try:
        user = await service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID"
)
async def get_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)]
):
    """Get a specific user by ID"""
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Get all users"
)
async def get_users(
    service: Annotated[UserService, Depends(get_user_service)],
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all users with pagination
    
    - **skip**: number of records to skip (default: 0)
    - **limit**: maximum number of records to return (default: 100)
    """
    users = await service.get_all_users(skip=skip, limit=limit)
    return users


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)]
):
    """Update user information"""
    try:
        user = await service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user"
)
async def delete_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)]
):
    """Delete a user by ID"""
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
