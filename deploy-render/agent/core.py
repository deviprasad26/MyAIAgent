from __future__ import annotations

import json
from typing import Any

from agent.llm import LLMClient
from agent.memory import ConversationMemory
from agent.tools import ToolRegistry, tool_schemas


SYSTEM_PROMPT = (
    "You are a helpful AI coding agent. "
    "When needed, call available tools to inspect or modify files. "
    "Be concise, accurate, and safe."
)


class Agent:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm
        self.tools = ToolRegistry()
        self.memory = ConversationMemory(system_prompt=SYSTEM_PROMPT)

    def run_turn(self, user_input: str, max_steps: int = 5) -> str:
        self.memory.add_user(user_input)

        for _ in range(max_steps):
            assistant_message = self.llm.chat(self.memory.all(), tools=tool_schemas())
            content = assistant_message.get("content")
            tool_calls = assistant_message.get("tool_calls")

            self.memory.add_assistant(content=content, tool_calls=tool_calls)

            if not tool_calls:
                return content or ""

            for tc in tool_calls:
                fn = tc.get("function", {})
                name = fn.get("name", "")
                raw_args = fn.get("arguments", "{}")
                try:
                    args: dict[str, Any] = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                except json.JSONDecodeError:
                    args = {}

                result = self.tools.call(name, args)
                self.memory.add_tool_result(tc.get("id", ""), result)

        return "I reached the tool-call step limit for this turn. Please refine your request."
