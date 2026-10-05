"""本地上传文件的落盘与校验

文件名由调用方按资源 id 指定（不采用用户上传的原始文件名），
所以不存在路径穿越问题；扩展名走白名单，大小边读边限量。
"""
from pathlib import Path

from fastapi import UploadFile

from backend.core.config import settings
from backend.core.exceptions import BadRequestError

_CHUNK = 1024 * 1024

# 各资源的扩展名白名单
AVATAR_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
MARKDOWN_EXT = {".md", ".markdown"}
HTML_EXT = {".html", ".htm"}


def save_upload(
    upload: UploadFile,
    directory: Path,
    stem: str,
    allowed_ext: set[str],
    max_mb: int,
    force_ext: str | None = None,
) -> str:
    """保存上传文件，返回可访问的 url

    同名不同扩展名的旧文件会被删除（如头像从 .png 换成 .jpg）。
    写入先落到 .part 临时文件，成功后再改名，避免中途失败留下半个文件。
    """
    # 先校验上传文件本身的后缀，force_ext 只决定落盘用什么扩展名
    src_ext = Path(upload.filename or "").suffix.lower()
    if src_ext not in allowed_ext:
        raise BadRequestError(
            f"不支持的文件类型，只允许 {'/'.join(sorted(allowed_ext))}"
        )
    ext = force_ext or src_ext

    directory.mkdir(parents=True, exist_ok=True)
    dest = directory / f"{stem}{ext}"
    tmp = directory / f"{stem}{ext}.part"
    limit = max_mb * 1024 * 1024

    size = 0
    try:
        with tmp.open("wb") as f:
            while chunk := upload.file.read(_CHUNK):
                size += len(chunk)
                if size > limit:
                    raise BadRequestError(f"文件超过 {max_mb}MB 上限")
                f.write(chunk)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise

    for old in directory.glob(f"{stem}.*"):
        if old != tmp:
            old.unlink(missing_ok=True)
    tmp.replace(dest)

    return f"/static/{dest.relative_to(settings.static_dir).as_posix()}"
