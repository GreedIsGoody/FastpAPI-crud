from fastapi import APIRouter
from .schemas import UserCreateModel

auth_router = APIRouter()

@auth_router.post("/signup")
async def create_user_Account(user_data: UserCreateModel):
    pass