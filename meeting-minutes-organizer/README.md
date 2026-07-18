# Meeting Minutes Organizer

一个前后端分离的会议纪要整理器示例项目。

- 前端：Vue 3 + Vite + TypeScript
- 后端：Python + FastAPI
- 解析方式：规则和正则解析会议文本，不接入大模型

## 目录结构

```text
meeting-minutes-organizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── parser.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   ├── style.css
│   │   └── vite-env.d.ts
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   └── README.md
└── README.md
```

## 后端启动

进入后端目录：

```bash
cd backend
```

创建并激活虚拟环境：

```bash
python -m venv .venv
```

Windows PowerShell：

```bash
.venv\Scripts\Activate.ps1
```

安装依赖：

```bash
pip install -r requirements.txt
```

启动服务：

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

接口文档：

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## 前端启动

进入前端目录：

```bash
cd frontend
```

安装依赖：

```bash
npm install
```

启动开发服务：

```bash
npm run dev
```

默认访问地址：

- http://127.0.0.1:5173

## 当前功能

当前仅提供基础项目骨架和一个简单的规则解析接口：

- 支持提交会议文本
- 通过简单规则提取标题、参会人和待办项
- 暂未实现复杂 NLP 或大模型能力

## API 示例

```http
POST /api/minutes/parse
Content-Type: application/json

{
  "text": "会议标题：产品周会\n参会人：张三、李四\n待办：张三完成原型设计"
}
```
