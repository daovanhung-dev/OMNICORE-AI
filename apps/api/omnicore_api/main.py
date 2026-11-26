from fastapi import FastAPI

app = FastAPI(title="OMNICORE AI Business API", version="0.1.0")


@app.get("/health/live", tags=["health"])
def health_live() -> dict[str, str]:
    return {"status": "ok", "service": "api"}
