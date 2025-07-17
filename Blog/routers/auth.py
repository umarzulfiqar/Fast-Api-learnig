from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from .. import scheme,database,models
from sqlalchemy.orm import Session
from ..hashing import Hash
from . import JWT_token

router=APIRouter(
    tags=(['Authentication'])
)


@router.post('/user_login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.user_data).filter(models.user_data.email==request.username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Invalid Email")
    if not Hash.verifty(user.password,request.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Incorrect Password")
    #Genrate JWT Token
    access_token =JWT_token.create_access_token(data={"sub": user.email})
    return {"access_token":access_token,"token_type":"bearer"}