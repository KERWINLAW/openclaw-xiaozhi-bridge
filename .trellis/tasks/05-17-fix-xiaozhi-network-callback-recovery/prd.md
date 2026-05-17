# Fix Xiaozhi Network Callback Recovery

## Problem

When the Xiaozhi WebSocket connection is closed by the server during idle or conversation, the protocol layer invokes the registered network error callback with `await`. The registered callback in `ProtocolManager` is synchronous, so the disconnect path raises `object NoneType can't be used in 'await' expression`.

## Goals

- Make protocol callback dispatch tolerate both synchronous and asynchronous callbacks.
- Preserve the current low-churn reconnect policy.
- Verify the current background process can be restarted cleanly.

## Acceptance Criteria

- No direct `await` of a possibly synchronous network error callback remains in `src/protocols/protocol.py`.
- Touched Python files pass `ruff check` and `py_compile`.
- Xiaozhi can be stopped and started in hidden mode after the fix.
