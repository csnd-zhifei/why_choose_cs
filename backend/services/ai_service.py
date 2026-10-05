"""AI 生成摘要与单页 SPA

在 Post 创建/编辑后作为后台任务执行：调用 AI 生成 summary 和 html，
写盘到 backend/static/spa/{postid}.html，再把 htmlurl 回填到库里。
未配置 AI_API_KEY / AI_BASE_URL / AI_MODEL 时直接跳过，Post 保持 ready=False。
"""
import json
import logging
import urllib.request
from typing import Optional

from backend.core.config import settings
from backend.db.models import Post
from backend.db.session import engine
from backend.prompts.templates import SPA_PROMPT, SUMMARY_PROMPT
from sqlmodel import Session

logger = logging.getLogger(__name__)

SUMMARY_MAX_LEN = 2047
INTRO_MAX_LEN = 511  # posts.intro 的列长度，喂给 AI 时截断


def _chat(prompt: str, timeout: int = 120) -> str:
    api_key = settings.ai_api_key
    base_url = settings.ai_base_url.rstrip("/")
    model = settings.ai_model
    if not (api_key and base_url and model):
        raise RuntimeError(
            "未配置 AI 相关环境变量（AI_API_KEY / AI_BASE_URL / AI_MODEL）"
        )

    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
    ).encode()
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode())
    return body["choices"][0]["message"]["content"].strip()


def _strip_code_fence(html: str) -> str:
    """模型有时会多包一层 ```html，去掉"""
    if html.startswith("```"):
        html = html.split("\n", 1)[-1]
        html = html.rsplit("```", 1)[0]
    return html.strip()


def generate_for_post(postid: int) -> Optional[str]:
    """生成并回填；返回 htmlurl，失败/未配置时返回 None"""
    with Session(engine) as session:
        post = session.get(Post, postid)
        if post is None or post.is_deleted:
            return None
        title = post.title or ""
        intro = (post.intro or "")[:INTRO_MAX_LEN]

    try:
        summary = _chat(SUMMARY_PROMPT.format(title=title, intro=intro))[
            :SUMMARY_MAX_LEN
        ]
        html = _strip_code_fence(_chat(SPA_PROMPT.format(title=title, intro=intro)))
    except Exception:
        logger.exception("AI 生成失败 postid=%s", postid)
        return None

    settings.spa_dir.mkdir(parents=True, exist_ok=True)
    (settings.spa_dir / f"{postid}.html").write_text(html, encoding="utf-8")
    htmlurl = f"/static/spa/{postid}.html"

    with Session(engine) as session:
        post = session.get(Post, postid)
        if post is None:
            return None
        post.summary = summary
        post.htmlurl = htmlurl
        session.add(post)
        session.commit()
    return htmlurl
