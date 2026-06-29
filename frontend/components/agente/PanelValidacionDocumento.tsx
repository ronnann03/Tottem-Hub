'use client'
import { useState } from 'react'

interface Documento {
  id: string
  nombre_archivo: string
  archivo: string
  estado: string
  inscripcion: { alumno: { nombre: string; apellidos: string } }
  documento_requerido: { nombre: string }
}

interface PanelValidacionDocumentoProps {
  documentos: Documento[]
}

export function PanelValidacionDocumento({ documentos }: PanelValidacionDocumentoProps) {
  const [motivoId, setMotivoId] = useState<string | null>(null)
  const [motivo, setMotivo] = useState('')
  const [procesando, setProcesando] = useState<string | null>(null)
  const [estados, setEstados] = useState<Record<string, string>>({})

  async function validar(id: string) {
    setProcesando(id)
    await fetch(`/api/v1/documentos/${id}/`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ estado: 'validado' }) })
    setEstados(prev => ({ ...prev, [id]: 'validado' }))
    setProcesando(null)
  }

  async function rechazar(id: string) {
    if (!motivo) return
    setProcesando(id)
    await fetch(`/api/v1/documentos/${id}/`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ estado: 'rechazado', motivo_rechazo: motivo }) })
    setEstados(prev => ({ ...prev, [id]: 'rechazado' }))
    setMotivoId(null)
    setMotivo('')
    setProcesando(null)
  }

  const pendientes = documentos.filter(d => (estados[d.id] ?? d.estado) === 'pendiente')

  return (
    <div className="space-y-4">
      {pendientes.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-3xl mb-2">✓</p>
          <p>No hay documentos pendientes de validacion.</p>
        </div>
      )}
      {pendientes.map(doc => {
        const esImagen = doc.archivo && /\.(jpg|jpeg|png)$/i.test(doc.archivo)
        const esPdf = doc.archivo && /\.pdf$/i.test(doc.archivo)
        return (
          <div key={doc.id} className="bg-white border border-gray-200 rounded-xl p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="font-semibold text-gray-900">{doc.inscripcion.alumno.nombre} {doc.inscripcion.alumno.apellidos}</p>
                <p className="text-sm text-blue-600">{doc.documento_requerido.nombre}</p>
                <p className="text-xs text-gray-400 mt-0.5">{doc.nombre_archivo}</p>
              </div>
              <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded-full">Pendiente</span>
            </div>
            {doc.archivo && (
              <div className="mb-4 border border-gray-100 rounded-lg overflow-hidden">
                {esImagen && <img src={doc.archivo} alt="Documento" className="max-h-64 w-full object-contain bg-gray-50" />}
                {esPdf && <iframe src={doc.archivo} className="w-full h-64" title="Documento PDF" />}
                {!esImagen && !esPdf && <a href={doc.archivo} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline text-sm p-4 block">Ver documento</a>}
              </div>
            )}
            {motivoId === doc.id ? (
              <div className="space-y-2">
                <textarea value={motivo} onChange={e => setMotivo(e.target.value)} placeholder="Motivo del rechazo..." rows={2} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
                <div className="flex gap-2">
                  <button onClick={() => rechazar(doc.id)} disabled={!motivo || procesando === doc.id} className="bg-red-600 text-white px-4 py-1.5 rounded-lg text-sm font-medium disabled:opacity-50">
                    Confirmar rechazo
                  </button>
                  <button onClick={() => setMotivoId(null)} className="border border-gray-300 text-gray-700 px-4 py-1.5 rounded-lg text-sm">
                    Cancelar
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex gap-2">
                <button onClick={() => validar(doc.id)} disabled={procesando === doc.id} className="bg-green-600 text-white px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50">
                  Validar documento
                </button>
                <button onClick={() => setMotivoId(doc.id)} className="border border-red-300 text-red-600 px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-red-50">
                  Rechazar
                </button>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}