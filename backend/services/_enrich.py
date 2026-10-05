"""批量补充作者/用户信息，避免 N+1 查询"""
from sqlmodel import Session, select

from backend.db.models import User


def user_map(session: Session, userids) -> dict[int, User]:
    """按 id 批量取用户，返回 {userid: User}。空集合直接返回空 dict。"""
    ids = {i for i in userids if i is not None}
    if not ids:
        return {}
    return {
        u.userid: u
        for u in session.exec(select(User).where(User.userid.in_(ids))).all()
    }
