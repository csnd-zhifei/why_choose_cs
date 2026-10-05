"""ORM 模型统一导出"""
from .orm import Comment, Post, Record, ReplyComment, Test, User

__all__ = ["User", "Post", "Comment", "ReplyComment", "Record", "Test"]
