from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app =FastAPI()

@app.get('/blog')
def index(length:int=10,published:bool=True,sort:Optional[str]=None):
    if published==True:
        return {'data': f'This published block with length: {length}'}
    else:
        return {'data':'This is blog'}


@app.get('/about/{id}')
def about(id:int):
    return {'data':id}

@app.get('/reader')
def reader():
    return {'data':"This is reader's page"}

class Blog(BaseModel):
    title :'str'
    body: 'str'
    published: Optional[bool]

@app.post('/blog_post')
def post(request:Blog):
    return {'data':f'Blog sucessfully posted as {request.title}'}