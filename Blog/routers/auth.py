from fastapi import APIRouter,Depends,HTTPException,status
from .. import scheme,database,models
from sqlalchemy.orm import Session
from ..hashing import Hash

router=APIRouter(
    tags=(['Authentication'])
)


@router.post('/user_login')
def login(request:scheme.Login,db:Session=Depends(database.get_db)):
    user=db.query(models.user_data).filter(models.user_data.email==request.user_name).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Invalid Email")
    if not Hash.verifty(user.password,request.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Incorrect Password")

    return user