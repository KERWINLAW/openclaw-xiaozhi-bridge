# OpenClaw + Xiaozhi Voice Bridge

This workspace uses `py-xiaozhi` as the voice and MCP baseline for OpenClaw integration.

## Relationship

Xiaozhi is the voice front end:

- wake-word detection
- speech recognition
- cloud conversation
- TTS playback
- MCP tool negotiation

OpenClaw is exposed as local MCP tools:

- `self.openclaw.ask`
- `self.openclaw.status`

Normal chat remains Xiaozhi's own capability. OpenClaw participates when the Xiaozhi server chooses one of the OpenClaw MCP tools.

## Local Runtime

- Python 3.12 is installed under `.uv-python`.
- The virtual environment is `.venv`.
- Runtime data is redirected with `PY_XIAOZHI_DATA_DIR` to `.runtime/data`.
- `.runtime`, `.venv`, `.uv-cache`, and `.uv-python` are ignored by Git.
- `onnxruntime>=1.24.3` is used so Sherpa-ONNX can avoid the old `C:\Windows\System32\onnxruntime.dll` API mismatch.
- GUI mode requires the optional `gui` extra: `PySide6` and `qasync`.

## Validate

```powershell
cd C:\Users\KERWIN\Documents\Codex\2026-05-14\openclaw
.\scripts\setup_xiaozhi.ps1
.\scripts\check_xiaozhi_setup.ps1
```

## Run

CLI:

```text
start_xiaozhi_cli.bat
```

CLI without activation flow:

```text
start_xiaozhi_cli_skip_activation.bat
```

GUI without activation flow:

```text
start_xiaozhi_gui_skip_activation.bat
```

Hidden background mode:

```text
start_xiaozhi_hidden.vbs
```

Stop background mode:

```text
stop_xiaozhi.bat
```

PowerShell entry point:

```powershell
.\scripts\run_xiaozhi_cli.ps1 -Mode cli -SkipActivation
.\scripts\run_xiaozhi_cli.ps1 -Mode gui -SkipActivation
```

## OpenClaw Delegation

The OpenClaw bridge runs:

```powershell
openclaw agent --session-id xiaozhi-openclaw --message "<message>" --json --timeout 90
```

The tool parser extracts OpenClaw replies from JSON payloads recursively, including `result.payloads[0].text`.

## Wake Word

Default wake configuration is in `src/utils/config_manager.py`:

- `WAKE_WORD_OPTIONS.USE_WAKE_WORD`: `true`
- `WAKE_WORD_OPTIONS.MODEL_PATH`: `models/zh`
- `WAKE_WORD_OPTIONS.WAKE_WORD`: `小智`
- `WAKE_WORD_OPTIONS.WAKE_WORD_LANG`: `zh`

The current Chinese keyword file is `models/zh/keywords.txt`. This setup includes:

- `小智`
- `你好小智`
- `台妹`
- `台妹你好`
- `你好台妹`

No local Windows SAPI wake feedback is used. Wake response audio comes from Xiaozhi's cloud TTS path.

## Preconnect Behavior

The app preconnects to Xiaozhi cloud after startup and keeps the protocol connection alive. Opening the protocol channel no longer switches the device into `LISTENING`; audio capture starts only after wake-word detection or a manual listen command.
