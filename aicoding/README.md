# Meeting Minutes Organizer

会议纪要整理器，采用前后端分离架构。

- 前端：Vue 3 + Vite + TypeScript
- 后端：Python + FastAPI
- 解析方式：不接入大模型，后端通过规则和正则解析会议文本

## 目录结构

```text
aicoding/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── parser.py
│   │   └── schemas.py
│   ├── pyproject.toml
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── api.ts
│   │   ├── main.ts
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── .gitignore
└── README.md
```

## 后端启动

进入后端目录：

```bash
cd aicoding/backend
```

创建并激活虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate
```

安装依赖：

```bash
pip install -e .
```

启动服务：

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

后端接口文档：

- http://127.0.0.1:8000/docs
- 健康检查：`GET /health`
- 会议文本解析：`POST /api/minutes/parse`

## 前端启动

进入前端目录：

```bash
cd aicoding/frontend
```

安装依赖：

```bash
npm install
```

启动开发服务：

```bash
npm run dev
```

默认访问：

- http://127.0.0.1:5173

前端开发服务器已配置 `/api` 代理到后端 `http://127.0.0.1:8000`。

## 当前功能范围

当前版本仅提供项目骨架和基础接口：

- 前端提供会议文本输入框和解析结果展示区域
- 后端提供基础文本解析接口
- 解析逻辑暂时只做轻量规则处理，不实现复杂纪要提取
