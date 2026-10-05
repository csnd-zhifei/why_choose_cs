"""笔记接口（对应 posts 表）"""
from typing import Literal, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, File, Query, UploadFile
from sqlmodel import Session

from backend.core import storage
from backend.core.config import settings
from backend.db.session import get_db
from backend.schemas.post import PostCreate, PostListOut, PostOut, PostUpdate
from backend.services import ai_service, post_service
from backend.services._enrich import user_map

router = APIRouter()

SortOrder = Literal["new", "hot"]


def _list_out(db: Session, total: int, page: int, size: int, posts) -> PostListOut:
    authors = user_map(db, [p.userid for p in posts])
    return PostListOut(
        total=total,
        page=page,
        size=size,
        items=[PostOut.from_model(p, authors.get(p.userid)) for p in posts],
    )


@router.get("", response_model=PostListOut, summary="笔记列表/搜索")
def list_posts(
    q: Optional[str] = Query(default=None, description="模糊匹配标题/简介/摘要"),
    userid: Optional[int] = Query(default=None, description="只看某个用户的笔记"),
    sort: SortOrder = Query(default="new", description="new=按时间，hot=按热度"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total, posts = post_service.list_posts(
        db, q=q, page=page, size=size, userid=userid, sort=sort
    )
    return _list_out(db, total, page, size, posts)


@router.get("/bookmarks", response_model=PostListOut, summary="我的收藏")
def list_bookmarks(
    userid: int = Query(...),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total, posts = post_service.list_bookmarked_posts(db, userid, page=page, size=size)
    return _list_out(db, total, page, size, posts)


@router.get("/{postid}", response_model=PostOut, summary="笔记详情")
def get_post(postid: int, db: Session = Depends(get_db)):
    post = post_service.get_post(db, postid)
    authors = user_map(db, [post.userid])
    return PostOut.from_model(post, authors.get(post.userid))


@router.post("", response_model=PostOut, summary="发布笔记")
def create_post(
    data: PostCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    post = post_service.create_post(db, data)
    # 摘要 + SPA 异步生成，前端轮询详情看 ready
    background_tasks.add_task(ai_service.generate_for_post, post.postid)
    return PostOut.from_model(post, user_map(db, [post.userid]).get(post.userid))


@router.patch("/{postid}", response_model=PostOut, summary="编辑笔记")
def update_post(
    postid: int,
    data: PostUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    post = post_service.update_post(db, postid, data)
    background_tasks.add_task(ai_service.generate_for_post, post.postid)
    return PostOut.from_model(post, user_map(db, [post.userid]).get(post.userid))


@router.delete("/{postid}", summary="删除笔记（软删）")
def delete_post(postid: int, db: Session = Depends(get_db)):
    post_service.delete_post(db, postid)
    return {"ok": True}


@router.post("/{postid}/md", response_model=PostOut, summary="上传笔记 md")
def upload_md(
    postid: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    post = post_service.get_post(db, postid)  # 先确认笔记存在
    url = storage.save_upload(
        file,
        settings.static_dir / "md",
        str(post.postid),
        storage.MARKDOWN_EXT,
        settings.md_max_mb,
        force_ext=".md",
    )
    post = post_service.set_markdown(db, postid, url)
    # 正文换了，重新生成摘要和 SPA
    background_tasks.add_task(ai_service.generate_for_post, post.postid)
    return PostOut.from_model(post, user_map(db, [post.userid]).get(post.userid))


@router.post("/{postid}/html", response_model=PostOut, summary="上传笔记 html")
def upload_html(
    postid: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    post = post_service.get_post(db, postid)
    url = storage.save_upload(
        file,
        settings.static_dir / "html",
        str(post.postid),
        storage.HTML_EXT,
        settings.html_max_mb,
        force_ext=".html",
    )
    post = post_service.set_html(db, postid, url)
    return PostOut.from_model(post, user_map(db, [post.userid]).get(post.userid))


@router.post("/{postid}/like", summary="点赞/取消点赞")
def toggle_like(postid: int, userid: int = Query(...), db: Session = Depends(get_db)):
    is_like, like_tot = post_service.toggle_like(db, postid, userid)
    return {"is_like": is_like, "like_tot": like_tot}


@router.post("/{postid}/bookmark", summary="收藏/取消收藏")
def toggle_bookmark(
    postid: int, userid: int = Query(...), db: Session = Depends(get_db)
):
    is_bookmark, bookmark_tot = post_service.toggle_bookmark(db, postid, userid)
    return {"is_bookmark": is_bookmark, "bookmark_tot": bookmark_tot}
