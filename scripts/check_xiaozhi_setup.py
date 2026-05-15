import json

import numpy  # noqa: F401
import onnxruntime
import sherpa_onnx  # noqa: F401
import sounddevice  # noqa: F401

from src.mcp.decorators import iter_registered_mcp_tools
from src.utils.config_manager import ConfigManager


def main() -> int:
    config = ConfigManager.get_instance()
    tools = sorted(tool.name for tool in iter_registered_mcp_tools())

    print("python_ok=true")
    print(f"onnxruntime_version={onnxruntime.__version__}")
    print(f"config_file={config.config_file}")
    print(f"wake_word={config.get_config('WAKE_WORD_OPTIONS.WAKE_WORD')}")
    print(f"mcp_tools={len(tools)}")
    print(
        "openclaw_tool_registered="
        + str("self.openclaw.ask" in tools).lower()
    )
    print(
        "openclaw_status_registered="
        + str("self.openclaw.status" in tools).lower()
    )
    print("first_tools=" + json.dumps(tools[:8], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
