from sqlalchemy import Column, Integer, String
from .database import Base

class blog_data(Base):
    __tablename__='blog_user'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)

class user_data(Base):
    __tablename__='user_data'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)

