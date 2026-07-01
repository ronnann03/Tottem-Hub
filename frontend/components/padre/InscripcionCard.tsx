import { Badge } from '@/components/ui/Badge'
import { ProgressBar } from '@/components/ui/ProgressBar'
import { SubCardPagos } from './SubCardPagos'
import { SubCardDocumentos } from './SubCardDocumentos'
import { SubCardAlojamiento } from './SubCardAlojamiento'
import Link from 'next/link'
import Image from 'next/image'

const ESTADO_BADGE: Record<string, { variant: 'default' | 'warning' | 'success' | 'info', icon: string, label: string }> = {
  pre_inscrito: { variant: 'warning', icon: '○', label: 'Pre-inscrito' },
  pendiente: { variant: 'warning', icon: '○', label: 'Pendiente' },
  confirmado: { variant: 'success', icon: '✓', label: 'Confirmado' },
  cancelado: { variant: 'default', icon: '✕', label: 'Cancelado' },
  baja: { variant: 'default', icon: '↓', label: 'Baja' },
}

interface InscripcionCardProps {
  inscripcion: {
    id: string
    estado: string
    precio_final: number
    porcentaje_pagado: number
    viaje: { id: string; nombre: string; destino: string; fecha_salida: string; fecha_regreso: string; imagen_url?: string }
    alumno: { nombre: string; apellidos: string }
    colegio?: string
    pagos_resumen: { total_cuotas: number; cuotas_pagadas: number; tiene_cuota_vencida: boolean }
    documentos_resumen: { total_requeridos: number; total_validados: number; tiene_rechazado: boolean }
    hotel_asignado?: { nombre: string; maps_url: string }
  }
}

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
}

export function InscripcionCard({ inscripcion }: InscripcionCardProps) {
  const badge = ESTADO_BADGE[inscripcion.estado] ?? ESTADO_BADGE.pendiente
  
  return (
    <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden mb-8 transition-shadow hover:shadow-md">
      {/* Header section with image and basic info */}
      <div className="relative h-32 md:h-40 bg-gray-100 border-b border-gray-200">
        {inscripcion.viaje.imagen_url ? (
          <Image 
            src={inscripcion.viaje.imagen_url} 
            alt={inscripcion.viaje.destino} 
            fill 
            className="object-cover" 
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-700"></div>
        )}
        <div className="absolute inset-0 bg-black/40"></div>
        <div className="absolute inset-0 p-6 flex flex-col justify-end">
          <h2 className="text-xl md:text-2xl font-bold text-white mb-1 shadow-sm drop-shadow-md">
            {inscripcion.viaje.nombre}
          </h2>
          <div className="flex items-center gap-4 text-sm font-medium text-white/90 drop-shadow-sm">
            <span className="flex items-center gap-1">
              <span className="material-symbols-outlined text-[16px]">calendar_month</span>
              {formatDate(inscripcion.viaje.fecha_salida)} – {formatDate(inscripcion.viaje.fecha_regreso)}
            </span>
            <span className="flex items-center gap-1">
              <span className="material-symbols-outlined text-[16px]">school</span>
              {inscripcion.colegio || 'Colegio no especificado'}
            </span>
          </div>
        </div>
      </div>

      {/* Main content body */}
      <div className="p-6">
        {/* Student and Status */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-bold text-sm">
              {inscripcion.alumno.nombre.charAt(0)}
            </div>
            <span className="font-semibold text-gray-900">{inscripcion.alumno.nombre} {inscripcion.alumno.apellidos}</span>
          </div>
          <Badge text={badge.label} icon={badge.icon} variant={badge.variant} />
        </div>

        {/* Progress */}
        <div className="mb-6 bg-gray-50 p-4 rounded-lg border border-gray-100">
          <div className="flex justify-between items-end mb-2">
            <span className="text-xs font-bold text-gray-500 tracking-wider uppercase">Progreso de Inscripción</span>
            <span className="text-sm font-bold text-blue-700">{inscripcion.porcentaje_pagado}%</span>
          </div>
          <ProgressBar porcentaje={inscripcion.porcentaje_pagado} />
        </div>

        {/* Subcards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
          <SubCardPagos
            totalCuotas={inscripcion.pagos_resumen.total_cuotas}
            cuotasPagadas={inscripcion.pagos_resumen.cuotas_pagadas}
            tieneCuotaVencida={inscripcion.pagos_resumen.tiene_cuota_vencida}
            href={`/app/inscripciones/${inscripcion.id}/pagos`}
          />
          <SubCardDocumentos
            totalRequeridos={inscripcion.documentos_resumen.total_requeridos}
            totalValidados={inscripcion.documentos_resumen.total_validados}
            tieneRechazado={inscripcion.documentos_resumen.tiene_rechazado}
            href={`/app/inscripciones/${inscripcion.id}/documentos`}
          />
          <SubCardAlojamiento
            hotelNombre={inscripcion.hotel_asignado?.nombre}
            mapsUrl={inscripcion.hotel_asignado?.maps_url}
          />
        </div>

        {/* CTA Footer */}
        <div className="flex justify-end gap-3 pt-4 border-t border-gray-100">
          <Link href={`/app/inscripciones/${inscripcion.id}/pagos`} className="px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            💳 Ir a Pagos
          </Link>
          <Link href={`/app/inscripciones/${inscripcion.id}/documentos`} className="px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            📁 Subir Docs
          </Link>
          <Link href={`/app/inscripciones/${inscripcion.id}`} className="px-4 py-2 text-sm font-semibold text-white bg-blue-700 rounded-lg hover:bg-blue-800 transition-colors">
            Ver todo →
          </Link>
        </div>
      </div>
    </div>
  )
}