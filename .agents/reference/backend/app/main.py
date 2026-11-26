import os
from pathlib import Path
from fastapi import FastAPI
from app.api.v1 import router
from app.core.config import Settings
from app.core.responses import ApiError, handle_error
from app.core.observability import trace_request
from app.core.database import get_db
from app.core.security import TokenConfig
import sqlite3
from fastapi.responses import JSONResponse

def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="Danh mục mẫu")
    app.state.settings = settings
    app.add_exception_handler(ApiError, handle_error)
    app.middleware('http')(trace_request)
    app.include_router(router)
    @app.get('/health/live',include_in_schema=False)
    def live():return {'status':'ok'}
    @app.get('/health/ready',include_in_schema=False)
    def ready():
        try:
            with get_db(settings) as db:db.execute('SELECT 1 FROM items LIMIT 1').fetchone()
        except sqlite3.Error:return JSONResponse(status_code=503,content={'status':'unavailable'})
        return {'status':'ok'}
    return app

def app_factory() -> FastAPI:
    protected=os.environ.get('DEMO_PROTECTED','0')=='1'
    token=TokenConfig(os.environ['JWT_SECRET'],os.environ['JWT_ISSUER'],os.environ['JWT_AUDIENCE']) if protected else None
    return create_app(Settings(Path(os.environ["DEMO_DB"]).resolve(),token,protected))
