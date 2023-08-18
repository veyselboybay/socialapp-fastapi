from fastapi import APIRouter,HTTPException,Depends
from ..schemas.user_schemas import UserCreate,UserOut
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from ..models.models import User
from ..utils.utils import hash


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup",status_code=201,response_model=UserOut)
async def create_user(user:UserCreate, db: Annotated[Session,Depends(get_db)]):

    hashed_pass = hash(user.password)
    user.password = hashed_pass
    new_user = User(**user.model_dump())    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 

@router.get("/{id}",status_code=200,response_model=UserOut)
async def get_user_by_id(id:int,db:Annotated[Session,Depends(get_db)]):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404,detail=f"user with {id} is not found!")
    return user