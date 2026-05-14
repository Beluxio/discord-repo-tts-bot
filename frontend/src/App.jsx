import { useState, useRef, useEffect } from 'react'
import './App.css'

const LOGO = `
██████╗ ███████╗██████╗  ██████╗
██╔══██╗██╔════╝██╔══██╗██╔═══██╗
██████╔╝█████╗  ██████╔╝██║   ██║
██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║
██║  ██║███████╗██║     ╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝`

export default function App() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [audioUrl, setAudioUrl] = useState(null)
  const [online, setOnline] = useState(null)
  const audioRef = useRef(null)

  useEffect(() => {
    fetch('/status')
      .then(r => r.json())
      .then(d => setOnline(d.status === 'online'))
      .catch(() => setOnline(false))
  }, [])

  async function speak() {
    if (!text.trim() || loading) return
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`/tts?texto=${encodeURIComponent(text.trim())}`)

      const contentType = res.headers.get('content-type') || ''
      if (!contentType.includes('audio')) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.error || `HTTP ${res.status}`)
      }

      const blob = await res.blob()
      if (audioUrl) URL.revokeObjectURL(audioUrl)
      const url = URL.createObjectURL(blob)
      setAudioUrl(url)
      setTimeout(() => audioRef.current?.play(), 50)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      speak()
    }
  }

  return (
    <div className="app">
      <div className="scanlines" aria-hidden="true" />

      <header className="header">
        <pre className="logo">{LOGO}</pre>
        <div className="header-meta">
          <span className="tagline">KLATTERSYNTH VOICE ENGINE v1.0</span>
          <span className={`status-indicator ${online === true ? 'online' : online === false ? 'offline' : 'checking'}`}>
            {online === true ? '● ONLINE' : online === false ? '● OFFLINE' : '● CHECKING...'}
          </span>
        </div>
      </header>

      <main className="panel">
        <span className="panel-title">[ R.E.P.O. TTS INTERFACE ]</span>

        <div className="field">
          <label className="field-label">&gt; INPUT_TEXT</label>
          <textarea
            className="field-textarea"
            value={text}
            onChange={e => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type something to speak..."
            rows={3}
            maxLength={300}
            spellCheck={false}
          />
          <span className="char-count">{text.length} / 300</span>
        </div>

        <button
          className={`btn-speak${loading ? ' loading' : ''}`}
          onClick={speak}
          disabled={loading || !text.trim()}
        >
          {loading ? '[ PROCESSING... ]' : '[ ▶  SPEAK ]'}
        </button>

        {error && (
          <div className="error-box" role="alert">
            <span className="error-label">! ERROR</span>
            <span>{error}</span>
          </div>
        )}

        {audioUrl && (
          <div className="output-field">
            <label className="field-label">&gt; AUDIO_OUTPUT</label>
            <audio ref={audioRef} src={audioUrl} controls className="audio-player" />
          </div>
        )}
      </main>

      <footer className="footer">
        <a href="/docs" target="_blank" rel="noopener noreferrer" className="footer-link">
          API DOCS
        </a>
        <span className="sep">|</span>
        <span>R.E.P.O. TTS BOT</span>
        <span className="sep">|</span>
        <a href="https://github.com/Beluxio" target="_blank" rel="noopener noreferrer" className="footer-link">
          GITHUB
        </a>
      </footer>
    </div>
  )
}
