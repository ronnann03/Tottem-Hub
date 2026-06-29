'use client'
import { useState, useEffect } from 'react'
import { ListaAlumnosPatrocinados } from '@/components/mecenas/ListaAlumnosPatrocinados'

export default function MecenasPage() {
  const [alumnos, setAlumnos] = useState<any[]>([])
  const [cargando, setCargando] = useState(true)
  const mecenasId = 'me'

  useEffect(() => {
    fetch(`/api/v1/mecenas/${mecenasId}/alumnos/`)
      .then(r => r.json())
      .then(setAlumnos)
      .finally(() => setCargando(false))
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto py-8 px-4">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Portal Mecenas</h1>
        <p className="text-sm text-gray-500 mb-6">Alumnos que estas patrocinando</p>
        {cargando ? (
          <div className="space-y-3">{[1,2].map(i => <div key={i} className="h-32 bg-gray-200 rounded-xl animate-pulse" />)}</div>
        ) : (
          <ListaAlumnosPatrocinados alumnos={alumnos} mecenasId={mecenasId} />
        )}
      </div>
    </div>
  )
}