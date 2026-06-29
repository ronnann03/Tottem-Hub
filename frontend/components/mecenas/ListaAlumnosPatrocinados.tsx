'use client'
import { useState } from 'react'
import { FormularioPagoMecenas } from './FormularioPagoMecenas'

interface AlumnoPatrocinado {
  id: string
  mecenas: string
  inscripcion: { id: string; alumno: { nombre: string; apellidos: string }; viaje: { nombre: string }; porcentaje_pagado: number }
  monto_comprometido: number
  monto_pagado: number
}

interface ListaAlumnosPatrocinadosProps {
  alumnos: AlumnoPatrocinado[]
  mecenasId: string
}

export function ListaAlumnosPatrocinados({ alumnos, mecenasId }: ListaAlumnosPatrocinadosProps) {
  const [pagoAbierto, setPagoAbierto] = useState<string | null>(null)

  if (alumnos.length === 0) return (
    <div className="text-center py-12 text-gray-400">
      <p className="text-3xl mb-2">🎓</p>
      <p>No tienes alumnos patrocinados aun.</p>
    </div>
  )

  return (
    <div className="space-y-4">
      {alumnos.map(ap => {
        const porcentaje = ap.monto_comprometido > 0 ? Math.round((ap.monto_pagado / ap.monto_comprometido) * 100) : 0
        return (
          <div key={ap.id} className="bg-white border border-gray-200 rounded-xl p-5">
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="font-semibold text-gray-900">{ap.inscripcion.alumno.nombre} {ap.inscripcion.alumno.apellidos}</p>
                <p className="text-sm text-gray-500">{ap.inscripcion.viaje.nombre}</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-gray-500">Comprometido</p>
                <p className="font-bold text-gray-900">S/ {ap.monto_comprometido}</p>
              </div>
            </div>
            <div className="mb-3">
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>Pagado: S/ {ap.monto_pagado}</span>
                <span>{porcentaje}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="h-2 rounded-full bg-green-500 transition-all" style={{ width: `${Math.min(100, porcentaje)}%` }} />
              </div>
            </div>
            <button onClick={() => setPagoAbierto(pagoAbierto === ap.id ? null : ap.id)} className="text-xs text-blue-600 hover:underline">
              {pagoAbierto === ap.id ? 'Cancelar' : '+ Registrar pago'}
            </button>
            {pagoAbierto === ap.id && (
              <FormularioPagoMecenas
                mecenasId={mecenasId}
                inscripcionId={ap.inscripcion.id}
                nombreAlumno={ap.inscripcion.alumno.nombre}
                onExito={() => setPagoAbierto(null)}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}