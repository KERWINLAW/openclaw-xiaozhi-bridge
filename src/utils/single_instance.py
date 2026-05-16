"""Single-instance guard for local app launches."""

import ctypes
import hashlib
import os
import tempfile
from pathlib import Path
from typing import TextIO


class SingleInstance:
    """Keep one process alive for a named runtime key."""

    def __init__(self, key: str) -> None:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]
        self._name = f"py_xiaozhi_{digest}"
        self._handle: int | None = None
        self._lock_file: TextIO | None = None

    def acquire(self) -> bool:
        """Return True when this process owns the instance guard."""
        if os.name == "nt":
            return self._acquire_windows()
        return self._acquire_file_lock()

    def release(self) -> None:
        """Release the guard if it was acquired."""
        if self._handle is not None:
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
            kernel32.CloseHandle.restype = ctypes.c_bool
            kernel32.CloseHandle(self._handle)
            self._handle = None

        if self._lock_file is not None:
            try:
                import fcntl

                fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_UN)
            finally:
                self._lock_file.close()
                self._lock_file = None

    def _acquire_windows(self) -> bool:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateMutexW.argtypes = [
            ctypes.c_void_p,
            ctypes.c_bool,
            ctypes.c_wchar_p,
        ]
        kernel32.CreateMutexW.restype = ctypes.c_void_p

        ctypes.set_last_error(0)
        handle = kernel32.CreateMutexW(None, False, f"Local\\{self._name}")
        if not handle:
            raise OSError(ctypes.get_last_error(), "CreateMutexW failed")

        self._handle = handle
        error_already_exists = 183
        if ctypes.get_last_error() == error_already_exists:
            self.release()
            return False
        return True

    def _acquire_file_lock(self) -> bool:
        import fcntl

        lock_path = Path(tempfile.gettempdir()) / f"{self._name}.lock"
        self._lock_file = lock_path.open("w", encoding="utf-8")
        try:
            fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.release()
            return False
        return True
