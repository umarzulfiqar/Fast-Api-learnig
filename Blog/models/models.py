import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String ,ForeignKey,Text
from core.database import Base
from sqlalchemy.orm import relationship

class blog_data(Base):
    __tablename__='blog_user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title=Column(String)
    body=Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user_data.id'), nullable=False)  #Foreign Key

    author=relationship("user_data",back_populates="blogs")  #relation 1 to *
    comments = relationship("Comment", back_populates="blogs")  # relation 1 to *


class user_data(Base):
    __tablename__='user_data'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name=Column(String)
    email=Column(String)
    password=Column(String)

    blogs=relationship("blog_data",back_populates="author")   #relation 1 to *
    comments = relationship("Comment", back_populates="author")  # relation 1 to *

class Comment(Base):
    __tablename__="comments_table"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    content = Column(Text, nullable=False)
    user_id=Column(UUID(as_uuid=True), ForeignKey('user_data.id'), nullable=False) #Foregin Key of user
    blog_id=Column(UUID(as_uuid=True), ForeignKey('blog_user.id'), nullable=False) #Foregin key of blog

    blogs=relationship("blog_data",back_populates="comments")
    author=relationship("user_data",back_populates="comments")