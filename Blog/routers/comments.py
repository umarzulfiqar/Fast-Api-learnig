from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .. import scheme,models
from ..database import get_db
from ..oauth2 import get_current_user
from uuid import UUID



router=APIRouter(
    tags=['Comment'],
    prefix='/blog/{id}/comment'
)

@router.post('/')
def add_comment(id:UUID,request:scheme.comment , db: Session = Depends(get_db), current_user: scheme.user = Depends(get_current_user)):
    new_comment = models.Comment(blog_id=id,content=request.content,user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment