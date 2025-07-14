from fastapi import FastAPI,Depends,status
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
