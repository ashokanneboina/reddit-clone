from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.models import Vote, Post, Comment, User
from app.schemas.schemas import VoteCreate

router = APIRouter()

@router.post("/")
def cast_vote(
    *,
    db: Session = Depends(deps.get_db),
    vote_in: VoteCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Cast a vote on a post or comment.
    """
    if vote_in.item_type not in ["post", "comment"]:
        raise HTTPException(status_code=400, detail="Invalid item_type")
        
    if vote_in.value not in [1, -1, 0]: # 0 to remove vote
        raise HTTPException(status_code=400, detail="Invalid vote value")
        
    # Check if item exists
    if vote_in.item_type == "post":
        item = db.query(Post).filter(Post.id == vote_in.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Post not found")
        existing_vote = db.query(Vote).filter(
            Vote.user_id == current_user.id,
            Vote.post_id == vote_in.item_id
        ).first()
    else:
        item = db.query(Comment).filter(Comment.id == vote_in.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Comment not found")
        existing_vote = db.query(Vote).filter(
            Vote.user_id == current_user.id,
            Vote.comment_id == vote_in.item_id
        ).first()

    if existing_vote:
        if vote_in.value == 0:
            db.delete(existing_vote)
        else:
            existing_vote.value = vote_in.value
            db.add(existing_vote)
    elif vote_in.value != 0:
        new_vote = Vote(
            user_id=current_user.id,
            value=vote_in.value,
        )
        if vote_in.item_type == "post":
            new_vote.post_id = vote_in.item_id
        else:
            new_vote.comment_id = vote_in.item_id
        db.add(new_vote)
        
    db.commit()
    return {"status": "success"}
