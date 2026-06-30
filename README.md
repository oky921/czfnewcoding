运行方式
进入项目目录并激活虚拟环境
cd D:\Drivers\mewcode-python
.\.venv\Scripts\Activate.ps1
如果你使用的不是 PowerShell，激活命令会不同：
cmd：.venv\Scripts\activate.bat
Git Bash：source .venv/Scripts/activate
安装依赖
python -m pip install -U pip
pip install -e .
配置模型信息
项目配置文件在 .mewcode/config.yaml，当前使用的是 OpenAI 兼容接口：
providers:
  - name: my_codex
    protocol: openai
    base_url: https://www.onetopai.com/v1
    api_key: ""
    model: gpt-5.4
运行前需要先设置环境变量：
$env:OPENAI_API_KEY="your_api_key"
启动项目
交互模式：
python -m mewcode
非交互测试：
python -m mewcode -p "Hello"
注意事项
Python 版本建议 3.11+
如果出现 Invalid API key，优先检查 OPENAI_API_KEY 是否正确
如果代理接口不支持 Responses API，可将 .mewcode/config.yaml 中的 protocol: openai 改为 protocol: openai-compat
项目默认启用了 context7 MCP，需要本机安装 Node.js
MCP 相关说明
项目默认会启动：
mcp_servers:
  - name: context7
    command: npx
    args: ["-y", "@upstash/context7-mcp"]
如果出现：
MCP warning: MCP server 'context7': Connection closed
通常是 Node.js 版本过低导致。建议使用：
nvm use 20.18.0
node -v
npx -y @upstash/context7-mcp
当看到下面这行输出时，说明 context7 启动成功：
Context7 Documentation MCP Server v3.2.2 running on stdio
如果暂时不需要 MCP，也可以先注释掉 .mewcode/config.yaml 中的 mcp_servers 配置。
<img width="613" height="255" alt="image" src="https://github.com/user-attachments/assets/7f66cd08-a922-4263-b1d8-a7346bc3580e" />

node.js需要到18+，或者使用nvm设置，如下：
<img width="1147" height="721" alt="image" src="https://github.com/user-attachments/assets/11492503-c3ed-4641-831b-75957c127735" />

