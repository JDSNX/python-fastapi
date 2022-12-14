from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str]=""): 

    posts = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(
        models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.get("/{id}", response_model=schemas.PostOut)
async def get_posts(id: int, 
                    db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):  

    post = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(
        models.Posts.id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post id {id} not found")

    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, 
                    db: Session = Depends(get_db), 
                    current_user: int=Depends(oauth2.get_current_user)):

    post = models.Posts(user_id=current_user.id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, 
                    db: Session = Depends(get_db), 
                    current_user: int=Depends(oauth2.get_current_user)):

    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post id {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, 
                    updated_post: schemas.PostCreate, 
                    db: Session = Depends(get_db), 
                    current_user: int=Depends(oauth2.get_current_user)):

    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post id {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()