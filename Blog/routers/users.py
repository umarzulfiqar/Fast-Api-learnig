from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .. import scheme,database
from ..actions import user_actions

router=APIRouter(
    prefix="/User",
    tags=['User']
)

get_db=database.get_db
#adding user
@router.post('/',response_model=scheme.show_user)
def add_user(request:scheme.user,db:Session=Depends(get_db)):
    return user_actions.add_user(request,db)

#get user from db
@router.get('/{id}',response_model=scheme.show_user)
def user_data_show(id,db:Session=Depends(get_db)):
    return user_actions.get_user(id,db)
