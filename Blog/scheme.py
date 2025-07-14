from pydantic import BaseModel

class Blog(BaseModel):
    title:'str'
    body:'str'

class show_blog(BaseModel):
    title:str #which i want to show only to the user
    
class Config:
    orm_mode=True

class user(BaseModel):
    name: 'str'
    email:'str'
    password:'str'