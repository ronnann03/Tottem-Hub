'use client'
import { useState, useEffect, useRef } from 'react'

interface Mensaje {
  id: string
  contenido: string
  remitente: string
  remitente_nombre: string
  estado: string
  created_at: string
}

interface ChatProps {
  inscripcionId: string
  usuarioActualId: string
}

export function ChatInscripcion({ inscripcionId, usuarioActualId }: ChatProps) {
  const [mensajes, setMensajes] = useState<Mensaje[]>([])
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [cargando, setCargando] = useState(true)
  const bottomRef = useRef<HTMLDivElement>(null)
  const ultimoRef = useRef<string>('')

  async function cargarConversacion() {
    const res = await fetch(`/api/v1/chat/${inscripcionId}/`)
    if (!res.ok) return
    const data = await res.json()
    setMensajes(data.mensajes || [])
    if (data.mensajes?.length > 0) {
      ultimoRef.current = data.mensajes[data.mensajes.length - 1].created_at
    }
    setCargando(false)
  }

  async function pollNuevos() {
    if (!ultimoRef.current) return
    const res = await fetch(`/api/v1/chat/${inscripcionId}/mensajes/nuevos/?desde=${ultimoRef.current}`)
    if (!res.ok) return
    const nuevos = await res.json()
    if (nuevos.length > 0) {
      setMensajes(prev => [...prev, ...nuevos])
      ultimoRef.current = nuevos[nuevos.length - 1].created_at
    }
  }

  useEffect(() => {
    cargarConversacion()
    const interval = setInterval(pollNuevos, 5000)
    return () => clearInterval(interval)
  }, [inscripcionId])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [mensajes])

  async function handleEnviar() {
    if (!texto.trim() || enviando) return
    setEnviando(true)
    const res = await fetch(`/api/v1/chat/${inscripcionId}/mensajes/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contenido: texto.trim() })
    })
    if (res.ok) {
      const nuevo = await res.json()
      setMensajes(prev => [...prev, nuevo])
      ultimoRef.current = nuevo.created_at
      setTexto('')
    }
    setEnviando(false)
  }

  if (cargando) return <div className="p-4 text-gray-400 text-sm">Cargando chat...</div>

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
        {mensajes.length === 0 && (
          <p className="text-center text-gray-400 text-sm mt-8">Sin mensajes aun. Inicia la conversacion.</p>
        )}
        {mensajes.map(m => {
          const esMio = m.remitente === usuarioActualId
          return (
            <div key={m.id} className={`flex ${esMio ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl text-sm ${esMio ? 'bg-blue-800 text-white rounded-br-sm' : 'bg-white border border-gray-200 text-gray-900 rounded-bl-sm'}`}>
                {!esMio && <p className="text-xs font-semibold mb-1 text-blue-600">{m.remitente_nombre}</p>}
                <p>{m.contenido}</p>
                <p className={`text-xs mt-1 ${esMio ? 'text-blue-200' : 'text-gray-400'}`}>
                  {new Date(m.created_at).toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })}
                  {esMio && <span className="ml-1">{m.estado === 'leido' ? '✓✓' : '✓'}</span>}
                </p>
              </div>
            </div>
          )
        })}
        <div ref={bottomRef} />
      </div>
      <div className="border-t bg-white p-3 flex gap-2">
        <input
          type="text"
          value={texto}
          onChange={e => setTexto(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleEnviar()}
          placeholder="Escribe un mensaje..."
          className="flex-1 border border-gray-300 rounded-full px-4 py-2 text-sm focus:outline-none focus:border-blue-500"
        />
        <button onClick={handleEnviar} disabled={enviando || !texto.trim()} className="bg-blue-800 text-white px-4 py-2 rounded-full text-sm font-medium disabled:opacity-50 hover:bg-blue-700">
          {enviando ? '...' : 'Enviar'}
        </button>
      </div>
    </div>
  )
}