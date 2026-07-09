import logging
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc, delete
from src.db.models import BookModel
from datetime import datetime


logger = logging.getLogger(__name__)

class BookService:
    async def get_all_books(self, session: AsyncSession):
        logger.info(f"Attempt to get all books from Database")
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = await session.exec(statement)
        logger.info(f"Successfull receiving a {len(result.all())} books from Database")
        return result.all()
    
    async def get_user_books(self, user_uid: str, session: AsyncSession):
        logger.info(f"Attempt to get all books of user with uid {user_uid} from Database")
        statement = select(BookModel).where(BookModel.user_uid == user_uid).order_by(desc(BookModel.created_at))
        result = await session.exec(statement)
        
        return result.all()
    
    async def get_book(self, book_uid:uuid.UUID, session: AsyncSession):
        logger.info(f"Attempt to get book with {book_uid} from Database")   
        statement = select(BookModel).where(BookModel.uid == book_uid)
        
        result = await session.exec(statement)
        
        book = result.first()
        logger.info(f"Successfull receiving a book {book_uid} from Database")
        return book if book is not None else None
     
    async def create_books(self,book_data:BookCreateModel, user_uid:str, session: AsyncSession):
        logger.info(f"Attempt to create book by user {user_uid} from Database")   
        book_data_dict = book_data.model_dump()
        
        new_book = BookModel(
            **book_data_dict
        )
        new_book.user_uid = user_uid
        
        
        
        session.add(new_book)
        
        await session.commit()
        await session.refresh(new_book)
        logger.info(f"Successfull creating a book by user {user_uid} for Database")
        return new_book
    
    async def update_books(self, book_uid:uuid.UUID, update_data:BookUpdateModel, session: AsyncSession):
        logger.info(f"Attempt to update book with uuid {book_uid} from Database")   
        book_to_update = await self.get_books(book_uid, session)

        if book_to_update is not None:
        
            update_data_dict = update_data.model_dump()
        
            for key, value in update_data_dict.items():
                setattr(book_to_update, key, value)
                
            await session.commit()
            await session.refresh(book_to_update)
            logger.info(f"Successfully to update book with uuid {book_uid} from Database")  
            return book_to_update
        
    async def delete_books(self, book_uid:uuid.UUID, session: AsyncSession):
        logger.info(f"Attempt to delete book with uuid {book_uid}from Database")
        book_to_delete = await self.get_books(book_uid, session)
        
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            
            await session.commit()
            logger.info(f"Successfully deletiting book with {book_uid} from Database")
            return {}
        else:
            return None