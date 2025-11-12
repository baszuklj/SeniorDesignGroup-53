# Minimal placeholder. PhishTank provides a database/feed; you can
# either download/refresh it periodically or use an API proxy.
# Here we just stub a function you can later wire to a cached feed lookup.

async def check(url: str) -> tuple[str, float, dict]:
    # TODO: implement local feed lookup or API request
    return ("error", 0.0, {"message": "PhishTank not configured"})
