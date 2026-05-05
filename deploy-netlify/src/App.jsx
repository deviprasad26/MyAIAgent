import { useEffect, useRef, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export default function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hey! I am your AI Agent. How can I help you today?' },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function sendMessage(e) {
    e.preventDefault()
    const text = input.trim()
    if (!text || loading) return

    setError('')
    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      })

      if (!response.ok) {
        const err = await response.json().catch(() => ({}))
        throw new Error(err.detail || 'Request failed')
      }

      const data = await response.json()
      setMessages((prev) => [...prev, { role: 'assistant', content: data.reply || '' }])
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <div className="chat-card">
        <header className="chat-header">
          <h1>AI Agent</h1>
          <p>Smooth React UI connected to your Python backend</p>
        </header>

        <main className="chat-body">
          {messages.map((msg, idx) => (
            <div key={idx} className={`bubble-row ${msg.role}`}>
              <div className={`bubble ${msg.role}`}>{msg.content}</div>
            </div>
          ))}

          {loading && (
            <div className="bubble-row assistant">
              <div className="bubble assistant typing">Thinking...</div>
            </div>
          )}

          <div ref={endRef} />
        </main>

        {error && <div className="error-banner">{error}</div>}

        <form className="chat-input" onSubmit={sendMessage}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  )
}
