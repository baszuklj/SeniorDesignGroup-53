from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime, JSON, ForeignKey, Boolean, func

Base = declarative_base()

class URLAnalysis(Base):
    __tablename__ = "url_analysis"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(2048), index=True)
    domain: Mapped[str] = mapped_column(String(512), index=True)
    submitted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    verdict: Mapped[str] = mapped_column(String(32))  # "safe"|"unsafe"|"suspicious"
    risk_score: Mapped[float] = mapped_column(Float)
    details: Mapped[dict] = mapped_column(JSON)       # raw service results
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)

class BlockedDomain(Base):
    __tablename__ = "blocked_domain"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    domain: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    reason: Mapped[str] = mapped_column(String(512), default="manual")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
