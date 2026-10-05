#!/usr/bin/env bash
# CS-为啥选 一键启动：后端(8000) + 前端(5173)
# 用法：bash start.sh  （或 chmod +x start.sh 后 ./start.sh）
set -euo pipefail
cd "$(dirname "$0")"

# ---- 1. 后端虚拟环境 + 依赖 ----
if [ ! -d .venv ]; then
  echo "[1/4] 创建虚拟环境 .venv (python 3.12)"
  uv venv --python 3.12
else
  echo "[1/4] 虚拟环境已存在"
fi

echo "[2/4] 安装后端依赖"
uv pip install -q -r requirements.txt

# ---- 2. 前端依赖 ----
if [ ! -d frontend/node_modules ]; then
  echo "[3/4] 安装前端依赖"
  (cd frontend && npm install)
else
  echo "[3/4] 前端依赖已就绪"
fi

echo "[4/4] 启动服务：后端 http://localhost:8000 · 前端 http://localhost:5173"
echo "      按 Ctrl+C 停止全部"

# 后端后台运行，前端前台运行
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACK_PID=$!

(cd frontend && npm run dev) &
FRONT_PID=$!

cleanup() {
  kill "$BACK_PID" "$FRONT_PID" 2>/dev/null || true
}
trap cleanup INT TERM EXIT

# 等前端（前台进程）结束，随后触发 cleanup 关掉后端
wait "$FRONT_PID"
