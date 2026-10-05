"""评论与回复接口"""
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from backend.db.session import get_db
from backend.schemas.comment import CommentCreate, CommentOut, ReplyCreate, ReplyOut
from backend.services import comment_service
from backend.services._enrich import user_map

router = APIRouter()


@router.get("", response_model=list[CommentOut], summary="评论列表")
def list_comments(postid: int = Query(...), db: Session = Depends(get_db)):
    comments = comment_service.list_comments(db, postid)
    users = user_map(db, [c.userid for c in comments])
    return [CommentOut.from_model(c, users.get(c.userid)) for c in comments]


@router.post("", response_model=CommentOut, summary="发表评论")
def create_comment(data: CommentCreate, db: Session = Depends(get_db)):
    comment = comment_service.create_comment(db, data)
    return CommentOut.from_model(comment, user_map(db, [comment.userid]).get(comment.userid))


@router.delete("/{comment_id}", summary="删除评论（软删）")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_service.delete_comment(db, comment_id)
    return {"ok": True}


@router.delete("/replies/{reply_id}", summary="删除回复（软删）")
def delete_reply(reply_id: int, db: Session = Depends(get_db)):
    comment_service.delete_reply(db, reply_id)
    return {"ok": True}


@router.get("/{commentid}/replies", response_model=list[ReplyOut], summary="回复列表")
def list_replies(commentid: int, db: Session = Depends(get_db)):
    replies = comment_service.list_replies(db, commentid)
    users = user_map(db, [r.userid for r in replies])
    return [ReplyOut.from_model(r, users.get(r.userid)) for r in replies]


@router.post("/{commentid}/replies", response_model=ReplyOut, summary="回复评论")
def create_reply(commentid: int, data: ReplyCreate, db: Session = Depends(get_db)):
    reply = comment_service.create_reply(db, commentid, data)
    return ReplyOut.from_model(reply, user_map(db, [reply.userid]).get(reply.userid))
