<p align="center" class="trendshift">
  <a href="https://trendshift.io/repositories/14130" target="_blank">
    <img src="https://trendshift.io/api/badge/repositories/14130" alt="Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/>
  </a>
</p>
<p align="center">
  <a href="https://github.com/huangjunsen0406/py-xiaozhi/releases/latest">
    <img src="https://img.shields.io/github/v/release/huangjunsen0406/py-xiaozhi?style=flat-square&logo=github&color=blue" alt="Release"/>
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License: MIT"/>
  </a>
  <a href="https://github.com/huangjunsen0406/py-xiaozhi/stargazers">
    <img src="https://img.shields.io/github/stars/huangjunsen0406/py-xiaozhi?style=flat-square&logo=github" alt="Stars"/>
  </a>
  <a href="https://github.com/huangjunsen0406/py-xiaozhi/releases/latest">
    <img src="https://img.shields.io/github/downloads/huangjunsen0406/py-xiaozhi/total?style=flat-square&logo=github&color=52c41a1&maxAge=86400" alt="Download"/>
  </a>
  <a href="https://gitee.com/huang-jun-sen/py-xiaozhi">
    <img src="https://img.shields.io/badge/Gitee-FF5722?style=flat-square&logo=gitee" alt="Gitee"/>
  </a>
  <a href="https://huangjunsen0406.github.io/py-xiaozhi/guide/00_%E6%96%87%E6%A1%A3%E7%9B%AE%E5%BD%95.html">
    <img alt="使用文档" src="https://img.shields.io/badge/使用文档-点击查看-blue?labelColor=2d2d2d" />
  </a>
  <a href="https://atomgit.com/huangjunsen0406/py-xiaozhi">
    <img src="./assets/AtomGit.svg" alt="AtomGit" height="20"/>
  </a>
</p>

简体中文 | [English](README.en.md)

## OpenClaw + 小智语音桥接版

本仓库是在 `py-xiaozhi` 基础上增加的 OpenClaw 语音桥接版本。小智负责唤醒、语音识别、对话和 TTS 播放；OpenClaw 作为本机能力后端，通过 MCP 工具被小智调用。

当前新增能力：

- 注册 `self.openclaw.ask`，把指定问题交给本机 OpenClaw agent 处理。
- 注册 `self.openclaw.status`，检查 OpenClaw CLI 与 Gateway 是否可用。
- 支持 Windows 隐藏后台启动、单实例保护，避免同时跑两个小智。
- 默认关闭空闲永久重连，降低后台 CPU 与日志负载。
- 使用小智云端 TTS，不使用 Windows SAPI 本地音色。

### 安装准备

需要 Windows 10/11、麦克风、扬声器、稳定网络，以及已安装并激活的 OpenClaw。建议先确认 OpenClaw Gateway 正常：

```powershell
openclaw --version
openclaw gateway status --json
```

如果 `rpc.ok` 为 `true`，说明本机 OpenClaw Gateway 可被本项目调用。

### 安装步骤

```powershell
git clone https://github.com/KERWINLAW/openclaw-xiaozhi-bridge.git
cd openclaw-xiaozhi-bridge
.\scripts\setup_xiaozhi.ps1
.\scripts\check_xiaozhi_setup.ps1
```

`setup_xiaozhi.ps1` 会使用 `uv sync --extra gui --python 3.12` 创建本地 `.venv`，并把 Python 运行时、缓存和小智运行数据留在项目目录内。若本机没有 `uv`，请先按 [uv 官方文档](https://docs.astral.sh/uv/) 安装。

检查脚本应看到：

```text
python_ok=true
openclaw_tool_registered=true
openclaw_status_registered=true
```

### 首次激活

首次运行不要跳过激活：

```powershell
.\scripts\run_xiaozhi_cli.ps1 -Mode cli
```

根据终端或弹出的激活提示完成小智设备激活。激活成功后，日常启动可以使用 `-SkipActivation`。

### 启动方式

图形界面：

```powershell
.\scripts\run_xiaozhi_cli.ps1 -Mode gui -SkipActivation
```

命令行界面：

```powershell
.\scripts\run_xiaozhi_cli.ps1 -Mode cli -SkipActivation
```

隐藏后台模式：

```text
start_xiaozhi_hidden.vbs
```

停止后台小智：

```text
stop_xiaozhi.bat
```

隐藏模式会启用 headless UI、单实例锁和低占用默认配置。重复启动时，第二个进程会自动退出，不会再生成两个小智监听器。

### 使用方式

普通聊天、天气、音乐等能力直接对小智说即可。需要让本机 OpenClaw 介入时，语音里明确点名 OpenClaw：

```text
你好小智，问 OpenClaw：现在 OpenClaw 网关状态是否正常
```

```text
你好小智，让 OpenClaw 帮我总结当前项目的启动方式
```

```text
你好小智，把这个交给 OpenClaw：检查这个项目有没有后台重复启动风险
```

实际调用链：

```text
语音唤醒 -> 小智识别与云端决策 -> MCP 工具 self.openclaw.ask/status
-> 本机 openclaw agent -> 结果回传小智 -> 小智 TTS 播放
```

复杂代码修改仍建议在 Codex/OpenClaw 窗口中完成；语音桥接更适合状态查询、轻量任务、语音触发和把明确任务转交给 OpenClaw。

### 常用排查

检查小智依赖和 MCP 工具：

```powershell
.\scripts\check_xiaozhi_setup.ps1
```

检查 OpenClaw Gateway：

```powershell
openclaw gateway status --json
```

停止可能残留的小智后台：

```powershell
.\scripts\stop_xiaozhi.ps1
```

项目运行数据在 `.runtime\data`，虚拟环境在 `.venv`，这些本地目录不会提交到 Git。

## 项目简介

py-xiaozhi 是一个使用 Python 实现的小智语音客户端，旨在通过代码学习和在没有硬件条件下体验 AI 小智的语音功能。
本仓库是基于 [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) 移植。

> **重要提示**
> - 请先阅读 [项目文档](https://huangjunsen0406.github.io/py-xiaozhi/)，启动教程和配置说明都在里面
> - main 是最新代码，每次更新后请重新安装 pip 依赖
> - **如果你已经基于本项目进行了二次开发，请不要直接合并最新代码**，新版本架构已大幅重构，强行合并会导致大量冲突。建议以旧版本为基础继续维护，或参考新架构重新适配
> - [从零开始使用小智客户端（视频教程）](https://www.bilibili.com/video/BV1dWQhYEEmq/)

## 演示

- [Bilibili 演示视频](https://www.bilibili.com/video/BV1HmPjeSED2/)

![系统界面](./documents/docs/guide/images/系统界面.png)

## 功能特点

- **AI 语音交互** — 语音输入与识别，自然流畅的对话体验
- **视觉多模态** — 图像识别和处理，理解图像内容
- **智能唤醒** — 多种唤醒词激活，免手动操作（可配置）
- **自动对话模式** — 连续对话，提升交互流畅度
- **MCP 工具生态** — 音乐播放、摄像头、截图、应用管理、天气查询、音量控制
- **Opus 编解码** — 音频编解码和实时重采样
- **唤醒词检测** — 基于 Sherpa-ONNX 离线识别，支持多唤醒词和拼音匹配
- **多界面模式** — GUI（PySide6 + QML）/ CLI / GPIO，适应不同环境
- **系统托盘 & 全局快捷键** — 后台运行，快捷操作
- **WebSocket / MQTT** — 双协议通信，支持 WSS 加密传输
- **设备激活** — v1/v2 双协议，自动验证码和设备指纹
- **跨平台** — Windows 10+ / macOS 10.15+ / Linux

## 相关项目

- [xiaozhi-desktop](https://github.com/huangjunsen0406/xiaozhi-desktop) — Electron 桌面版，支持 AEC 回声消除、Live2D、悬浮窗等显示模式，提供 Windows / macOS 安装包

## 快速开始

**环境要求**：Python >= 3.10，麦克风和扬声器，稳定网络连接

```bash
# 克隆项目
git clone https://github.com/huangjunsen0406/py-xiaozhi.git
cd py-xiaozhi

# 基础安装（CLI / GPIO 模式）
uv sync                        # 推荐
# 或: pip install -e .

# GUI 模式（额外安装 PySide6 + qasync）
uv sync --extra gui            # 推荐
# 或: pip install -e '.[gui]'

# 运行
python main.py                 # GUI 模式（默认）
python main.py --mode cli      # CLI 模式
python main.py --protocol mqtt # MQTT 协议
```

## 项目结构

```
py-xiaozhi/
├── main.py                     # 应用程序主入口
├── src/
│   ├── bootstrap/              # 应用引导与依赖注入
│   ├── core/                   # 核心基础设施（事件总线、状态管理等）
│   ├── plugins/                # 插件系统（音频、UI、MCP、唤醒词、快捷键）
│   ├── protocols/              # 通信协议（WebSocket / MQTT）
│   ├── audio_codecs/           # 音频编解码
│   ├── audio_processing/       # 唤醒词检测
│   ├── activation/             # 设备激活
│   ├── mcp/                    # MCP 工具系统
│   │   └── tools/              # 工具模块（music/camera/screenshot/app/weather/volume）
│   ├── ui/                     # 用户界面
│   │   ├── gui/                # PySide6 + QML 图形界面
│   │   ├── cli/                # 命令行界面
│   │   └── gpio/               # GPIO 嵌入式界面
│   └── utils/                  # 工具函数
├── libs/                       # 第三方原生库（libopus / webrtc_apm）
├── models/                     # 语音唤醒模型
├── documents/                  # VitePress 文档站
└── pyproject.toml              # 项目配置
```

## 状态流转

```
                    +----------------+
                    |                |
                    v                |
+------+  唤醒/按钮  +------------+  |   +------------+
| IDLE | ---------> | CONNECTING | -+-> | LISTENING  |
+------+            +------------+      +------------+
   ^                                          |
   |                                          | 语音识别完成
   |        +------------+                    v
   +------- |  SPEAKING  | <-----------------+
    完成播放 +------------+
```

## 贡献指南

欢迎提交 Issue 和 PR，请确保：

1. 代码风格符合 PEP8 规范
2. PR 包含适当的测试
3. 更新相关文档

## 感谢

> 排名不分前后

[Xiaoxia](https://github.com/78)
[zhh827](https://github.com/zhh827)
[四博智联-李洪刚](https://github.com/SmartArduino)
[HonestQiao](https://github.com/HonestQiao)
[vonweller](https://github.com/vonweller)
[孙卫公](https://space.bilibili.com/416954647)
[isamu2025](https://github.com/isamu2025)
[Rain120](https://github.com/Rain120)
[kejily](https://github.com/kejily)
[电波bilibili君](https://space.bilibili.com/119751)
[赛搏智能](https://shop115087494.m.taobao.com/?refer=https%3A%2F%2Fm.tb.cn%2F)

## 赞助支持

<div align="center">
  <p>感谢所有赞助者的支持，无论是接口资源、设备兼容测试还是资金支持，每一份帮助都让项目更加完善</p>
  <a href="https://huangjunsen0406.github.io/py-xiaozhi/sponsors/" target="_blank">
    <img src="https://img.shields.io/badge/查看-赞助者名单-brightgreen?style=for-the-badge&logo=github" alt="赞助者名单">
  </a>
  <a href="https://huangjunsen0406.github.io/py-xiaozhi/sponsors/" target="_blank">
    <img src="https://img.shields.io/badge/成为-项目赞助者-orange?style=for-the-badge&logo=heart" alt="成为赞助者">
  </a>
</div>

## 项目统计

[![Star History Chart](https://api.star-history.com/svg?repos=huangjunsen0406/py-xiaozhi&type=Date)](https://www.star-history.com/#huangjunsen0406/py-xiaozhi&Date)

## 许可证

[MIT License](LICENSE)
