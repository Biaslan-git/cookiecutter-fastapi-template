"""
Database and service dependencies
"""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.services import UserService


async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserService:
    """Get UserService instance with database session"""
    return UserService(db)
