from dataclasses import dataclass
from pathlib import Path
from .security import TokenConfig

@dataclass(frozen=True)
class Settings:
    """Đường dẫn cơ sở dữ liệu thử nghiệm, không chứa bí mật."""
    database_path: Path
    token_config: TokenConfig | None = None
    protected_items: bool = False

    def __post_init__(self) -> None:
        if self.protected_items and self.token_config is None:
            raise ValueError("API bảo vệ cần cấu hình JWT")
        if not self.database_path.is_absolute():
            raise ValueError("Đường dẫn cơ sở dữ liệu phải tuyệt đối")
