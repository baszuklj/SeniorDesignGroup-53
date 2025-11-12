import httpx
from ..config import settings

# Docs: https://developers.google.com/safe-browsing
async def check(url: str) -> tuple[str, float, dict]:
    """
    Returns (status, score, raw).
    status: "ok"|"flagged"|"error"
    score: 0..100 risk percentage (higher = riskier)
    """
    if not settings.GOOGLE_SAFE_BROWSING_API_KEY:
        return ("error", 0.0, {"message": "GSB key not set"})
    endpoint = (
        "https://safebrowsing.googleapis.com/v4/threatMatches:find"
        f"?key={settings.GOOGLE_SAFE_BROWSING_API_KEY}"
    )
    body = {
        "client": {"clientId": "url-guardian", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE","SOCIAL_ENGINEERING","UNWANTED_SOFTWARE","POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(endpoint, json=body)
        data = r.json()
        flagged = bool(data.get("matches"))
        return ("flagged" if flagged else "ok", 90.0 if flagged else 0.0, data)
