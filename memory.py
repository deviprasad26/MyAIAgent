from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


Message = dict[str, Any]


@dataclass
class ConversationMemory:
    system_prompt: str
    messages: list[Message] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.messages.append({"role": "system", "content": self.system_prompt})

    def add_user(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str | None = None, tool_calls: list[dict] | None = None) -> None:
        message: Message = {"role": "assistant"}
        if content is not None:
            message["content"] = content
        if tool_calls is not None:
            message["tool_calls"] = tool_calls
        self.messages.append(message)

    def add_tool_result(self, tool_call_id: str, content: str) -> None:
        self.messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": content,
            }
        )

    def all(self) -> list[Message]:
        return self.messages
