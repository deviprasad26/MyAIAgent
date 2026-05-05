from __future__ import annotations

from agent.config import load_settings
from agent.core import Agent
from agent.llm import LLMClient


def main() -> None:
    settings = load_settings()
    if not settings.api_key:
        print("Missing OPENAI_API_KEY. Set it in .env or environment variables.")
        return

    llm = LLMClient(
        api_key=settings.api_key,
        model=settings.model,
        base_url=settings.base_url,
    )
    agent = Agent(llm)

    print("AI Agent started. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        if not user_input:
            continue

        try:
            reply = agent.run_turn(user_input)
            print(f"Agent: {reply}\n")
        except Exception as exc:  # noqa: BLE001
            print(f"Agent error: {exc}\n")


if __name__ == "__main__":
    main()
