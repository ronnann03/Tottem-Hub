'use client'
import { useState } from 'react'
import { FileUploader } from '@/components/forms/FileUploader'

interface FormularioPagoMecenasProps {
  mecenasId: string
  inscripcionId: string
  nombreAlumno: string
  onExito: () => void
}

export function FormularioPagoMecenas({ mecenasId, inscripcionId, nombreAlumno, onExito }: FormularioPagoMecenasProps) {
  const [importe, setImporte] = useState('')
  const [fecha, setFecha] = useState('')
  const [comprobante, setComprobante] = useState<File | null>(null)
  const [enviando, setEnviando] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [exito, setExito] = useState(false)

  async function handleSubmit() {
    if (!importe || !fecha) { setError('Completa importe y fecha.'); return }
    setEnviando(true)
    setError(null)
    try {
      const formData = new FormData()
      formData.append('inscripcion', inscripcionId)
      formData.append('importe', importe)
      formData.append('fecha_pago', fecha)
      formData.append('metodo_pago', 'mecenas')
      if (comprobante) formData.append('comprobante', comprobante)
      const res = await fetch('/api/v1/pagos/', { method: 'POST', body: formData })
      if (!res.ok) throw new Error('Error')
      setExito(true)
      onExito()
    } catch {
      setError('Error al registrar el pago.')
    } finally {
      setEnviando(false)
    }
  }

  if (exito) return (
    <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
      <p className="text-green-800 font-semibold">✓ Pago registrado para {nombreAlumno}</p>
      <p className="text-xs text-green-600 mt-1">Pendiente de revision por el agente</p>
    </div>
  )

  return (
    <div className="space-y-3 mt-4 border-t pt-4">
      <h4 className="text-sm font-semibold text-gray-700">Registrar pago para {nombreAlumno}</h4>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Importe (S/) *</label>
          <input type="number" value={importe} onChange={e => setImporte(e.target.value)} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Fecha *</label>
          <input type="date" value={fecha} onChange={e => setFecha(e.target.value)} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
        </div>
      </div>
      <div>
        <label className="block text-xs font-medium text-gray-600 mb-1">Comprobante (opcional)</label>
        <FileUploader onFileSelect={f => setComprobante(f)} />
      </div>
      {error && <p className="text-red-600 text-xs">{error}</p>}
      <button onClick={handleSubmit} disabled={enviando} className="w-full bg-blue-800 text-white py-2 rounded-lg text-sm font-semibold disabled:opacity-50">
        {enviando ? 'Registrando...' : 'Registrar pago'}
      </button>
    </div>
  )
}