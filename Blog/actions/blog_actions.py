from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from .. import models,scheme

def create_blog(request:scheme.Blog,db:Session):
    new_blog=models.blog_data(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def read_blog(db:Session):
    blogs=db.query(models.blog_data).all()
    return blogs



def read_blog_with_id(db:Session,id):
    blogs=db.query(models.blog_data).filter(models.blog_data.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Response with id {id} not found')
    #     response.status_code=status.HTTP_404_NOT_FOUND
    #     return {'detail':f'Response with id {id} not found'}
    return blogs


def update_blog(id,db:Session,request:scheme.Blog):
    blog=db.query(models.blog_data).filter(models.blog_data.id==id)
    if not blog.first():
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog not found with id {id}")
    blog.update(request.model_dump(), synchronize_session=False)
    db.commit()
    return "UPDATED"

def delete_blog(db,id):
    blog=db.query(models.blog_data).filter(models.blog_data.id==id)
    if  not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog not found with id {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return blog