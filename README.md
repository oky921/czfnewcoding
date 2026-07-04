# MewCode

MewCode 是一个面向开发者的终端 AI 编码助手，基于 Python 和 Textual 构建。
它支持交互式终端 UI、非交互 prompt 执行、模型提供商接入、权限控制、会话记忆、MCP 多 agent 协作等功能。

## 目录

- [功能](#功能)
- [快速开始](#快速开始)
- [配置](#配置)
- [运行方式](#运行方式)
- [项目结构](#项目结构)
- [注意事项](#注意事项)
- [环境要求](#环境要求)
- [调试与常见问题](#调试与常见问题)

## 功能

- 终端 AI 编码助手，支持交互式和非交互式运行
- 基于 `textual` 的终端界面，支持命令补全、历史记录、文件引用展开等
- 支持 OpenAI 兼容模型和 Anthropic 模型接入
- 权限控制与沙箱机制，限制危险命令执行
- 会话记忆与指令管理，支持持续上下文
- 多 agent / 团队模式，支持 MCP 协作和任务通知
- 可扩展工具系统与插件式命令注册
- 支持工作树管理和本地配置覆盖

## 快速开始

1. 进入项目目录：

```powershell
cd D:\Drivers\mewcode-python
```

2. 激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果你使用的不是 PowerShell：

- cmd：

```bat
.venv\Scripts\activate.bat
```

- Git Bash：

```bash
source .venv/Scripts/activate
```

3. 安装依赖：

```powershell
python -m pip install -U pip
pip install -e .
```

4. 配置模型接口：

在项目根目录下创建或编辑 `.mewcode/config.yaml`：

```yaml
providers:
  - name: my_codex
    protocol: openai
    base_url: https://www.onetopai.com/v1
    api_key: ""
    model: gpt-5.4
```

5. 设置环境变量：

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

## 运行方式

- 交互模式：

```powershell
python -m mewcode
```

- 非交互模式：

```powershell
python -m mewcode -p "Hello"
```

## 配置

项目主要配置文件位于 `.mewcode/config.yaml`。

### 模型提供商配置

```yaml
providers:
  - name: my_codex
    protocol: openai
    base_url: https://www.onetopai.com/v1
    api_key: ""
    model: gpt-5.4
```

- `protocol`: 可以是 `openai` 或 `openai-compat`
- `base_url`: 模型接口地址
- `api_key`: 可直接写入配置，也可通过环境变量 `OPENAI_API_KEY` 提供
- `model`: 模型名称

### MCP 配置

默认项目支持 `context7` MCP：

```yaml
mcp_servers:
  - name: context7
    command: npx
    args: ["-y", "@upstash/context7-mcp"]
```

如果你暂时不使用 MCP，可注释或删除 `.mewcode/config.yaml` 中的 `mcp_servers`。

## 项目结构

- `mewcode/__main__.py`: CLI 入口，解析参数并启动应用
- `mewcode/app.py`: 终端 UI 主程序，实现输入、输出和界面交互
- `mewcode/agent.py`: AI agent 运行流程、工具调用、权限请求等
- `mewcode/config.py`: 配置加载与校验
- `mewcode/client.py`: 模型客户端创建与错误处理
- `mewcode/tools/`: 工具注册与扩展命令实现
- `mewcode/teams/`: 多 agent / 协作机制
- `mewcode/memory/`: 会话与记忆管理
- `mewcode/mcp/`: MCP 服务器集成与通信
- `tests/`: 测试用例

## 注意事项

- 推荐 Python 版本：`3.11+`
- 运行前请确认 `OPENAI_API_KEY` 已正确设置
- 如果出现 `Invalid API key`，优先检查环境变量或配置文件中的 API key
- 如果代理接口不支持 Responses API，可将 `.mewcode/config.yaml` 中的 `protocol: openai` 改为 `protocol: openai-compat`

## 环境要求

- Python 3.11 或更高版本
- `node.js` 18+（仅在启用 MCP 时需要）
- `npx` 可用，用于启动 MCP server

## 调试与常见问题

### MCP 连接失败

如果出现：

```text
MCP warning: MCP server 'context7': Connection closed
```

通常是 Node.js 版本过低，可以尝试：

```bash
nvm use 20.18.0
node -v
npx -y @upstash/context7-mcp
```

成功启动时，你会看到类似：

```text
Context7 Documentation MCP Server v3.2.2 running on stdio
```

### 关闭 MCP

如果你不想使用 MCP，可以注释 `.mewcode/config.yaml` 中的 `mcp_servers` 配置段。

## 贡献指南

- 请使用英文提交信息
- 变量命名建议使用 `snake_case`
- 类型注释推荐使用 PEP 604 语法，如 `X | Y`
- 欢迎在 `tests/` 中添加测试用例

## 许可证

请根据项目实际情况补充 LICENSE 信息。



<img width="613" height="255" alt="image" src="https://github.com/user-attachments/assets/7f66cd08-a922-4263-b1d8-a7346bc3580e" />

node.js需要到18+，或者使用nvm设置，如下：
<img width="1147" height="721" alt="image" src="https://github.com/user-attachments/assets/11492503-c3ed-4641-831b-75957c127735" />

