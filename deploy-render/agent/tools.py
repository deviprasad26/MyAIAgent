from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Any


ToolFn = Callable[..., str]


def _safe_resolve(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    root = Path.cwd().resolve()
    try:
        p.relative_to(root)
    except ValueError as exc:
        raise ValueError("Path is outside the working directory.") from exc
    return p


def read_file(path: str) -> str:
    file_path = _safe_resolve(path)
    if not file_path.exists() or not file_path.is_file():
        return f"ERROR: File not found: {path}"
    return file_path.read_text(encoding="utf-8", errors="replace")


def list_files(path: str = ".") -> str:
    dir_path = _safe_resolve(path)
    if not dir_path.exists() or not dir_path.is_dir():
        return f"ERROR: Directory not found: {path}"

    items = sorted([p.name for p in dir_path.iterdir()])
    return json.dumps(items)


def write_file(path: str, content: str) -> str:
    file_path = _safe_resolve(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return f"OK: Wrote {path}"


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolFn] = {
            "read_file": read_file,
            "list_files": list_files,
            "write_file": write_file,
        }

    def has(self, name: str) -> bool:
        return name in self._tools

    def call(self, name: str, arguments: dict[str, Any]) -> str:
        if name not in self._tools:
            return f"ERROR: Unknown tool: {name}"
        try:
            return self._tools[name](**arguments)
        except Exception as exc:  # noqa: BLE001
            return f"ERROR: Tool {name} failed: {exc}"


def tool_schemas() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read a UTF-8 text file from current workspace.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Relative file path"}
                    },
                    "required": ["path"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "List files/folders inside a directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative directory path",
                            "default": ".",
                        }
                    },
                    "required": [],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Create or overwrite a UTF-8 text file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Relative file path"},
                        "content": {"type": "string", "description": "Text content"},
                    },
                    "required": ["path", "content"],
                    "additionalProperties": False,
                },
            },
        },
    ]
