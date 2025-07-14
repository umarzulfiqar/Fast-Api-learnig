from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import scheme,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close

#adding user
@app.post('/user')
def add_user(request:scheme.user,db:Session=Depends(get_db)):
    new_user=models.user_data(name=request.name,email=request.email,password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#add data 
@app.post('/blog',status_code=status.HTTP_201_CREATED)
def C(request:scheme.Blog,db:Session=Depends(get_db)):
    new_blog=models.blog_data(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#read data
@app.get('/blog',response_model=list[scheme.show_blog])
def R(db:Session=Depends(get_db)):
    blogs=db.query(models.blog_data).all()
    return blogs

@app.get('/blog/{id}',response_model=scheme.show_blog)
def R_with_id(response:Response,id,db:Session=Depends(get_db)):
    blogs=db.query(models.blog_data).filter(models.blog_data.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Response with id {id} not found')
    #     response.status_code=status.HTTP_404_NOT_FOUND
    #     return {'detail':f'Response with id {id} not found'}
    return blogs

#updata data
@app.put('/blog{id}',status_code=status.HTTP_202_ACCEPTED)
def U(id,request:scheme.Blog,db:Session=Depends(get_db)):
    blog=db.query(models.blog_data).filter(models.blog_data.id==id)
    if not blog.first():
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog not found with id {id}")
    blog.update(request.model_dump(), synchronize_session=False)
    db.commit()
    return "UPDATED"

#delete data
@app.delete('/blog{id}',status_code=status.HTTP_204_NO_CONTENT)
def D(id,db:Session=Depends(get_db)):
    blog=db.query(models.blog_data).filter(models.blog_data.id==id)
    if  not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog not found with id {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return blog