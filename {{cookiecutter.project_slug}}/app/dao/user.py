"""
DAO operations for User model
"""
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel


class UserDAO:
    """Data Access Object for User"""
    
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[UserModel]:
        """Get user by ID"""
        result = await db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[UserModel]:
        """Get user by email"""
        result = await db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[UserModel]:
        """Get user by username"""
        result = await db.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserModel]:
        """Get all users with pagination"""
        result = await db.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def create(db: AsyncSession, user: UserModel) -> UserModel:
        """Create new user"""
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def update(db: AsyncSession, user: UserModel) -> UserModel:
        """Update existing user"""
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        """Delete user by ID"""
        user = await UserDAO.get_by_id(db, user_id)
        if not user:
            return False
        
        await db.delete(user)
        await db.commit()
        return True

