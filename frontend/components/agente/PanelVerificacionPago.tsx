'use client'
import { useState } from 'react'

interface Pago {
  id: string
  importe: number
  fecha_pago: string
  metodo_pago: string
  comprobante?: string
  estado: string
  inscripcion: { alumno: { nombre: string; apellidos: string } }
}

interface PanelVerificacionPagoProps {
  pagos: Pago[]
}

export function PanelVerificacionPago({ pagos }: PanelVerificacionPagoProps) {
  const [motivoId, setMotivoId] = useState<string | null>(null)
  const [motivo, setMotivo] = useState('')
  const [procesando, setProcesando] = useState<string | null>(null)
  const [estados, setEstados] = useState<Record<string, string>>({})

  async function verificar(id: string) {
    setProcesando(id)
    await fetch(`/api/v1/pagos/${id}/`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ estado: 'verificado' }) })
    setEstados(prev => ({ ...prev, [id]: 'verificado' }))
    setProcesando(null)
  }

  async function rechazar(id: string) {
    if (!motivo) return
    setProcesando(id)
    await fetch(`/api/v1/pagos/${id}/`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ estado: 'rechazado', motivo_rechazo: motivo }) })
    setEstados(prev => ({ ...prev, [id]: 'rechazado' }))
    setMotivoId(null)
    setMotivo('')
    setProcesando(null)
  }

  const pendientes = pagos.filter(p => (estados[p.id] ?? p.estado) === 'pendiente')

  return (
    <div className="space-y-4">
      {pendientes.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-3xl mb-2">✓</p>
          <p>No hay pagos pendientes de revision.</p>
        </div>
      )}
      {pendientes.map(pago => {
        const esImagen = pago.comprobante && /\.(jpg|jpeg|png)$/i.test(pago.comprobante)
        const esPdf = pago.comprobante && /\.pdf$/i.test(pago.comprobante)
        return (
          <div key={pago.id} className="bg-white border border-gray-200 rounded-xl p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="font-semibold text-gray-900">{pago.inscripcion.alumno.nombre} {pago.inscripcion.alumno.apellidos}</p>
                <p className="text-sm text-gray-500">S/ {pago.importe} · {pago.fecha_pago} · {pago.metodo_pago}</p>
              </div>
              <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded-full">Pendiente</span>
            </div>
            {pago.comprobante && (
              <div className="mb-4 border border-gray-100 rounded-lg overflow-hidden">
                {esImagen && <img src={pago.comprobante} alt="Comprobante" className="max-h-64 w-full object-contain bg-gray-50" />}
                {esPdf && <iframe src={pago.comprobante} className="w-full h-64" title="Comprobante PDF" />}
                {!esImagen && !esPdf && <a href={pago.comprobante} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline text-sm p-4 block">Ver comprobante</a>}
              </div>
            )}
            {motivoId === pago.id ? (
              <div className="space-y-2">
                <textarea value={motivo} onChange={e => setMotivo(e.target.value)} placeholder="Motivo del rechazo..." rows={2} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
                <div className="flex gap-2">
                  <button onClick={() => rechazar(pago.id)} disabled={!motivo || procesando === pago.id} className="bg-red-600 text-white px-4 py-1.5 rounded-lg text-sm font-medium disabled:opacity-50">
                    Confirmar rechazo
                  </button>
                  <button onClick={() => setMotivoId(null)} className="border border-gray-300 text-gray-700 px-4 py-1.5 rounded-lg text-sm">
                    Cancelar
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex gap-2">
                <button onClick={() => verificar(pago.id)} disabled={procesando === pago.id} className="bg-green-600 text-white px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50">
                  Verificar pago
                </button>
                <button onClick={() => setMotivoId(pago.id)} className="border border-red-300 text-red-600 px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-red-50">
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