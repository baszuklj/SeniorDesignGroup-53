from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/block", response_model=schemas.BlockDomainResponse)
async def block_domain(req: schemas.BlockDomainRequest, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(select(models.BlockedDomain).where(models.BlockedDomain.domain == req.domain.lower()))
    if exists.scalar_one_or_none():
        return schemas.BlockDomainResponse(domain=req.domain.lower(), blocked=True, reason="already")
    entry = models.BlockedDomain(domain=req.domain.lower(), reason=req.reason or "manual")
    db.add(entry)
    await db.commit()
    return schemas.BlockDomainResponse(domain=req.domain.lower(), blocked=True, reason=entry.reason)
