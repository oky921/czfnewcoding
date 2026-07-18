# MewCode

MewCode 是一个面向开发者的终端 AI 编码助手，基于 Python 和 Textual 构建。
它支持交互式终端 UI、非交互 prompt 执行、模型提供商接入、权限控制、会话记忆、MCP 多 agent 协作等功能。

## 目录

- [功能](#功能)
- [功能展示](#功能展示)
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

## 功能展示

### 1. 项目过程与结果

下面按截图顺序，简单记录这次项目从需求确认到最终落地的完整过程。

1. 先明确了会议纪要整理器的目标和技术路线，前端采用 Vue 3 + Vite + TypeScript，后端采用 Python + FastAPI，整体走前后端分离方案。

   ![项目过程 1](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717224256144.png)

2. 随后开始搭建项目骨架，先创建基础目录、README 和依赖文件，把工程最小运行框架先立起来。

   ![项目过程 2](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717224240040.png)

3. 后端部分继续补齐入口文件、数据结构定义和会议文本解析逻辑，为后续接口开发做准备。

   ![项目过程 3](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717225038183.png)

4. 前端部分同步搭建主入口和页面结构，把会议整理的交互页面先跑通，方便后续联调。

   ![项目过程 4](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717225049412.png)

5. 在核心能力上补充会议纪要解析与格式化输出，让后端能够先把原始会议文本转成可用结构。

   ![项目过程 5](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717225926206.png)

6. 再把前后端的调用路径和目录职责理顺，确保页面、接口和解析逻辑各自独立，便于维护。

   ![项目过程 6](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717225939495.png)

7. 项目说明文档也一并整理，补充了启动方式、目录结构和基本使用说明，方便后续接手和部署。

   ![项目过程 7](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717225946364.png)

8. 随着工程逐步成型，继续完善了配置示例和依赖说明，让项目可以更清晰地被复现和启动。

   ![项目过程 8](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717225954094.png)

9. 最终阶段对整体结果做了收尾展示，确认前后端分离结构、基础页面和后端接口都已经落地。

   ![项目过程 9](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717230653007.png)

10. 过程中也补充了运行环境要求，特别是 Node.js 版本和相关工具链，避免启动时因为环境不一致而报错。

    ![项目过程 10](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717230703933.png)

11. 整体来看，项目已经形成了可继续迭代的完整雏形，后续可以在此基础上继续补强业务规则和解析能力。

    ![项目过程 11](C:\Users\22879\AppData\Roaming\Typora\typora-user-images\image-20260717230716356.png)

### 2. 简历解析与面试题生成

MewCode 支持通过 skill 机制加载特定领域的智能体能力。例如 `backend-interview` skill 可以解析候选人简历，并自动生成三轮针对性技术面试题，帮助招聘方快速进入面试准备阶段。

<img width="1461" height="616" alt="07dd34ff063b372195a34700791ba638" src="https://github.com/user-attachments/assets/6d6ec783-e92a-499d-b932-06a887e447dc" />
<img width="1400" height="317" alt="6a99f7dd40badf415772c10551c9c3cf" src="https://github.com/user-attachments/assets/1ab70107-ca3d-4fb7-91e3-bc9eb91dc51a" />
<img width="1801" height="792" alt="d13c4110060a48305fde4e5124e1f665" src="https://github.com/user-attachments/assets/11bf2774-df11-4e75-b030-6ce23ea65077" />

### 3. 快捷指令系统

通过 `/` 前缀可以快速调用内置指令，例如清空对话历史、压缩上下文、生成规范 commit 信息等。所有指令均支持自动补全和提示，提升终端操作效率。

<img width="1872" height="265" alt="bb4c5cf3cd32cd994144a111fb7492a1" src="https://github.com/user-attachments/assets/4d285e55-2a0e-4e8e-af14-e25064028eea" />

### 4. MCP 服务器集成

MewCode 内置 MCP（Model Context Protocol）客户端，支持接入第三方 MCP 服务器（如 Context7），扩展模型的知识获取和工具调用能力。MCP 服务器状态可通过 `--mcp` 命令查看。
<img width="1897" height="1031" alt="30ce8048b2f9483009d3eea636977c06" src="https://github.com/user-attachments/assets/ad1d3f3a-266b-4399-b2fd-00222cf947f9" />

### 5. 非交互模式执行

除了完整的终端 UI，MewCode 也支持非交互模式，通过 `-p` 参数直接传入 prompt，快速完成单次问答或任务执行，适合脚本集成和自动化场景。
<img width="768" height="58" alt="6879956cbbe4cc9cdd52db472a6c3471" src="https://github.com/user-attachments/assets/b7ec9c73-af40-4ffe-ada1-081fdef0fd9a" />

### 6. 多 Agent 团队协作

MewCode 内置了完整的 Agent 团队协作框架，支持：
- 协调者（Coordinator）创建团队并注册成员
- 工具集按角色动态过滤（四层权限控制）
- 成员间通过任务系统和邮箱进行异步通信
- 子任务拆分与结果汇总

内置 Agent 类型包括 Explore、Plan、general-purpose 等，并支持自定义 Agent 加载。系统已验证通过多 Agent 协作流程的端到端测试。

<img width="1828" height="865" alt="278db6a40b9689df499a3c8603e38857" src="https://github.com/user-attachments/assets/b162abf9-97dd-45ea-a937-006d0c246c2f" />
<img width="1812" height="785" alt="06cd9fbb3d1d4e7bc685b46784556301" src="https://github.com/user-attachments/assets/c36e17b0-f376-4f69-bae5-14916a70c63c" />
<img width="1071" height="705" alt="0f4298242fe0e9b4f4f91a86cb596842" src="https://github.com/user-attachments/assets/ef5ed905-3838-4c8c-8f55-768e6fb75aad" />
<img width="1063" height="717" alt="9e338ad2ecd5830b643bb41ddd6bebd7" src="https://github.com/user-attachments/assets/f2f091ac-d37d-41e9-a4c4-b4e83638e878" />


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

