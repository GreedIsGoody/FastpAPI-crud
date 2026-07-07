import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc, delete
from .models import BookModel
from datetime import datetime

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = await session.exec(statement)
        
        return result.all()
    
    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = select(BookModel).where(BookModel.user_uid == user_uid).order_by(desc(BookModel.created_at))
        result = await session.exec(statement)
        
        return result.all()
    
    async def get_books(self, book_uid:uuid.UUID, session: AsyncSession):
        statement = select(BookModel).where(BookModel.uid == book_uid)
        
        result = await session.exec(statement)
        
        book = result.first()
        
        return book if book is not None else None
     
    async def create_books(self,book_data:BookCreateModel, user_uid:str, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        
        new_book = BookModel(
            **book_data_dict
        )
        new_book.user_uid = user_uid
        
        
        
        session.add(new_book)
        
        await session.commit()
        await session.refresh(new_book)
        return new_book
    
    async def update_books(self, book_uid:uuid.UUID, update_data:BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_books(book_uid, session)

        if book_to_update is not None:
        
            update_data_dict = update_data.model_dump()
        
            for key, value in update_data_dict.items():
                setattr(book_to_update, key, value)
                
            await session.commit()
            await session.refresh(book_to_update)
        
            return book_to_update
        
    async def delete_books(self, book_uid:uuid.UUID, session: AsyncSession):
        
        book_to_delete = await self.get_books(book_uid, session)
        
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            
            await session.commit()
            
            return {}
        else:
            return None