from urllib.parse import urlparse
from .config import settings

def domain_of(url: str) -> str:
    host = urlparse(url).netloc
    return host.split(":")[0].lower()

def weighted_score(gsb: float, vt: float, ssl: float, phish: float) -> float:
    s = (
        settings.WEIGHT_GSB * gsb
        + settings.WEIGHT_VT * vt
        + settings.WEIGHT_SSL * ssl
        + settings.WEIGHT_PHISH * phish
    )
    return round(min(100.0, max(0.0, s * 100 if s <= 1 else s)), 2) if max(gsb, vt, ssl, phish) <= 1 else round(min(100.0, s), 2)

def verdict_from(score: float) -> str:
    if score >= 60:  return "unsafe"
    if score >= 20:  return "suspicious"
    return "safe"
