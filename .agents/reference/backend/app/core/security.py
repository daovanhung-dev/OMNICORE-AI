"""JWT HS256 có issuer/audience, thời hạn và quyền rõ. Không tự đăng nhập người dùng."""
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
import secrets
import jwt
from .responses import ApiError

@dataclass(frozen=True)
class TokenConfig:
    secret: str = field(repr=False)
    issuer: str
    audience: str
    ttl_seconds: int = 300
    def __post_init__(self):
        if len(self.secret.encode()) < 32 or not self.issuer or not self.audience or not 1 <= self.ttl_seconds <= 900:
            raise ValueError('Cấu hình JWT không hợp lệ')

@dataclass(frozen=True)
class Principal:
    subject: str
    roles: tuple[str, ...]

def issue_access(config: TokenConfig, principal: Principal) -> str:
    if not principal.subject or not all(isinstance(r,str) and r for r in principal.roles):raise ValueError('Định danh sai')
    now=datetime.now(timezone.utc)
    return jwt.encode({'sub':principal.subject,'roles':list(principal.roles),'iss':config.issuer,'aud':config.audience,'iat':now,'nbf':now,'exp':now+timedelta(seconds=config.ttl_seconds),'jti':secrets.token_urlsafe(18),'typ':'access'},config.secret,algorithm='HS256')

def authenticate(config: TokenConfig, authorization: str | None) -> Principal:
    try:
        scheme, token=(authorization or '').split(' ',1)
        if scheme.lower()!='bearer' or not token or len(token)>8192:raise ValueError('token')
        data=jwt.decode(token,config.secret,algorithms=['HS256'],issuer=config.issuer,audience=config.audience,options={'require':['sub','roles','iss','aud','iat','nbf','exp','jti','typ']})
        if data['typ']!='access' or not isinstance(data['sub'],str) or not data['sub'] or not isinstance(data['roles'],list) or not all(isinstance(r,str) and r for r in data['roles']):raise ValueError('claims')
        return Principal(data['sub'],tuple(data['roles']))
    except (jwt.InvalidTokenError,ValueError,TypeError,KeyError) as exc:
        raise ApiError(401,'UNAUTHENTICATED','Yêu cầu xác thực hợp lệ') from exc

def require_role(principal: Principal, roles: frozenset[str]) -> None:
    if not roles.intersection(principal.roles):raise ApiError(403,'FORBIDDEN','Không có quyền thực hiện')

def require_owner(principal: Principal, owner: str) -> None:
    if not owner or principal.subject!=owner:raise ApiError(403,'FORBIDDEN','Không có quyền thực hiện')
