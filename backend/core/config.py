"""应用配置

所有配置集中在这里，值从环境变量 / 项目根目录的 .env 读取（环境变量优先）。
字段名小写，pydantic-settings 默认大小写不敏感，对应 .env 里的大写变量名。
"""
from pathlib import Path
from urllib.parse import quote

from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录（backend/core/config.py -> backend/core -> backend -> 根）
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ---- MySQL ----
    mysql_root_name: str = "root"
    mysql_root_password: str = ""
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_database: str = "why_choose_cs"
    db_echo: bool = False

    # ---- AI（任意兼容 OpenAI /chat/completions 接口的第三方提供商）----
    # base_url 不写死，必须在 .env 里配置，例如 https://api.deepseek.com
    ai_api_key: str = ""
    ai_base_url: str = ""
    ai_model: str = ""

    # ---- 运行 ----
    static_dir: Path = BASE_DIR / "backend" / "static"

    @property
    def spa_dir(self) -> Path:
        """AI 生成的 SPA 页面目录"""
        return self.static_dir / "spa"

    # ---- 上传限制 ----
    avatar_max_mb: int = 2
    md_max_mb: int = 1
    html_max_mb: int = 2

    # ---- 热度排序（Hacker News 式时间衰减）----
    # score = (like_tot - 1) / (发布至今小时数 + hot_offset) ** hot_gravity
    hot_offset: float = 2.0  # 分子分母的平缓项，防止新帖分数爆炸
    hot_gravity: float = 1.8  # 衰减指数，越大越偏向新内容
    hot_window_days: int = 30  # 热度榜只统计最近 N 天；0 表示不限

    @property
    def database_url(self) -> str:
        """密码里可能带 @ 等特殊字符，必须转义"""
        password = quote(self.mysql_root_password)
        return (
            f"mysql+pymysql://{self.mysql_root_name}:{password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )


settings = Settings()
