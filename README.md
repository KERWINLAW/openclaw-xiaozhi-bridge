# OpenClaw Xiaozhi Voice Bridge

这是一个基于 `py-xiaozhi` 改造的 Windows 语音桥接项目。它把小智作为语音前台，把本机 OpenClaw 作为 MCP 工具后端，用语音把任务转交给 OpenClaw。

## 项目关系

小智负责：

- 唤醒词监听
- 语音识别
- 云端对话
- TTS 语音回复
- MCP 工具协商

OpenClaw 负责：

- 本机 OpenClaw agent 调用
- OpenClaw Gateway 状态检查
- Codex/OpenClaw 风格的本地任务处理

当前注册的 OpenClaw MCP 工具：

- `self.openclaw.ask`
- `self.openclaw.status`

普通聊天、天气、音乐等仍由小智处理。只有当你明确说到 OpenClaw、本机项目、代码分析、网关状态等任务时，小智才更容易选择 OpenClaw 工具。

## 当前特性

- Windows 本地运行，支持 GUI、CLI 和隐藏后台模式。
- 隐藏后台模式启用 headless UI，避免多余窗口。
- 单实例保护，重复启动时第二个小智会自动退出。
- 默认关闭空闲永久重连，降低后台 CPU 和日志负载。
- 唤醒词线程数默认较低，减少常驻资源占用。
- OpenClaw 回复会从 `openclaw agent --json` 输出中提取可读文本。
- 不使用 Windows SAPI 本地 TTS，语音回复来自小智 TTS。

## 安装准备

需要：

- Windows 10/11
- 麦克风和扬声器
- 稳定网络
- 已安装并激活的 OpenClaw
- `uv`

先确认 OpenClaw 可用：

```powershell
openclaw --version
openclaw gateway status --json
```

`openclaw gateway status --json` 中 `rpc.ok` 为 `true` 时，本项目可以调用本机 OpenClaw Gateway。

## 安装

```powershell
git clone https://github.com/KERWINLAW/openclaw-xiaozhi-bridge.git
cd openclaw-xiaozhi-bridge
.\scripts\setup_xiaozhi.ps1
.\scripts\check_xiaozhi_setup.ps1
```

`setup_xiaozhi.ps1` 会执行：

```powershell
uv sync --extra gui --python 3.12
```

本地运行目录：

- `.venv`：Python 虚拟环境
- `.uv-python`：项目内 Python 运行时
- `.uv-cache`：uv 缓存
- `.runtime\data`：小智激活信息、配置和日志

这些本地目录已被 `.gitignore` 忽略，不会上传到 GitHub。

检查脚本应看到：

```text
python_ok=true
openclaw_tool_registered=true
openclaw_status_registered=true
```

## 首次激活

首次运行不要跳过激活：

```powershell
.\scripts\run_xiaozhi_cli.ps1 -Mode cli
```

按终端或弹窗提示完成小智设备激活。激活成功后，日常启动可以加 `-SkipActivation`。

## 启动

GUI：

```powershell
.\scripts\run_xiaozhi_cli.ps1 -Mode gui -SkipActivation
```

CLI：

```powershell
.\scripts\run_xiaozhi_cli.ps1 -Mode cli -SkipActivation
```

隐藏后台：

```text
start_xiaozhi_hidden.vbs
```

隐藏后台会使用单实例锁。重复运行 `start_xiaozhi_hidden.vbs` 不会启动第二个监听器。

## 停止

```text
stop_xiaozhi.bat
```

或：

```powershell
.\scripts\stop_xiaozhi.ps1
```

## 使用方式

唤醒后，普通问题直接对小智说即可。

需要 OpenClaw 介入时，语音里明确点名 OpenClaw：

```text
你好小智，问 OpenClaw：现在 OpenClaw 网关状态是否正常
```

```text
你好小智，让 OpenClaw 帮我总结当前项目的启动方式
```

```text
你好小智，把这个交给 OpenClaw：检查这个项目有没有后台重复启动风险
```

调用链：

```text
语音唤醒
-> 小智识别和云端决策
-> MCP 工具 self.openclaw.ask/status
-> 本机 openclaw agent
-> 结果回传小智
-> 小智 TTS 播放
```

复杂代码修改仍建议在 Codex/OpenClaw 窗口中完成。这个桥接项目更适合语音触发、状态查询、轻量控制和把明确任务转交给 OpenClaw。

## 常用排查

检查依赖和 MCP 工具：

```powershell
.\scripts\check_xiaozhi_setup.ps1
```

检查 OpenClaw Gateway：

```powershell
openclaw gateway status --json
```

停止残留的小智后台：

```powershell
.\scripts\stop_xiaozhi.ps1
```

查看小智日志：

```powershell
Get-Content .\.runtime\data\logs\app.log -Tail 80
```

## 关键文件

- `src/mcp/tools/openclaw/_tools.py`：OpenClaw MCP 工具。
- `src/utils/single_instance.py`：单实例保护。
- `start_xiaozhi_hidden.vbs`：隐藏后台启动入口。
- `scripts/run_xiaozhi_cli.ps1`：PowerShell 启动入口。
- `scripts/stop_xiaozhi.ps1`：停止本项目小智后台。
- `OPENCLAW_XIAOZHI_PLAN.md`：本地集成说明。

## 上游来源

本项目基于开源项目 `py-xiaozhi` 二次开发，并保留其 MIT License。上游项目地址：

https://github.com/huangjunsen0406/py-xiaozhi

本仓库的 README 只描述当前 OpenClaw 语音桥接版本，不代表上游项目，也不包含上游名单或推广信息。

## 许可证

[MIT License](LICENSE)
