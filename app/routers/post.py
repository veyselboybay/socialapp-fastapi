from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import get_db
from ..oauth2 import get_current_user
from ..models.models import Post
from ..schemas.user_schemas import Post as resPost, PostCreate


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",status_code=200,response_model=list[resPost])
async def root(db:Annotated[Session,Depends(get_db)],user:Annotated[int,Depends(get_current_user)]):
    
    posts = db.query(Post).all()
    
    return posts

@router.post("/create",status_code=201, response_model=resPost)
async def create_posts(post:PostCreate,db:Annotated[Session,Depends(get_db)],user:Annotated[int,Depends(get_current_user)]):
    new_post = Post(owner_id=user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}",status_code=200,response_model=resPost)
async def get_post_by_id(id:int,db:Annotated[Session,Depends(get_db)],user:Annotated[int,Depends(get_current_user)]):
    post = db.query(Post).filter(Post.id == id)
    if not post.first():
        raise HTTPException(status_code=404,detail=f"post with {id} not found!")
    return post.first()

@router.put("/{id}",status_code=200,response_model=resPost)
async def update_post_by_id(id: int, post:PostCreate,db:Annotated[Session,Depends(get_db)],user:Annotated[int,Depends(get_current_user)]):
    post_query = db.query(Post).filter(Post.id == id)
    
    if not post_query.first():
        raise HTTPException(status_code=404,detail=f"post with {id} not found!")
    
    if post_query.first().owner_id != user.id:
        raise HTTPException(status_code=404,detail=f"Not Authorized")
    
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()

    return post_query.first()

@router.delete("/{id}",status_code=204)
async def delete_post_by_id(id: int,db:Annotated[Session,Depends(get_db)],user:Annotated[int,Depends(get_current_user)]):
    post_query = db.query(Post).filter(Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=404,detail=f"post with {id} not found!")
    
    if post_query.first().owner_id != user.id:
        raise HTTPException(status_code=404,detail=f"Not Authorized")
    
    post_query.delete(synchronize_session=False)
    db.commit()
