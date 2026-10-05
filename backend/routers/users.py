"""用户接口"""
from fastapi import APIRouter, Depends, File, UploadFile
from sqlmodel import Session

from backend.core import storage
from backend.core.config import settings
from backend.db.session import get_db
from backend.schemas.user import UserCreate, UserLogin, UserOut, UserUpdate
from backend.services import user_service

router = APIRouter()


@router.post("/register", response_model=UserOut, summary="注册")
def register(data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.post("/login", summary="登录")
def login(data: UserLogin, db: Session = Depends(get_db)):
    # 暂不做鉴权，登录成功只回用户标识，后续接入 token 时在这里签发
    user = user_service.login(db, data.username, data.password)
    return {"userid": user.userid, "username": user.username, "avatar": user.avatar}


@router.get("/{userid}", response_model=UserOut, summary="用户公开资料")
def get_user(userid: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, userid)


@router.patch("/{userid}", response_model=UserOut, summary="修改资料")
def update_user(userid: int, data: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, userid, data)


@router.post("/{userid}/avatar", response_model=UserOut, summary="上传头像")
def upload_avatar(
    userid: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    user = user_service.get_user(db, userid)  # 先确认用户存在，避免为幽灵用户写文件
    url = storage.save_upload(
        file,
        settings.static_dir / "avatar",
        str(user.userid),
        storage.AVATAR_EXT,
        settings.avatar_max_mb,
    )
    return user_service.update_user(db, userid, UserUpdate(avatar=url))
