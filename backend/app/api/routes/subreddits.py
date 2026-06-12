from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.models import Subreddit, User
from app.schemas.schemas import SubredditCreate, SubredditResponse

router = APIRouter()

@router.get("/", response_model=List[SubredditResponse])
def read_subreddits(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve subreddits.
    """
    subreddits = db.query(Subreddit).offset(skip).limit(limit).all()
    return subreddits

@router.post("/", response_model=SubredditResponse)
def create_subreddit(
    *,
    db: Session = Depends(deps.get_db),
    subreddit_in: SubredditCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new subreddit.
    """
    subreddit = db.query(Subreddit).filter(Subreddit.name == subreddit_in.name).first()
    if subreddit:
        raise HTTPException(
            status_code=400,
            detail="A subreddit with this name already exists.",
        )
    subreddit = Subreddit(
        name=subreddit_in.name,
        description=subreddit_in.description,
        owner_id=current_user.id
    )
    db.add(subreddit)
    db.commit()
    db.refresh(subreddit)
    return subreddit

@router.get("/{name}", response_model=SubredditResponse)
def read_subreddit(
    name: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get subreddit by name.
    """
    subreddit = db.query(Subreddit).filter(Subreddit.name == name).first()
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")
    return subreddit
