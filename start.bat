@echo off
rem CS-why-choose one-click start: backend(8000) + frontend(5173)
cd /d "%~dp0"

if not exist .venv (
  echo [1/4] Creating virtualenv .venv (python 3.12)
  uv venv --python 3.12
) else (
  echo [1/4] virtualenv already exists
)

echo [2/4] Installing backend deps
uv pip install -r requirements.txt

if not exist frontend\node_modules (
  echo [3/4] Installing frontend deps
  pushd frontend
  call npm install
  popd
) else (
  echo [3/4] frontend deps ready
)

echo [4/4] Starting: backend http://localhost:8000 · frontend http://localhost:5173

start "cs-why-backend" cmd /k "uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

cd frontend
call npm run dev
