""" 数据库 ORM 模型 """
from __future__ import annotations

from typing import Optional

from pydantic import NaiveDatetime
from sqlalchemy import Index, SmallInteger, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlmodel import Field, SQLModel

_TABLE_ARGS = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_general_ci"}


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = _TABLE_ARGS

    userid: int = Field(sa_type=BIGINT, primary_key=True, sa_column_kwargs={"autoincrement": False}, description="pk")
    username: str = Field(max_length=50, description="用户名")
    password_hash: str = Field(max_length=128, description="密码盐值")
    avatar: str = Field(max_length=511, description="头像")
    gender: Optional[int] = Field(default=None, sa_type=SmallInteger, description="性别（0女，1男，2其他）")
    user_location: Optional[str] = Field(default=None, max_length=128, description="用户地区")
    create_time: Optional[NaiveDatetime] = Field(
        default=None, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    update_time: Optional[NaiveDatetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        },
    )
    is_deleted: int = Field(default=0, sa_type=TINYINT, description="0有效，1已软删")


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    # 列表按 create_time 排序、热度榜按时间窗口过滤，都走这个复合索引
    __table_args__ = (
        Index("ix_posts_deleted_ctime", "is_deleted", "create_time"),
        _TABLE_ARGS,
    )

    postid: int = Field(sa_type=BIGINT, primary_key=True, sa_column_kwargs={"autoincrement": False}, description="笔记id")
    userid: int = Field(sa_type=BIGINT, description="用户id")
    title: Optional[str] = Field(default=None, max_length=255, description="笔记标题")
    intro: str = Field(max_length=511, description="简介")
    summary: str = Field(max_length=2047, description="ai生成摘要，用于搜索")
    comment_tot: Optional[int] = Field(default=None, description="评论数")
    like_tot: Optional[int] = Field(default=None, description="点赞数")
    bookmark_tot: Optional[int] = Field(default=None, description="收藏数")
    mdurl: Optional[str] = Field(default=None, max_length=2083, description="笔记md的url")
    htmlurl: Optional[str] = Field(default=None, max_length=2083, description="html笔记的url")
    create_time: Optional[NaiveDatetime] = Field(
        default=None, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    delete_time: Optional[NaiveDatetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        },
    )
    is_deleted: int = Field(default=0, sa_type=TINYINT, description="0有效，1删除")


class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    __table_args__ = _TABLE_ARGS

    id: Optional[int] = Field(default=None, primary_key=True, description="pk")
    commentid: int = Field(sa_type=BIGINT, description="评论id")
    postid: Optional[int] = Field(default=None, sa_type=BIGINT, description="笔记id")
    userid: int = Field(sa_type=BIGINT, description="用户id")
    content: str = Field(max_length=2047, description="评论内容")
    create_time: Optional[NaiveDatetime] = Field(
        default=None, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    update_time: Optional[NaiveDatetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        },
    )
    is_deleted: int = Field(default=0, sa_type=TINYINT, description="0有效，1软删")


class ReplyComment(SQLModel, table=True):
    __tablename__ = "reply_comment"
    __table_args__ = _TABLE_ARGS

    id: Optional[int] = Field(default=None, primary_key=True, description="pk")
    commentid: int = Field(sa_type=BIGINT, description="评论id")
    userid: int = Field(sa_type=BIGINT, description="用户id")
    content: str = Field(max_length=2047, description="评论内容")
    to_user: int = Field(sa_type=BIGINT, description="目标评论id")
    create_time: Optional[NaiveDatetime] = Field(
        default=None, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    update_time: Optional[NaiveDatetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        },
    )
    is_deleted: int = Field(default=0, sa_type=TINYINT, description="0有效，1软删")


class Record(SQLModel, table=True):

    __tablename__ = "record"
    # 点赞/收藏按 (postid, userid) 查，走这个索引
    __table_args__ = (
        Index("ix_record_postid_userid", "postid", "userid"),
        _TABLE_ARGS,
    )

    id: Optional[int] = Field(default=None, primary_key=True, description="pk")
    postid: int = Field(sa_type=BIGINT, description="资源id")
    userid: int = Field(sa_type=BIGINT, description="用户id")
    is_like: Optional[int] = Field(default=None, sa_type=TINYINT, description="是否喜欢")
    is_bookmark: Optional[int] = Field(default=None, sa_type=TINYINT, description="是否收藏")
    is_comment: Optional[int] = Field(default=None, sa_type=TINYINT, description="留下的评论")
    # 这两列由应用侧写入，DDL 是 naive DATETIME，用 NaiveDatetime 注解
    create_time: Optional[NaiveDatetime] = Field(default=None)
    update_time: Optional[NaiveDatetime] = Field(default=None)


class Test(SQLModel, table=True):
    __tablename__ = "test"
    __table_args__ = _TABLE_ARGS

    id: int = Field(sa_type=BIGINT, primary_key=True, sa_column_kwargs={"autoincrement": False}, description="pk")
    title: Optional[str] = Field(default=None, max_length=255, description="标题")
    create_time: Optional[NaiveDatetime] = Field(
        default=None, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    update_time: Optional[NaiveDatetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        },
    )
    is_deleted: Optional[int] = Field(default=None, sa_type=TINYINT, description="0有效。1软删")
