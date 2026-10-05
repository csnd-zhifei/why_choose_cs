# main.py - FastAPI 应用入口点
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.core.config import settings
from backend.core.exceptions import AppError
from backend.routers import book, comments, users

app = FastAPI(
    title="CS-为啥选",
    description="“你为什么选择CS？”这是一个给CS学生、结合各自经历、分享CS思考、看法、观点的网站。",
    version="1.0.0",
)

# 配置 CORS（跨域资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 上传文件与 AI 生成的 SPA 页面都在这里，统一通过 /static 暴露
STATIC_DIR = settings.static_dir
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 业务异常统一转成 HTTP 响应
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# 注册路由（Route）
app.include_router(users.router, prefix="/api/v1/users", tags=["用户"])
app.include_router(book.router, prefix="/api/v1/books", tags=["笔记"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["评论"])


# 根路径健康检查
@app.get("/")
async def root():
    return {"message": "欢迎使用 FastAPI 项目！"}


# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
