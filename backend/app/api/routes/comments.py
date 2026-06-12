from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api import deps
from app.models.models import Comment, Post, User
from app.schemas.schemas import CommentCreate, CommentResponse

router = APIRouter()

@router.get("/post/{post_id}", response_model=List[CommentResponse])
def read_comments_for_post(
    post_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve comments for a specific post.
    """
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(desc(Comment.created_at)).offset(skip).limit(limit).all()
    return comments

@router.post("/", response_model=CommentResponse)
def create_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_in: CommentCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new comment.
    """
    post = db.query(Post).filter(Post.id == comment_in.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    if comment_in.parent_id:
        parent = db.query(Comment).filter(Comment.id == comment_in.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent comment not found")
            
    comment = Comment(
        content=comment_in.content,
        post_id=comment_in.post_id,
        parent_id=comment_in.parent_id,
        author_id=current_user.id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
