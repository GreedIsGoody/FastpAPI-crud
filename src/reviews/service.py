from src.db.models import Reviews
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewsCreateModel
from fastapi import status
from fastapi.exceptions import HTTPException
import logging

book_service = BookService()
user_service = UserService()

class ReviewService():
    
    async def add_review_to_book(self,user_email: str, book_uid: str, review_data: ReviewsCreateModel, session: AsyncSession):
        try:
            book =  await book_service.get_books(book_uid=book_uid, session=session)
            user = await user_service.get_user_by_email(user_email, session=session)
            
            review_data_in_dict = review_data.model_dump()
            new_review = Reviews(**review_data_in_dict)
            
            
            if book is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Book was not found'
                )
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='User was not found'
                )
            
            new_review.user = user
            
            new_review.book = book
            
            session.add(new_review)
            
            await session.commit()
            
            return new_review
            
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops...Something is wrong"
            )
        