from fastapi import APIRouter,status,Depends,Response,HTTPException
from sqlalchemy.orm import Session
from .. import scheme,models,database
from ..actions import blog_actions
from . import oauth2

get_db=database.get_db

router=APIRouter(
    prefix="/blog",
    tags=['Blog']
)



#add data 
@router.post('/',status_code=status.HTTP_201_CREATED)
def create_blog(request:scheme.Blog,db:Session=Depends(get_db),current_user:scheme.user=Depends(oauth2.get_current_user)):
    return blog_actions.create_blog(request,db)

#read data
@router.get('/',response_model=list[scheme.show_blog])
def read_blog(db:Session=Depends(get_db),current_user:scheme.user=Depends(oauth2.get_current_user)):
    return blog_actions.read_blog(db)

@router.get('/{id}',response_model=scheme.show_blog)
def read_with_id(response:Response,id,db:Session=Depends(get_db),current_user:scheme.user=Depends(oauth2.get_current_user)):
    return blog_actions.read_blog_with_id(db,id)


#updata data
@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:scheme.Blog,db:Session=Depends(get_db),current_user:scheme.user=Depends(oauth2.get_current_user)):
    return blog_actions.update_blog(id,db,request)

#delete data
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db:Session=Depends(get_db),current_user:scheme.user=Depends(oauth2.get_current_user)):
    return blog_actions.delete_blog(db,id)