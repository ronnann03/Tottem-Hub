async function getInscripcionAlumno() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_GATEWAY_URL}/api/v1/inscripciones/`, { cache: 'no-store' })
  if (!res.ok) return null
  const data = await res.json()
  return data[0] ?? null
}

export default async function AlumnoPage() {
  const inscripcion = await getInscripcionAlumno()
  if (!inscripcion) return (
    <div className="p-12 text-center text-gray-500">
      <p className="text-4xl mb-4">✈️</p>
      <p>No tienes viajes asignados.</p>
    </div>
  )

  const viaje = inscripcion.viaje
  const etapas = viaje?.itinerario?.etapas ?? []
  const docs = inscripcion.documentos_resumen

  return (
    <div className="max-w-3xl mx-auto py-8 px-4 space-y-8">
      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
        <h2 className="text-xl font-bold text-gray-900">{viaje?.nombre}</h2>
        <p className="text-sm text-gray-500 mt-1">{viaje?.destino} · {viaje?.fecha_salida} al {viaje?.fecha_regreso}</p>
        <div className="mt-4 grid grid-cols-3 gap-3 text-center">
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-lg font-bold text-gray-800">{inscripcion.estado}</p>
            <p className="text-xs text-gray-500">Estado</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-lg font-bold text-green-700">{inscripcion.porcentaje_pagado}%</p>
            <p className="text-xs text-gray-500">Pagado</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-lg font-bold text-blue-700">{docs?.total_validados ?? 0}/{docs?.total_requeridos ?? 0}</p>
            <p className="text-xs text-gray-500">Documentos</p>
          </div>
        </div>
      </div>

      {etapas.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Itinerario</h3>
          <div className="space-y-3">
            {etapas.map((etapa: any) => (
              <div key={etapa.dia_numero} className="border-l-4 border-blue-800 pl-4">
                <p className="font-semibold text-sm text-blue-800">Dia {etapa.dia_numero}: {etapa.titulo}</p>
                <p className="text-xs text-gray-500 mt-1">{etapa.descripcion}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Documentacion</h3>
        {docs?.total_requeridos === 0 ? (
          <p className="text-sm text-gray-400">No hay documentos requeridos.</p>
        ) : (
          <div className="space-y-2">
            <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
              <div className="h-2 rounded-full bg-blue-500" style={{ width: `${docs?.total_requeridos > 0 ? (docs.total_validados / docs.total_requeridos) * 100 : 0}%` }} />
            </div>
            <p className="text-sm text-gray-600">{docs?.total_validados} de {docs?.total_requeridos} documentos validados</p>
            {docs?.tiene_rechazado && <p className="text-xs text-red-600">Tienes documentos rechazados — contacta a tu padre/tutor.</p>}
          </div>
        )}
      </div>
    </div>
  )
}