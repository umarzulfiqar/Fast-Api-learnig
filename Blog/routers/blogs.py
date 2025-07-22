from fastapi import APIRouter,status,Depends,Response,HTTPException
from sqlalchemy.orm import Session
from .. import scheme,models,database,oauth2


get_db=database.get_db

router=APIRouter(
    prefix="/blog",
    tags=['Blog']
)



#add data 
@router.post('/',status_code=status.HTTP_201_CREATED)
def create_blog(request:scheme.Blog,db:Session=Depends(get_db),current_user:scheme.user=Depends(oauth2.get_current_user)):
    new_blog=models.blog_data(title=request.title,body=request.body,user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#read data
@router.get('/',response_model=list[scheme.show_blog])
def read_blog(db:Session=Depends(get_db),current_user:scheme.user=Depends(oauth2.get_current_user)):
    blogs=db.query(models.blog_data).all()
    return blogs


@router.get('/{id}',response_model=scheme.show_blog)
def read_with_id(response:Response, id: int, db:Session=Depends(get_db), current_user:scheme.user=Depends(oauth2.get_current_user)):
    blogs=db.query(models.blog_data).filter(models.blog_data.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Response with id {id} not found')
    #     response.status_code=status.HTTP_404_NOT_FOUND
    #     return {'detail':f'Response with id {id} not found'}
    return blogs


#updata data
@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request:scheme.Blog, db:Session=Depends(get_db), current_user:scheme.user=Depends(oauth2.get_current_user)):
    blog=db.query(models.blog_data).filter(models.blog_data.id==id)
    if not blog.first():
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog not found with id {id}")
    blog.update(request.model_dump(), synchronize_session=False)
    db.commit()
    return "UPDATED"

#delete data
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db:Session=Depends(get_db), current_user:scheme.user=Depends(oauth2.get_current_user)):
    blog=db.query(models.blog_data).filter(models.blog_data.id==id)
    if  not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog not found with id {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return blog
