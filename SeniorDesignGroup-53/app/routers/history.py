from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api", tags=["history"])

@router.get("/history", response_model=List[schemas.HistoryItem])
async def history(limit: int = Query(25, ge=1, le=200), db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(models.URLAnalysis).order_by(desc(models.URLAnalysis.submitted_at)).limit(limit))
    rows = q.scalars().all()
    return [
        schemas.HistoryItem(
            id=r.id, url=r.url, domain=r.domain,
            submitted_at=r.submitted_at.isoformat(),
            verdict=r.verdict, risk_score=r.risk_score, blocked=r.blocked
        )
        for r in rows
    ]
