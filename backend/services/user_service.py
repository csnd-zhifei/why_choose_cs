"""用户业务逻辑"""
from typing import Optional

from sqlmodel import Session, select

from backend.core.exceptions import BadRequestError, NotFoundError, UnauthorizedError
from backend.core.ids import gen_id
from backend.core.security import hash_password, verify_password
from backend.db.models import User
from backend.schemas.user import UserCreate, UserUpdate


def get_user(session: Session, userid: int) -> User:
    user = session.get(User, userid)
    if user is None or user.is_deleted:
        raise NotFoundError("用户不存在")
    return user


def get_by_username(session: Session, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username, User.is_deleted == 0)
    return session.exec(stmt).first()


def create_user(session: Session, data: UserCreate) -> User:
    if get_by_username(session, data.username) is not None:
        raise BadRequestError("用户名已存在")

    user = User(
        userid=gen_id(),
        username=data.username,
        password_hash=hash_password(data.password),
        avatar=data.avatar,
        gender=data.gender,
        user_location=data.user_location,
        is_deleted=0,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def login(session: Session, username: str, password: str) -> User:
    user = get_by_username(session, username)
    if user is None or not verify_password(password, user.password_hash):
        raise UnauthorizedError("用户名或密码错误")
    return user


def update_user(session: Session, userid: int, data: UserUpdate) -> User:
    user = get_user(session, userid)
    # exclude_unset：没传的字段不动
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
