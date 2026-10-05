"""评论与回复相关请求/响应模型"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    postid: Optional[int] = None
    userid: int
    content: str = Field(min_length=1, max_length=2047)


class CommentOut(BaseModel):
    id: int
    commentid: int
    postid: Optional[int] = None
    userid: int
    username: Optional[str] = None
    avatar: Optional[str] = None
    content: str
    create_time: Optional[datetime] = None

    @classmethod
    def from_model(cls, comment, user=None) -> "CommentOut":
        return cls(
            id=comment.id,
            commentid=comment.commentid,
            postid=comment.postid,
            userid=comment.userid,
            username=user.username if user is not None else None,
            avatar=user.avatar if user is not None else None,
            content=comment.content,
            create_time=comment.create_time,
        )


class ReplyCreate(BaseModel):
    userid: int
    content: str = Field(min_length=1, max_length=2047)
    to_user: int = Field(description="被回复的用户id")


class ReplyOut(BaseModel):
    id: int
    commentid: int
    userid: int
    username: Optional[str] = None
    avatar: Optional[str] = None
    content: str
    to_user: int
    create_time: Optional[datetime] = None

    @classmethod
    def from_model(cls, reply, user=None) -> "ReplyOut":
        return cls(
            id=reply.id,
            commentid=reply.commentid,
            userid=reply.userid,
            username=user.username if user is not None else None,
            avatar=user.avatar if user is not None else None,
            content=reply.content,
            to_user=reply.to_user,
            create_time=reply.create_time,
        )
