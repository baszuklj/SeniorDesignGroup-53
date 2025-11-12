from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import schemas, models
from ..analysis import domain_of, weighted_score, verdict_from
from ..services import google_safe_browsing as gsb
from ..services import virustotal as vt
from ..services import ssllabs as ssl
from ..services import phishtank as pt

router = APIRouter(prefix="/api", tags=["analyze"])

@router.post("/analyze", response_model=schemas.AnalyzeResponse)
async def analyze(req: schemas.AnalyzeRequest, db: AsyncSession = Depends(get_db)):
    dom = domain_of(str(req.url))

    # Is domain blocked?
    blocked = await db.execute(select(models.BlockedDomain).where(models.BlockedDomain.domain == dom))
    is_blocked = blocked.scalar_one_or_none() is not None

    # Call services
    gsb_status, gsb_score, gsb_raw = await gsb.check(str(req.url))
    vt_status,  vt_score,  vt_raw  = await vt.check(str(req.url))
    ssl_status, ssl_score, ssl_raw = await ssl.check(str(req.url))
    pt_status,  pt_score,  pt_raw  = await pt.check(str(req.url))

    # Normalize scores to 0..100
    gsb_score = float(gsb_score)
    vt_score  = float(vt_score)
    ssl_score = float(ssl_score)
    pt_score  = float(pt_score)

    final_score = weighted_score(gsb_score, vt_score, ssl_score, pt_score)
    verdict = verdict_from(final_score)

    # Persist
    analysis = models.URLAnalysis(
        url=str(req.url),
        domain=dom,
        verdict=verdict,
        risk_score=final_score,
        blocked=is_blocked,
        details={
            "google_safe_browsing": {"status": gsb_status, "score": gsb_score, "raw": gsb_raw},
            "virustotal":           {"status": vt_status,  "score": vt_score,  "raw": vt_raw},
            "ssllabs":              {"status": ssl_status, "score": ssl_score, "raw": ssl_raw},
            "phishtank":            {"status": pt_status,  "score": pt_score,  "raw": pt_raw},
        },
    )
    db.add(analysis)
    await db.commit()

    return schemas.AnalyzeResponse(
        url=str(req.url),
        domain=dom,
        verdict=verdict,
        risk_score=final_score,
        blocked=is_blocked,
        services={
            "google_safe_browsing": schemas.ServiceDetail(status=gsb_status, score=gsb_score, raw=gsb_raw),
            "virustotal":           schemas.ServiceDetail(status=vt_status,  score=vt_score,  raw=vt_raw),
            "ssllabs":              schemas.ServiceDetail(status=ssl_status, score=ssl_score, raw=ssl_raw),
            "phishtank":            schemas.ServiceDetail(status=pt_status,  score=pt_score,  raw=pt_raw),
        },
    )
