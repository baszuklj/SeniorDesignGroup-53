import httpx
from ..config import settings

# Docs: https://docs.virustotal.com/reference/url
async def check(url: str) -> tuple[str, float, dict]:
    if not settings.VIRUSTOTAL_API_KEY:
        return ("error", 0.0, {"message": "VT key not set"})
    headers = {"x-apikey": settings.VIRUSTOTAL_API_KEY}
    async with httpx.AsyncClient(timeout=30) as client:
        # Submit/normalize URL
        submit = await client.post("https://www.virustotal.com/api/v3/urls", data={"url": url}, headers=headers)
        if submit.status_code >= 400:
            return ("error", 0.0, {"submit_error": submit.text})
        url_id = submit.json()["data"]["id"]

        # Fetch analysis
        res = await client.get(f"https://www.virustotal.com/api/v3/analyses/{url_id}", headers=headers)
        data = res.json()
        stats = data.get("data", {}).get("attributes", {}).get("stats", {})
        malicious = int(stats.get("malicious", 0))
        suspicious = int(stats.get("suspicious", 0))
        score = min(100.0, (malicious * 20) + (suspicious * 10))  # simple mapping
        status = "flagged" if score >= 20 else "ok"
        return (status, score, data)
