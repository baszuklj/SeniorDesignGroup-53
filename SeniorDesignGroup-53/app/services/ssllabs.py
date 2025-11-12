import httpx
from urllib.parse import urlparse
from ..config import settings

# Docs: https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs.md
async def check(url: str) -> tuple[str, float, dict]:
    host = urlparse(url).netloc
    if ":" in host:
        host = host.split(":")[0]
    params = {"host": host, "publish": "off", "startNew": "on", "fromCache": "on", "all": "done"}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(settings.SSLLABS_API_URL + "analyze", params=params)
        data = r.json()
        # Derive a rough risk: if any endpoint grade is below B, add risk
        endpoints = data.get("endpoints", []) or []
        risk = 0.0
        for ep in endpoints:
            grade = ep.get("grade", "T")
            # A+:0, A:5, B:10, C:30, lower/higher risk if worse/ungraded
            mapping = {"A+": 0, "A": 5, "B": 10, "C": 30, "T": 40}
            risk = max(risk, mapping.get(grade, 40))
        status = "ok" if risk <= 10 else "flagged" if risk >= 30 else "warn"
        return (status, risk, data)
