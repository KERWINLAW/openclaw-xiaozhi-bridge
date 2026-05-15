"""OpenClaw MCP tools.

These tools let Xiaozhi delegate general reasoning or local OpenClaw tasks to
the installed OpenClaw agent while keeping Xiaozhi responsible for voice UX and
device-style MCP control.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
from typing import Any

from src.logging import get_logger
from src.mcp.decorators import Prop, PropType, mcp_tool

logger = get_logger()

DEFAULT_SESSION_ID = "xiaozhi-openclaw"
MAX_OUTPUT_CHARS = 12000


def _openclaw_executable() -> str:
    exe = shutil.which("openclaw") or shutil.which("openclaw.cmd")
    if not exe:
        raise RuntimeError("OpenClaw command not found in PATH")
    return exe


def _creation_flags() -> int:
    if os.name != "nt":
        return 0
    return getattr(subprocess, "CREATE_NO_WINDOW", 0)


def _clean_text(value: str) -> str:
    return value.strip().replace("\x00", "")


def _iter_json_candidates(text: str) -> list[str]:
    stripped = text.strip()
    candidates: list[str] = []
    if stripped.startswith("{") and stripped.endswith("}"):
        candidates.append(stripped)

    for line in reversed(stripped.splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            candidates.append(line)

    return candidates


def _extract_payload_text(value: Any) -> str | None:
    if isinstance(value, str):
        return _clean_text(value) or None

    if isinstance(value, list):
        parts = []
        for item in value:
            text = _extract_payload_text(item)
            if text:
                parts.append(text)
        return "\n".join(parts).strip() or None

    if not isinstance(value, dict):
        return None

    for key in ("text", "content", "message", "output"):
        item = value.get(key)
        if isinstance(item, str) and item.strip():
            return _clean_text(item)

    for key in ("payloads", "result", "response", "data"):
        if key in value:
            text = _extract_payload_text(value[key])
            if text:
                return text

    return None


async def _run_openclaw(args: list[str], timeout: int) -> subprocess.CompletedProcess:
    exe = _openclaw_executable()
    cmd = [exe, *args]
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("NO_COLOR", "1")

    def _run() -> subprocess.CompletedProcess:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            creationflags=_creation_flags(),
            env=env,
            check=False,
        )

    return await asyncio.to_thread(_run)


def _format_process_result(result: subprocess.CompletedProcess) -> str:
    stdout = _clean_text(result.stdout or "")
    stderr = _clean_text(result.stderr or "")

    for candidate in _iter_json_candidates(stdout):
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        extracted = _extract_payload_text(parsed)
        if extracted:
            return extracted

    if stdout:
        return stdout[-MAX_OUTPUT_CHARS:]
    if stderr:
        return stderr[-MAX_OUTPUT_CHARS:]
    return f"OpenClaw exited with code {result.returncode} and no output."


@mcp_tool(
    name="self.openclaw.ask",
    description=(
        "Ask the local OpenClaw agent to handle a task and return its answer. "
        "Use this when the user explicitly wants OpenClaw, Codex/OpenClaw-style "
        "reasoning, coding help, local workspace analysis, or a task that should "
        "be delegated from Xiaozhi to OpenClaw. "
        "参数: message 是要交给 OpenClaw 的中文或英文请求；session_id 可用于保持上下文。"
    ),
    props=[
        Prop("message", PropType.STR),
        Prop("session_id", PropType.STR, default=DEFAULT_SESSION_ID),
        Prop("timeout_seconds", PropType.INT, default=90, min_val=10, max_val=300),
    ],
)
async def ask_openclaw(args: dict[str, Any]) -> str:
    message = args["message"].strip()
    if not message:
        raise ValueError("message is required")

    session_id = args.get("session_id") or DEFAULT_SESSION_ID
    timeout = int(args.get("timeout_seconds") or 90)
    logger.info("[OpenClawTool] Delegating message to OpenClaw session=%s", session_id)

    result = await _run_openclaw(
        [
            "agent",
            "--session-id",
            session_id,
            "--message",
            message,
            "--json",
            "--timeout",
            str(timeout),
        ],
        timeout=timeout + 15,
    )

    text = _format_process_result(result)
    if result.returncode != 0:
        logger.warning(
            "[OpenClawTool] OpenClaw returned code %s: %s",
            result.returncode,
            text[:500],
        )
    return text


@mcp_tool(
    name="self.openclaw.status",
    description=(
        "Check whether the local OpenClaw CLI and gateway are reachable. "
        "Use this before delegating to OpenClaw when the user asks whether "
        "OpenClaw is available or when OpenClaw calls fail."
    ),
    props=[Prop("timeout_seconds", PropType.INT, default=20, min_val=5, max_val=60)],
)
async def openclaw_status(args: dict[str, Any]) -> str:
    timeout = int(args.get("timeout_seconds") or 20)

    version = await _run_openclaw(["--version"], timeout=timeout)
    status = await _run_openclaw(["gateway", "status", "--json"], timeout=timeout)

    return json.dumps(
        {
            "openclaw_version": _format_process_result(version),
            "version_exit_code": version.returncode,
            "gateway_status": _format_process_result(status),
            "gateway_exit_code": status.returncode,
        },
        ensure_ascii=False,
    )
