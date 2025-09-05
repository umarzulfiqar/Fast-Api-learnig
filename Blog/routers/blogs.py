from fastapi import APIRouter,status,Depends,Response,HTTPException
from sqlalchemy.orm import Session
from schemas import scheme
from models import models
from core import database
from api import oauth2
from core import hashing
from uuid import UUID



get_db=database.get_db

router=APIRouter(tags=['User'])



#add data 
@router.post('/blog',status_code=status.HTTP_201_CREATED)
def create_blog(request:scheme.Blog,db:Session=Depends(get_db),current_user:scheme.user=Depends(oauth2.get_current_user)):
    new_blog=models.blog_data(title=request.title,body=request.body,user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#read data
@router.get('/blog',response_model=list[scheme.show_blog])
def read_blog(db:Session=Depends(get_db),current_user:scheme.user=Depends(oauth2.get_current_user)):
    blogs=db.query(models.blog_data).all()
    return blogs


@router.get('/blog/{id}',response_model=scheme.show_blog)
def read_with_id(response:Response, id: int, db:Session=Depends(get_db), current_user:scheme.user=Depends(oauth2.get_current_user)):
    blogs=db.query(models.blog_data).filter(models.blog_data.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Response with id {id} not found')
    #     response.status_code=status.HTTP_404_NOT_FOUND
    #     return {'detail':f'Response with id {id} not found'}
    return blogs


#updata data
@router.put('/bog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request:scheme.Blog, db:Session=Depends(get_db), current_user:scheme.user=Depends(oauth2.get_current_user)):
    blog=db.query(models.blog_data).filter(models.blog_data.id==id)
    if not blog.first():
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog not found with id {id}")
    blog.update(request.model_dump(), synchronize_session=False)
    db.commit()
    return "UPDATED"

#delete data
@router.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db:Session=Depends(get_db), current_user:scheme.user=Depends(oauth2.get_current_user)):
    blog=db.query(models.blog_data).filter(models.blog_data.id==id)
    if  not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog not found with id {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return blog

#add comment
@router.post('/blog/{id}/comment')
def add_comment(id:UUID,request:scheme.comment , db: Session = Depends(get_db), current_user: scheme.user = Depends(oauth2.get_current_user)):
    new_comment = models.Comment(blog_id=id,content=request.content,user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

#login user user
@router.post('/user',response_model=scheme.show_user)
def add_user(request:scheme.user,db:Session=Depends(get_db)):
    new_user=models.user_data(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#show user
@router.get('/user/{id}',response_model=scheme.show_user)
def user_data_show(id,db:Session=Depends(get_db)):
    user=db.query(models.user_data).filter(models.user_data.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No user found with id {id}')
    return user