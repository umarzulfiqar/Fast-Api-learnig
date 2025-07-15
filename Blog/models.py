from sqlalchemy import Column, Integer, String ,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class blog_data(Base):
    __tablename__='blog_user'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)
    user_id=Column(Integer,ForeignKey('user_data.id'))  #Foreign Key

    author=relationship("user_data",back_populates="blogs")  #relation 1 to *

class user_data(Base):
    __tablename__='user_data'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)

    blogs=relationship("blog_data",back_populates="author")   #relation 1 to *