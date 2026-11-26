from fastapi import Request
from .security import authenticate,require_role

def guard_items(request: Request) -> None:
    settings=request.app.state.settings
    if settings.protected_items:
        principal=authenticate(settings.token_config,request.headers.get('Authorization'))
        require_role(principal,frozenset({'reader'}))
