"""业务异常

service 层直接抛这些异常，由 main.py 注册的处理器统一转成 HTTP 响应，
router 里不再出现 try/except 和 None 判断。
"""


class AppError(Exception):
    """所有业务异常的基类，响应体格式与 HTTPException 一致：{"detail": ...}"""

    status_code = 400

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class BadRequestError(AppError):
    """参数或业务校验不通过，如用户名重复、引用的用户不存在"""

    status_code = 400


class UnauthorizedError(AppError):
    """用户名或密码错误"""

    status_code = 401


class NotFoundError(AppError):
    """资源不存在或已软删"""

    status_code = 404
