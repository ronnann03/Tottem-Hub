import Link from 'next/link'

async function getViajes() {
  const gatewayUrl = process.env.NEXT_PUBLIC_GATEWAY_INTERNAL_URL || process.env.NEXT_PUBLIC_GATEWAY_URL
  try {
    const res = await fetch(`${gatewayUrl}/api/v1/viajes/publico/`, { cache: 'no-store' })
    if (!res.ok) return []
    const data = await res.json()
    return data.results ?? data
  } catch {
    return []
  }
}

export default async function ViajesPublicPage() {
  const viajes = await getViajes()

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-blue-900 mb-2 text-center">Descubre nuestros Viajes</h1>
        <p className="text-gray-600 text-center mb-10">Explora las opciones de viajes de estudio y turismo.</p>

        {viajes.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <p className="text-5xl mb-4">✈️</p>
            <p className="font-medium text-lg">No hay viajes disponibles por el momento.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {viajes.map((v: any) => (
              <Link key={v.id} href={`/viajes/${v.slug}`} className="block bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow overflow-hidden">
                <div className="bg-blue-800 h-32 flex items-center justify-center">
                  <span className="text-4xl">✈️</span>
                </div>
                <div className="p-5">
                  <h2 className="font-bold text-gray-900 text-lg mb-1">{v.nombre}</h2>
                  <p className="text-sm text-gray-500 mb-3">📍 {v.destino}</p>
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-gray-500">📅 {v.fecha_salida}</span>
                    <span className="font-bold text-blue-800">S/ {v.precio_total}</span>
                  </div>
                  <div className="mt-4">
                    <span className="inline-block bg-blue-800 text-white text-xs px-3 py-1 rounded-full">Ver viaje →</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
