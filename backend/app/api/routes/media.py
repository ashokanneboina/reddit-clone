from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api import deps
from app.models.models import Media

router = APIRouter()

@router.get("/{media_id}")
def get_media(
    media_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get media file by ID.
    """
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
        
    return Response(content=media.data, media_type=media.content_type)
