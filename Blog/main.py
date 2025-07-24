from fastapi import FastAPI
from .models import models
from .core.database import engine
from .routers import blogs,authorization
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authorization.router)
app.include_router(blogs.router)

