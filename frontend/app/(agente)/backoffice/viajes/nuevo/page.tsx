'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function NuevoViajePage() {
  const router = useRouter()
  const [enviando, setEnviando] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [form, setForm] = useState({
    nombre: '', destino: '', fecha_salida: '', fecha_regreso: '',
    cupo_maximo: '', precio_total: '', descripcion: ''
  })

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  async function handleSubmit() {
    if (!form.nombre || !form.destino || !form.fecha_salida || !form.fecha_regreso) {
      setError('Completa los campos obligatorios.')
      return
    }
    setEnviando(true)
    setError(null)
    try {
      const res = await fetch('/api/v1/viajes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, cupo_maximo: Number(form.cupo_maximo), precio_total: Number(form.precio_total) })
      })
      if (!res.ok) throw new Error('Error al crear viaje')
      const data = await res.json()
      router.push(`/backoffice/viajes/${data.id}`)
    } catch {
      setError('Error al crear el viaje. Intenta de nuevo.')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="p-8 max-w-2xl">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Nuevo viaje</h1>
      <div className="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Nombre del viaje *</label>
          <input name="nombre" value={form.nombre} onChange={handleChange} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" placeholder="Ej: Viaje a Machu Picchu 2026" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Destino *</label>
          <input name="destino" value={form.destino} onChange={handleChange} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" placeholder="Ej: Cusco, Peru" />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fecha de salida *</label>
            <input type="date" name="fecha_salida" value={form.fecha_salida} onChange={handleChange} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fecha de regreso *</label>
            <input type="date" name="fecha_regreso" value={form.fecha_regreso} onChange={handleChange} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Cupo maximo</label>
            <input type="number" name="cupo_maximo" value={form.cupo_maximo} onChange={handleChange} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Precio total (S/)</label>
            <input type="number" name="precio_total" value={form.precio_total} onChange={handleChange} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Descripcion</label>
          <textarea name="descripcion" value={form.descripcion} onChange={handleChange} rows={3} className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
        </div>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <div className="flex gap-3 pt-2">
          <button onClick={handleSubmit} disabled={enviando} className="bg-blue-800 text-white px-6 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 disabled:opacity-50">
            {enviando ? 'Creando...' : 'Crear viaje'}
          </button>
          <button onClick={() => router.back()} className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg text-sm hover:bg-gray-50">
            Cancelar
          </button>
        </div>
      </div>
    </div>
  )
}