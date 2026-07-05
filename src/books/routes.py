import uuid
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import BookModel, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.auth.dependencies import AccessTokenBearer

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()

@book_router.get('/', response_model=List[BookModel])
async def get_all_books(session:AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)) -> list:
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def create_book(book_data: BookCreateModel, session:AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)) -> dict:
    new_book = await book_service.create_books(book_data, session)
    return new_book


@book_router.get("/{book_uid}")
async def get_book(book_uid: uuid.UUID, session:AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)) -> BookModel:
    book = await book_service.get_books(book_uid, session)
    
    if book is not None:
        return book
    else:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
@book_router.patch("/{book_uid}")
async def update_book(book_uid: uuid.UUID, book_update_data: BookUpdateModel, session:AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)) -> BookModel:
   
   updated_book = await book_service.update_books(book_uid, book_update_data, session)
   
   if updated_book:
       return updated_book
   else:
       raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")
   
   
@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: uuid.UUID, session:AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    book_to_delete = await book_service.delete_books(book_uid, session)
    
    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")