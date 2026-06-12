from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api import deps
from app.models.models import Post, Subreddit, User
from app.schemas.schemas import PostCreate, PostResponse

router = APIRouter()

@router.get("/", response_model=List[PostResponse])
def read_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    subreddit_name: Optional[str] = None
) -> Any:
    """
    Retrieve posts. Supports filtering by subreddit.
    """
    query = db.query(Post)
    if subreddit_name:
        subreddit = db.query(Subreddit).filter(Subreddit.name == subreddit_name).first()
        if subreddit:
            query = query.filter(Post.subreddit_id == subreddit.id)
        else:
            return []
            
    posts = query.order_by(desc(Post.created_at)).offset(skip).limit(limit).all()
    return posts

@router.post("/", response_model=PostResponse)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: PostCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new post.
    """
    subreddit = db.query(Subreddit).filter(Subreddit.id == post_in.subreddit_id).first()
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")
        
    post = Post(
        title=post_in.title,
        content=post_in.content,
        type=post_in.type,
        subreddit_id=post_in.subreddit_id,
        author_id=current_user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/{id}", response_model=PostResponse)
def read_post(
    id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get post by ID.
    """
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
