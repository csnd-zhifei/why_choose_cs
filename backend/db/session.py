"""数据库连接与 Session 管理"""
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import Session

from backend.core.config import settings

# 连接池配置，echo 由 .env 的 DB_ECHO 控制（调试时置 true）
engine = create_engine(
    settings.database_url,
    pool_size=5,
    pool_recycle=1200,
    pool_pre_ping=True,
    echo=settings.db_echo,
)


def get_db():
    """FastAPI 依赖：每个请求一个 Session，请求结束自动关闭"""
    with Session(engine) as session:
        yield session


def connect_db() -> Engine:
    """启动时探活，连不上会直接抛异常"""
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1")
    return engine
