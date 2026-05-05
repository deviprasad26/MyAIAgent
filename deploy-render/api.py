from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.config import load_settings
from agent.core import Agent
from agent.llm import LLMClient


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


settings = load_settings()

if not settings.api_key:
    raise RuntimeError("Missing OPENAI_API_KEY. Set it in .env or environment variables.")

llm = LLMClient(
    api_key=settings.api_key,
    model=settings.model,
    base_url=settings.base_url,
)
agent = Agent(llm)

app = FastAPI(title="AI Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        reply = agent.run_turn(message)
        return ChatResponse(reply=reply)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Agent error: {exc}") from exc
