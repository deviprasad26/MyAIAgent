# AI Agent (Python + React UI)

A lightweight, extensible AI agent with:

- **Python backend** (CLI + FastAPI)
- **React frontend** (smooth chat UI)

## Features

- Chat with an LLM from terminal (`main.py`)
- Chat via web API (`api.py`)
- Smooth React chat interface (`web/`)
- Tool-calling loop for local tools
- Built-in tools:
  - `read_file(path)`
  - `list_files(path='.')`
  - `write_file(path, content)`
- Conversation memory in-process
- Easy provider swap via environment variables

## Tech

- Python 3.10+
- FastAPI + Uvicorn
- OpenAI-compatible Chat Completions API
- `requests` + `python-dotenv`
- React + Vite

## Quick Start (Backend)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows cmd
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` file from example:

```bash
copy .env.example .env
```

4. Set your key in `.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

5. (Optional) Run CLI agent:

```bash
python main.py
```

6. Run API server:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Backend health check:

```bash
curl http://127.0.0.1:8000/health
```

## Quick Start (React Web UI)

1. Open new terminal and go to web app:

```bash
cd web
```

2. Install frontend dependencies:

```bash
npm install
```

3. Create frontend env file:

```bash
copy .env.example .env
```

4. Start frontend:

```bash
npm run dev
```

Open: `http://127.0.0.1:5173`

> Make sure backend is running on `http://127.0.0.1:8000`.

## API Usage

### POST `/chat`

Request:

```json
{
  "message": "Explain recursion in simple terms"
}
```

Response:

```json
{
  "reply": "..."
}
```

## CLI Usage

- Type your prompt and press Enter.
- Type `exit` to quit.

The agent can decide to call tools when needed. Example prompts:

- `List files in current directory`
- `Create a file notes.txt with 3 bullet points about Python`
- `Read README.md and summarize it`

## Project Structure

```text
.
├── api.py
├── main.py
├── requirements.txt
├── .env.example
├── web/
│   ├── package.json
│   ├── .env.example
│   ├── index.html
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       └── styles.css
└── agent/
    ├── __init__.py
    ├── config.py
    ├── llm.py
    ├── memory.py
    ├── tools.py
    └── core.py
```

## Extend with New Tools

Add a function in `agent/tools.py`, register it in `ToolRegistry`, and include its JSON schema in `tool_schemas()`.

## Notes

- This is a local starter template, not a sandboxed execution environment.
- Be careful with file-writing prompts.

## Deployment (Full Steps)

You will deploy **2 services**:

1. **Backend API** (Render)
2. **Frontend React** (Vercel or Netlify)

---

### A) Deploy Backend on Render

1. Push project to GitHub.
2. Go to Render → **New +** → **Web Service**.
3. Connect your GitHub repo.
4. Configure:
   - **Root Directory**: project root
   - **Build Command**:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn api:app --host 0.0.0.0 --port $PORT
     ```
5. Add environment variables:
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL` (e.g. `gpt-4o-mini`)
   - `OPENAI_BASE_URL` (usually `https://api.openai.com/v1`)
6. Deploy and copy backend URL (example: `https://your-agent-api.onrender.com`).

---

### B) Deploy Frontend on Vercel

1. Import same repo into Vercel.
2. Set **Root Directory** to `web`.
3. Build settings:
   - Build command: `npm run build`
   - Output directory: `dist`
4. Add env variable:
   - `VITE_API_URL=https://your-agent-api.onrender.com`
5. Deploy.

---

### C) Deploy Frontend on Netlify (Alternative)

1. New site from Git.
2. Base directory: `web`
3. Build command: `npm run build`
4. Publish directory: `web/dist`
5. Environment variable:
   - `VITE_API_URL=https://your-agent-api.onrender.com`
6. Deploy.

---

### D) Important Production Note (CORS)

`api.py` currently allows all origins (`*`) for easy setup.
For production security, restrict `allow_origins` to your frontend domain(s).
