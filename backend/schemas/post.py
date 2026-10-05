"""笔记相关请求/响应模型"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.schemas.user import UserOut


class PostCreate(BaseModel):
    userid: int
    title: Optional[str] = Field(default=None, max_length=255)
    intro: str = Field(min_length=1, max_length=511)
    mdurl: Optional[str] = Field(default=None, max_length=2083)


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    intro: Optional[str] = Field(default=None, min_length=1, max_length=511)
    mdurl: Optional[str] = Field(default=None, max_length=2083)


class PostOut(BaseModel):
    postid: int
    userid: int
    author: Optional[UserOut] = None  # 作者信息，列表/详情统一带上
    title: Optional[str] = None
    intro: str
    summary: Optional[str] = None
    comment_tot: Optional[int] = None
    like_tot: Optional[int] = None
    bookmark_tot: Optional[int] = None
    mdurl: Optional[str] = None
    htmlurl: Optional[str] = None
    create_time: Optional[datetime] = None
    ready: bool = False  # 是否已有可展示的页面（htmlurl 就绪）

    @classmethod
    def from_model(cls, post, user=None) -> "PostOut":
        return cls(
            postid=post.postid,
            userid=post.userid,
            author=UserOut.model_validate(user) if user is not None else None,
            title=post.title,
            intro=post.intro,
            summary=post.summary,
            comment_tot=post.comment_tot,
            like_tot=post.like_tot,
            bookmark_tot=post.bookmark_tot,
            mdurl=post.mdurl,
            htmlurl=post.htmlurl,
            create_time=post.create_time,
            ready=bool(post.htmlurl),
        )


class PostListOut(BaseModel):
    total: int
    page: int
    size: int
    items: list[PostOut]
