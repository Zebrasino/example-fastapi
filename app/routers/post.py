from fastapi import Depends, HTTPException, status, APIRouter, Response
from .. import models, utils, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2
from typing import Optional

router = APIRouter(prefix="/posts",tags=["Posts"])

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #              (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
 

@router.get("/",response_model=list[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = (
        db.query(
            models.Post,
            func.count(func.distinct(models.Vote.id_user)).label("votes"),
            func.count(func.distinct(models.Retweet.id_user)).label("retweets"),
        )
        .join(models.Vote, models.Post.id == models.Vote.id_post, isouter=True)
        .join(models.Retweet, models.Post.id == models.Retweet.id_post, isouter=True)
        .group_by(models.Post.id) 
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts

@router.get("/{id}",response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
   # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id)))
   # post = cursor.fetchone()
    post_query = (
        db.query(
            models.Post,
            func.count(func.distinct(models.Vote.id_user)).label("votes"),
            func.count(func.distinct(models.Retweet.id_user)).label("retweets"),
        )
        .join(models.Vote, models.Post.id == models.Vote.id_post, isouter=True)
        .join(models.Retweet, models.Post.id == models.Retweet.id_post, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
    )
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} was not found")
    
    
    return post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to do this action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}",response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #               (post.title,post.content,post.published,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    
    query_post = db.query(models.Post).filter(models.Post.id == id)
    
    if query_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} was not found")
    
    if query_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to do this action")
    
    query_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return query_post.first()
