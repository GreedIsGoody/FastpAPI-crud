import logging
from src.db.models import User
from .schemas import UserCreateModel
from .utils import generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

logger = logging.getLogger(__name__)

class UserService:
    async def get_user_by_email(self,email: str, session: AsyncSession):
        logger.info('Attempt to  getting a user by email {email}')
        statement = select(User).where(User.email == email )
        
        result = await session.exec(statement)
        
        user = result.first()
        
        logger.info('Successfully getting a user by email {email}')
        return user
    
    async def user_exists(self,email, session:AsyncSession):
        user = await self.get_user_by_email(email, session)
        
        return True if user is not None else False
        
    async def create_user(self, user_data:UserCreateModel,session:AsyncSession):
        logger.info('Attempt to  getting a create a user')
        user_data_dict = user_data.model_dump()
        
        new_user = User(
            **user_data_dict
        )
        
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        new_user.role = "user"
        
        session.add(new_user)
        
        await session.commit()
        
        logger.info('Succesfully attempt to create a user')
        return new_user
    
    