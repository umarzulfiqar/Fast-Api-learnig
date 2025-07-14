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

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def C(request:scheme.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def R(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def R_with_id(response:Response,id,db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Response with id {id} not found')
    #     response.status_code=status.HTTP_404_NOT_FOUND
    #     return {'detail':f'Response with id {id} not found'}
    return blogs