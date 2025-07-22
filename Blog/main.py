from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users,blogs,authorization,comments
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authorization.router)
app.include_router(blogs.router)
app.include_router(comments.router)
app.include_router(users.router)
