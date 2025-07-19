from fastapi import APIRouter,Depends,HTTPException,status
from .. import scheme,database,models,JWT_token
from sqlalchemy.orm import Session
from ..hashing import Hash


router=APIRouter(
    tags=['Authentication'],
    prefix='/login'
)


@router.post('/')
def login(request:scheme.login,db:Session=Depends(database.get_db)):
    user=db.query(models.user_data).filter(models.user_data.email==request.user_name).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Invalid Email")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Incorrect Password")
    #Generate JWT Token
    access_token = JWT_token.create_access_token(data={"sub": user.email})
    return {"access_token":access_token, "token_type":"bearer"}