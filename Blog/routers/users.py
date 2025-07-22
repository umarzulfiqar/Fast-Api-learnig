from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import scheme,database,models,hashing

router=APIRouter(
    prefix="/User",
    tags=['User']
)

get_db=database.get_db
#adding user
@router.post('/',response_model=scheme.show_user)
def add_user(request:scheme.user,db:Session=Depends(get_db)):
    new_user=models.user_data(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#get user from db
@router.get('/{id}',response_model=scheme.show_user)
def user_data_show(id,db:Session=Depends(get_db)):
    user=db.query(models.user_data).filter(models.user_data.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No user found with id {id}')
    return user