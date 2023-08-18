from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from .config import settings
from .schemas.user_schemas import TokenData
from fastapi import Depends, HTTPException
from .database import get_db
from sqlalchemy.orm import Session
# from .models.models import User
from .models.models import User

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=settings.expires_in)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,settings.secret,algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,settings.secret,algorithms=[settings.algorithm])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    tokn = verify_access_token(token,credentials_exception)
    user = db.query(User).filter(User.id == tokn.id).first()

    return user