import uuid
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import BookModel, BookUpdateModel, BookCreateModel, BookDetailModel
from src.db.main import get_session
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))

@book_router.get('/', response_model=List[BookModel], dependencies=[role_checker])
async def get_all_books(
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
    ) -> list:
    
    books = await book_service.get_all_books(session)
    return books
@book_router.get('/user/{user_uid}', response_model=List[BookModel], dependencies=[role_checker])
async def get_user_book(
    user_uid: str,
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
    ) -> list:
    
    books = await book_service.get_user_books(user_uid,session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookModel, dependencies=[role_checker])
async def create_book(
    book_data: BookCreateModel, 
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
    ) -> dict:
    user_id = token_details.get('user')['user_uid']
    new_book = await book_service.create_books(book_data,user_id, session)
    return new_book


@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(
    book_uid: uuid.UUID, 
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
    ) -> BookModel:
    book = await book_service.get_books(book_uid, session)
    
    if book is not None:
        return book
    else:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
@book_router.patch("/{book_uid}", response_model=BookModel, dependencies=[role_checker])
async def update_book(
    book_uid: uuid.UUID, 
    book_update_data: BookUpdateModel, 
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
    ) -> BookModel:
   
   updated_book = await book_service.update_books(book_uid, book_update_data, session)
   
   if updated_book:
       return updated_book
   else:
       raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")
   
   
@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(
    book_uid: uuid.UUID, 
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
    ):
    book_to_delete = await book_service.delete_books(book_uid, session)
    
    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")