
from .. import models,hashing
from fastapi import HTTPException,status

def add_user(request,db):
    new_user=models.user_data(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(id,db):
    user=db.query(models.user_data).filter(models.user_data.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No user found with id {id}')
    return user