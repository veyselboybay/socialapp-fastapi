from fastapi import APIRouter,HTTPException,Depends
from ..schemas.user_schemas import UserCreate,UserOut
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Annotated


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup",status_code=201,response_model=UserOut)
async def create_user(user:UserCreate, db: Annotated[Session,Depends(get_db)]):
    return user