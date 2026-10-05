"""用户相关请求/响应模型"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=6, max_length=64)
    avatar: str = Field(default="", max_length=511)
    gender: Optional[int] = Field(default=None, description="0女，1男，2其他")
    user_location: Optional[str] = Field(default=None, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    avatar: Optional[str] = Field(default=None, max_length=511)
    gender: Optional[int] = None
    user_location: Optional[str] = Field(default=None, max_length=128)


class UserOut(BaseModel):
    """对外输出，不含 password_hash"""
    model_config = ConfigDict(from_attributes=True)

    userid: int
    username: str
    avatar: str
    gender: Optional[int] = None
    user_location: Optional[str] = None
    create_time: Optional[datetime] = None
