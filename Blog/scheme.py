from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title:str
    body:str

class user(BaseModel):
    name: str
    email:str
    password:str

class show_user(BaseModel):
    name:str
    email:str
    blogs:List[Blog]=[]

class show_just_user(BaseModel):
    name: str
    email: str

class show_blog(BaseModel):
    title:str #which i want to show only to the user
    body:str
    author: show_just_user
    
#FOr Login User    
class login(BaseModel):
    user_name: str
    password: str
#For Tokens
class token(BaseModel):
    access_token: str
    token_type: str

class token_data(BaseModel): 
    email: str | None = None

#For Comments
class comment(BaseModel):
    content :str