"""
User business logic service
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.user import UserDAO
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """User service with business logic"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.dao = UserDAO
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """Get user by ID"""
        return await self.dao.get_by_id(self.db, user_id)
    
    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Get user by email"""
        return await self.dao.get_by_email(self.db, email)
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Get all users with pagination"""
        return await self.dao.get_all(self.db, skip=skip, limit=limit)
    
    async def create_user(self, user_data: UserCreate) -> UserModel:
        """Create new user with business logic validation"""
        
        # Проверка: email уже существует?
        existing_user = await self.dao.get_by_email(self.db, user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Проверка: username уже существует?
        existing_username = await self.dao.get_by_username(self.db, user_data.username)
        if existing_username:
            raise ValueError("User with this username already exists")
        
        # Хешируем пароль (TODO: использовать bcrypt или passlib)
        hashed_password = self._hash_password(user_data.password)
        
        # Создаём модель
        user = UserModel(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            is_active=True,
        )
        
        # Сохраняем в БД
        return await self.dao.create(self.db, user)
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserModel]:
        """Update user"""
        user = await self.dao.get_by_id(self.db, user_id)
        if not user:
            return None
        
        # Обновляем только переданные поля
        if user_data.email is not None:
            # Проверяем что новый email не занят
            existing = await self.dao.get_by_email(self.db, user_data.email)
            if existing and existing.id != user_id:
                raise ValueError("Email already taken")
            user.email = user_data.email
        
        if user_data.username is not None:
            # Проверяем что новый username не занят
            existing = await self.dao.get_by_username(self.db, user_data.username)
            if existing and existing.id != user_id:
                raise ValueError("Username already taken")
            user.username = user_data.username
        
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
        
        return await self.dao.update(self.db, user)
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        return await self.dao.delete(self.db, user_id)
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password (simplified - use bcrypt in production!)"""
        # TODO: Использовать passlib или bcrypt
        return f"hashed_{password}"
