from fastapi import APIRouter, Depends, HTTPException
# from schemas.user_schemas import Token
from ..schemas.user_schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.utils import verify
from .. import oauth2
from ..models.models import User

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # check if the user exists
    user = db.query(User).filter(User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code=403,detail="Invalid Credentials")
    # check if the passwords match
    if not verify(credentials.password,user.password):
        raise HTTPException(status_code=403,detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return Token(access_token=access_token,token_type="bearer")