from fastapi import Depends, HTTPException, status,Depends
from sqlalchemy.orm import Session
from ..core.JWT_token import SECRET_KEY,ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from ..core.database import get_db
from ..models import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    #Query that get user from database
    user = db.query(models.user_data).filter(models.user_data.email == username).first()
    if user is None:
        raise credentials_exception
    return user