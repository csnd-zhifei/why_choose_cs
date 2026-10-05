"""评论与回复业务逻辑"""
from sqlmodel import Session, col, select

from backend.core.exceptions import BadRequestError, NotFoundError
from backend.core.ids import gen_id
from backend.db.models import Comment, Post, ReplyComment, User
from backend.schemas.comment import CommentCreate, ReplyCreate


def _require_user(session: Session, userid: int) -> None:
    if session.get(User, userid) is None:
        raise BadRequestError("用户不存在")


def list_comments(session: Session, postid: int) -> list[Comment]:
    stmt = (
        select(Comment)
        .where(Comment.postid == postid, Comment.is_deleted == 0)
        .order_by(col(Comment.create_time).asc())
    )
    return list(session.exec(stmt).all())


def create_comment(session: Session, data: CommentCreate) -> Comment:
    _require_user(session, data.userid)

    comment = Comment(
        commentid=gen_id(),
        postid=data.postid,
        userid=data.userid,
        content=data.content,
        is_deleted=0,
    )
    session.add(comment)

    # 同步笔记的评论数
    if data.postid is not None:
        post = session.get(Post, data.postid)
        if post is not None:
            post.comment_tot = (post.comment_tot or 0) + 1
            session.add(post)

    session.commit()
    session.refresh(comment)
    return comment


def delete_comment(session: Session, comment_id: int) -> None:
    comment = session.get(Comment, comment_id)
    if comment is None or comment.is_deleted:
        raise NotFoundError("评论不存在")

    comment.is_deleted = 1
    session.add(comment)

    if comment.postid is not None:
        post = session.get(Post, comment.postid)
        if post is not None:
            post.comment_tot = max(0, (post.comment_tot or 0) - 1)
            session.add(post)

    session.commit()


def list_replies(session: Session, commentid: int) -> list[ReplyComment]:
    stmt = (
        select(ReplyComment)
        .where(ReplyComment.commentid == commentid, ReplyComment.is_deleted == 0)
        .order_by(col(ReplyComment.create_time).asc())
    )
    return list(session.exec(stmt).all())


def create_reply(
    session: Session, commentid: int, data: ReplyCreate
) -> ReplyComment:
    """commentid 是评论的业务 id（comments.commentid）"""
    _require_user(session, data.userid)
    if session.exec(
        select(Comment).where(Comment.commentid == commentid, Comment.is_deleted == 0)
    ).first() is None:
        raise NotFoundError("评论不存在")

    reply = ReplyComment(
        commentid=commentid,
        userid=data.userid,
        content=data.content,
        to_user=data.to_user,
        is_deleted=0,
    )
    session.add(reply)
    session.commit()
    session.refresh(reply)
    return reply


def delete_reply(session: Session, reply_id: int) -> None:
    reply = session.get(ReplyComment, reply_id)
    if reply is None or reply.is_deleted:
        raise NotFoundError("回复不存在")
    reply.is_deleted = 1
    session.add(reply)
    session.commit()
