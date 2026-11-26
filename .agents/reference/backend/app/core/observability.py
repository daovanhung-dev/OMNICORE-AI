"""Mã truy vết sinh tại máy chủ, log cấu trúc không ghi URL tham số, body hay header."""
import logging,json,time,uuid
from fastapi import Request

async def trace_request(request:Request,call_next):
    trace=uuid.uuid4().hex;request.state.trace_id=trace;started=time.monotonic()
    response=await call_next(request)
    response.headers['X-Request-ID']=trace
    logging.getLogger('app.requests').info(json.dumps({'request_id':trace,'method':request.method,'status':response.status_code,'duration_ms':round((time.monotonic()-started)*1000,2)}))
    return response
