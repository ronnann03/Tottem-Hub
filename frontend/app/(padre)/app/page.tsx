import { InscripcionCard } from '@/components/padre/InscripcionCard'
import { AlertasPendientes } from '@/components/padre/AlertasPendientes'
import { HijosRegistrados } from '@/components/padre/HijosRegistrados'

import { cookies } from 'next/headers'

async function getInscripciones() {
  const cookieStore = await cookies()
  const token = cookieStore.get('access_token')?.value
  
  const gatewayUrl = 'http://127.0.0.1:3001'
  const headers: Record<string, string> = token ? { Cookie: `access_token=${token}` } : {}

  try {
    const res = await fetch(`${gatewayUrl}/api/v1/inscripciones/`, { 
      cache: 'no-store',
      headers
    })
    if (!res.ok) return []
    return await res.json()
  } catch (error) {
    console.error('Error fetching inscripciones:', error)
    return []
  }
}

export default async function DashboardPadrePage() {
  const inscripciones = await getInscripciones()

  const alertas = inscripciones.flatMap((ins: any) => {
    const a = []
    if (ins.pagos_resumen?.tiene_cuota_vencida) {
      a.push({ tipo: 'error' as const, titulo: 'Cuota vencida', mensaje: 'Tienes una cuota vencida en ' + ins.viaje.nombre, href: `/app/inscripciones/${ins.id}/pagos` })
    }
    if (ins.documentos_resumen?.tiene_rechazado) {
      a.push({ tipo: 'warning' as const, titulo: 'Documento rechazado', mensaje: 'Un documento fue rechazado en ' + ins.viaje.nombre, href: `/app/inscripciones/${ins.id}/documentos` })
    }
    return a
  })

  // Extract unique students
  const hijosMap = new Map()
  inscripciones.forEach((ins: any) => {
    if (!hijosMap.has(ins.alumno.id)) {
      hijosMap.set(ins.alumno.id, {
        id: ins.alumno.id,
        nombreCompleto: `${ins.alumno.nombre} ${ins.alumno.apellidos}`,
        colegio: ins.colegio || 'Sin colegio',
        gradoNivel: `${ins.grado || ''} ${ins.nivel_educativo || ''}`.trim() || 'Sin grado',
        alergias: ins.alergias || []
      })
    }
  })
  const hijosUnicos = Array.from(hijosMap.values())

  return (
    <div className="min-h-screen bg-gray-50 pb-16">
      <div className="max-w-3xl mx-auto pt-8 px-4">
        {/* Header Section */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Bienvenido</h1>
            <p className="text-sm text-gray-500 mt-1">Aquí puedes gestionar las inscripciones y viajes de tus hijos.</p>
          </div>
          <button className="flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-gray-800 transition-colors bg-white px-3 py-1.5 rounded-lg border border-gray-200 shadow-sm">
            <span className="material-symbols-outlined text-[18px]">help</span>
            Ayuda
          </button>
        </div>

        {/* Alertas */}
        <AlertasPendientes alertas={alertas} />

        {/* Inscripciones / Viajes Activos */}
        <div className="mb-8">
          <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Viajes Activos</h2>
          {inscripciones.length === 0 ? (
            <div className="bg-white border border-gray-200 rounded-xl p-10 text-center shadow-sm">
              <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">
                ✈️
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">No tienes viajes activos</h3>
              <p className="text-gray-500 text-sm mb-6 max-w-sm mx-auto">
                No tienes inscripciones activas en este momento. Si tu colegio organizó un viaje, búscalo para inscribir a tu hijo.
              </p>
              <a href="/app/buscar-viaje" className="inline-block px-6 py-2.5 bg-blue-700 text-white rounded-lg text-sm font-bold hover:bg-blue-800 transition-colors shadow-md">
                Buscar viaje escolar
              </a>
            </div>
          ) : (
            <div className="space-y-6">
              {inscripciones.map((ins: any) => (
                <InscripcionCard key={ins.id} inscripcion={ins} />
              ))}
            </div>
          )}
        </div>

        {/* Hijos Registrados */}
        <HijosRegistrados hijos={hijosUnicos} />

      </div>
    </div>
  )
}