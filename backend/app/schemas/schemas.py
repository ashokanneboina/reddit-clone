from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Subreddit Schemas ---
class SubredditBase(BaseModel):
    name: str
    description: Optional[str] = None

class SubredditCreate(SubredditBase):
    pass

class SubredditResponse(SubredditBase):
    id: int
    owner_id: int
    created_at: datetime
    class Config:
        from_attributes = True

# --- Media Schemas ---
class MediaResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    created_at: datetime
    class Config:
        from_attributes = True

# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    type: str = "text"
    subreddit_id: int

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    author: UserResponse
    subreddit: SubredditResponse
    media: List[MediaResponse] = []
    class Config:
        from_attributes = True

# --- Comment Schemas ---
class CommentBase(BaseModel):
    content: str
    post_id: int
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    author_id: int
    created_at: datetime
    author: UserResponse
    class Config:
        from_attributes = True

# --- Vote Schemas ---
class VoteCreate(BaseModel):
    item_id: int
    item_type: str # 'post' or 'comment'
    value: int # 1 or -1
