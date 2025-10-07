import React, { useState } from 'react'

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`/api${path}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export const App: React.FC = () => {
  const [health, setHealth] = useState<string>('')
  const [ping, setPing] = useState<string>('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [useSynthetic, setUseSynthetic] = useState(false)
  const [token, setToken] = useState('')
  const [verifyMsg, setVerifyMsg] = useState('')
  const [scanResults, setScanResults] = useState<any>(null)
  const [imageInfo, setImageInfo] = useState<any>(null)

  const checkHealth = async () => {
    const r = await api<{ status: string }>(`/health`)
    setHealth(r.status)
  }
  const checkPing = async () => {
    const r = await api<{ message: string }>(`/auth/ping`)
    setPing(r.message)
  }
  const doRegister = async () => {
    const full_name = `${firstName} ${lastName}`.trim()
    const r = await api<{ message: string }>(`/auth/register`, {
      method: 'POST',
      body: JSON.stringify({ full_name, email, consent: true }),
    })
    setToken(r.message)
  }
  const doVerify = async () => {
    const r = await api<{ message: string }>(`/auth/verify`, {
      method: 'POST',
      body: JSON.stringify({ token }),
    })
    setVerifyMsg(r.message)
  }
  const doSelfScan = async () => {
    const full_name = `${firstName} ${lastName}`.trim()
    const r = await api<any>(`/self-scan`, {
      method: 'POST',
      body: JSON.stringify({ full_name, email: email || null }),
    })
    setScanResults(r)
  }

  const doImageAnalyze = async (file: File) => {
    const form = new FormData()
    form.append('file', file)
    const res = await fetch('/api/analyze-image', { method: 'POST', body: form })
    if (!res.ok) throw new Error('Gorsel analizi basarisiz')
    const data = await res.json()
    setImageInfo(data)
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🔐 Dijital Ayak İzi Farkındalık</h1>
        <p>Kendi dijital izinizi keşfedin, gizliliğinizi koruyun</p>
      </div>

      <div className="section">
        <h2>Kayıt & Doğrulama</h2>
        <div className="input-group">
          <input type="text" placeholder="Ad" value={firstName} onChange={e => setFirstName(e.target.value)} />
          <input type="text" placeholder="Soyad" value={lastName} onChange={e => setLastName(e.target.value)} />
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <button onClick={doRegister}>Kaydol</button>
        {token && (
          <div className="token-display">
            <small>Doğrulama Token'ı:</small>
            <div>{token}</div>
          </div>
        )}
        {token && (
          <div style={{ marginTop: 16 }}>
            <button onClick={doVerify}>Email Doğrula</button>
            {verifyMsg && <div className="result-box">{verifyMsg}</div>}
          </div>
        )}
      </div>

      <div className="section">
        <h2>🔎 İsim Taraması</h2>
        <label className="checkbox-label">
          <input type="checkbox" checked={useSynthetic} onChange={e => setUseSynthetic(e.target.checked)} />
          <span>Sentetik demo modu (backend ENV: SYNTHETIC_MODE=true)</span>
        </label>
        <button onClick={doSelfScan}>Kendi Dijital İzimi Tara</button>
        {scanResults && (
          <div className="result-box">
            <div className="info-row">
              <strong>Risk Skoru:</strong> {scanResults.risk_score}/100
              <span className={`risk-badge risk-${scanResults.risk_level}`}>{scanResults.risk_level}</span>
            </div>
            <ul className="result-list">
              {scanResults.results?.map((it: any, idx: number) => (
                <li key={idx}>
                  {it.type === 'web' ? (
                    <a href={it.link} target="_blank" rel="noreferrer">🌐 {it.title}</a>
                  ) : (
                    <span>⚠️ Veri İhlali: {it.name} ({it.domain})</span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className="section">
        <h2>📷 Görsel Analiz</h2>
        <input type="file" accept="image/*" onChange={e => e.target.files && e.target.files[0] && doImageAnalyze(e.target.files[0])} />
        {imageInfo && (
          <div className="result-box">
            <div className="info-row"><strong>pHash:</strong> {imageInfo.phash}</div>
            {imageInfo.exif?.gps?.lat && imageInfo.exif?.gps?.lon ? (
              <div className="info-row"><strong>GPS Konum:</strong> {imageInfo.exif.gps.lat.toFixed(6)}, {imageInfo.exif.gps.lon.toFixed(6)}</div>
            ) : (
              <div className="info-row"><strong>GPS:</strong> Bulunamadı</div>
            )}
            <div className="info-row"><strong>EXIF Verileri:</strong> {imageInfo.exif?.has_exif ? '✅ Mevcut' : '❌ Yok'}</div>
          </div>
        )}
      </div>

      <div className="section">
        <h2>⚡ API Sağlık Kontrolü</h2>
        <div style={{ display: 'flex', gap: 12 }}>
          <button onClick={checkHealth}>Health</button>
          <button onClick={checkPing}>Ping</button>
        </div>
        {(health || ping) && (
          <div className="result-box" style={{ marginTop: 12 }}>
            {health && <div className="info-row">Health: {health}</div>}
            {ping && <div className="info-row">Ping: {ping}</div>}
          </div>
        )}
      </div>
    </div>
  )
}


