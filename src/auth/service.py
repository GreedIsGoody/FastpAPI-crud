from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

class UserService:
    async def get_user_by_email(email: str, session: AsyncSession):
        statement = select(User).where(User.email == email )
        
        result = await session.exec(statement)
        
        user = result.first()
        
        return user
    
    async def user_exists(email, session:AsyncSession):
        pass