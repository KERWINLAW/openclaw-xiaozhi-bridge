# Fix Xiaozhi Background Lifecycle

## Problem

After reboot testing, Xiaozhi can leave a resident Python process that adds CPU pressure and makes TTS stutter. Launching again can also create two identical Xiaozhi background instances.

## Goals

- Prevent two Xiaozhi instances from running for the same workspace/runtime data directory.
- Reduce idle network churn from preconnect/keepalive behavior.
- Keep hidden startup lightweight and avoid an extra resident PowerShell process where practical.
- Keep OpenClaw Gateway separate; do not treat the gateway `wscript.exe` as Xiaozhi.

## Non-Goals

- Do not rewrite the core in Rust in this task.
- Do not change Xiaozhi cloud protocol behavior beyond reconnect/preconnect policy.
- Do not remove GUI or CLI launch modes.

## Acceptance Criteria

- Starting Xiaozhi twice exits the second process without creating a duplicate listener.
- Runtime defaults avoid infinite idle reconnect loops.
- Wake-word worker threads default to a lower CPU setting.
- Background logging respects `INFO` level and avoids verbose MCP JSON writes.
- Hidden launch can run without CLI UI and can be stopped by the stop script.
- Python files compile successfully.
