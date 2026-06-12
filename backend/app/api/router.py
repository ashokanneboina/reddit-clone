from fastapi import APIRouter

from app.api.routes import auth, users, subreddits, posts, comments, votes

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(subreddits.router, prefix="/subreddits", tags=["subreddits"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
