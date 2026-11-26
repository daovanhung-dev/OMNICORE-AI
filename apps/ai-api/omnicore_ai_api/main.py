from fastapi import FastAPI

app = FastAPI(title="OMNICORE AI Adapter", version="0.1.0")


@app.get("/health/live", tags=["health"])
def health_live() -> dict[str, str]:
    return {"status": "ok", "service": "ai-api"}
