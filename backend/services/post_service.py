"""笔记业务逻辑"""
from datetime import datetime
from typing import Optional

from sqlalchemy import text
from sqlmodel import Session, col, func, select

from backend.core.config import settings
from backend.core.exceptions import BadRequestError, NotFoundError
from backend.core.ids import gen_id
from backend.db.models import Post, Record, User
from backend.schemas.post import PostCreate, PostUpdate


def get_post(session: Session, postid: int) -> Post:
    """取笔记，不存在或已软删直接抛 404"""
    post = session.get(Post, postid)
    if post is None or post.is_deleted:
        raise NotFoundError("笔记不存在")
    return post


def _hot_score():
    """HN 式热度分：(点赞数 - 1) / (发布至今小时数 + offset) ^ gravity

    时间在变，分数是连续变化的，所以每次查询现算、不落库。
    分值为负（点赞 0 时）不影响排序，只影响绝对大小。
    """
    age_hours = func.timestampdiff(text("HOUR"), Post.create_time, func.now())
    return (func.coalesce(Post.like_tot, 0) - 1) / func.pow(
        age_hours + settings.hot_offset, settings.hot_gravity
    )


def list_posts(
    session: Session,
    q: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    userid: Optional[int] = None,
    sort: str = "new",
) -> tuple[int, list[Post]]:
    """列表 + 分页。q 对 title/intro/summary 模糊匹配，userid 过滤某人的笔记

    sort=new 按发布时间倒序；sort=hot 按热度分倒序，且只统计时间窗口内的笔记
    """
    where = [Post.is_deleted == 0]
    if userid is not None:
        where.append(Post.userid == userid)
    if q:
        pattern = f"%{q}%"
        where.append(
            col(Post.title).like(pattern)
            | col(Post.intro).like(pattern)
            | col(Post.summary).like(pattern)
        )

    if sort == "hot":
        # 热度榜只看近期内容：限定时间窗口，让 MySQL 走 (is_deleted, create_time) 索引
        # 先缩小扫描范围，再对窗口内的行排序，避免全表 filesort
        if settings.hot_window_days > 0:
            cutoff = func.now() - text(f"INTERVAL {settings.hot_window_days} DAY")
            where.append(Post.create_time >= cutoff)
        order = _hot_score().desc()
    else:
        order = col(Post.create_time).desc()

    total = session.exec(select(func.count()).select_from(Post).where(*where)).one()
    stmt = select(Post).where(*where).order_by(order)
    return total, list(session.exec(stmt.offset((page - 1) * size).limit(size)).all())


def list_bookmarked_posts(
    session: Session, userid: int, page: int = 1, size: int = 20
) -> tuple[int, list[Post]]:
    """某用户收藏的笔记，按收藏时间倒序"""
    where = [Record.userid == userid, Record.is_bookmark == 1, Post.is_deleted == 0]
    joined = select(Post).join(Record, Record.postid == Post.postid).where(*where)

    total = session.exec(
        select(func.count()).select_from(Post).join(
            Record, Record.postid == Post.postid
        ).where(*where)
    ).one()
    stmt = joined.order_by(col(Record.create_time).desc())
    return total, list(session.exec(stmt.offset((page - 1) * size).limit(size)).all())


def create_post(session: Session, data: PostCreate) -> Post:
    if session.get(User, data.userid) is None:
        raise BadRequestError("用户不存在")

    post = Post(
        postid=gen_id(),
        userid=data.userid,
        title=data.title,
        intro=data.intro,
        summary="",  # 由 ai_service 后台回填
        mdurl=data.mdurl,
        comment_tot=0,
        like_tot=0,
        bookmark_tot=0,
        is_deleted=0,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def set_markdown(session: Session, postid: int, url: str) -> Post:
    """上传 md 后回写 mdurl。正文变了，摘要和旧 html 一并清空，等 AI 重新生成"""
    post = get_post(session, postid)
    post.mdurl = url
    post.summary = ""
    post.htmlurl = None
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def set_html(session: Session, postid: int, url: str) -> Post:
    """上传 html 后回写 htmlurl。它是可展示的成品，不影响摘要"""
    post = get_post(session, postid)
    post.htmlurl = url
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def update_post(session: Session, postid: int, data: PostUpdate) -> Post:
    post = get_post(session, postid)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)
    # 正文变了，摘要和 SPA 需要重新生成
    post.summary = ""
    post.htmlurl = None
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def delete_post(session: Session, postid: int) -> None:
    post = get_post(session, postid)
    post.is_deleted = 1
    session.add(post)
    session.commit()


def _toggle(session: Session, postid: int, userid: int, field: str, counter: str):
    """点赞/收藏的通用 toggle：翻转 record 标记并同步 posts 里的计数"""
    post = get_post(session, postid)

    record = session.exec(
        select(Record).where(Record.postid == postid, Record.userid == userid)
    ).first()
    if record is None:
        now = datetime.now()
        record = Record(postid=postid, userid=userid, create_time=now, update_time=now)
        session.add(record)

    new_value = 0 if getattr(record, field) else 1
    setattr(record, field, new_value)
    record.update_time = datetime.now()

    current = getattr(post, counter) or 0
    setattr(post, counter, max(0, current + (1 if new_value else -1)))

    session.add(post)
    session.commit()
    return bool(new_value), getattr(post, counter)


def toggle_like(session: Session, postid: int, userid: int) -> tuple[bool, int]:
    return _toggle(session, postid, userid, "is_like", "like_tot")


def toggle_bookmark(session: Session, postid: int, userid: int) -> tuple[bool, int]:
    return _toggle(session, postid, userid, "is_bookmark", "bookmark_tot")
