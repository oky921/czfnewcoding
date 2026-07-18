# Backend

会议纪要整理器后端，使用 Python + FastAPI。

## 启动

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 接口

- `GET /health`：健康检查
- `POST /api/minutes/parse`：解析会议文本

当前解析逻辑仅包含基础规则和正则，后续可逐步扩展。
