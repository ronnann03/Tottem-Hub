import Link from 'next/link'

interface Hijo {
  id: string
  nombreCompleto: string
  colegio: string
  gradoNivel: string
  alergias: string[]
}

interface HijosRegistradosProps {
  hijos: Hijo[]
}

export function HijosRegistrados({ hijos }: HijosRegistradosProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-bold text-gray-900 tracking-tight uppercase">Hijos Registrados</h2>
        <Link 
          href="/app/buscar-viaje" 
          className="text-sm font-medium text-blue-700 bg-blue-50 px-4 py-2 rounded-lg hover:bg-blue-100 transition-colors"
        >
          + Nuevo hijo
        </Link>
      </div>

      {hijos.length === 0 ? (
        <div className="text-center py-6">
          <p className="text-gray-500 text-sm">No tienes hijos registrados aún.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {hijos.map((hijo, index) => (
            <div key={hijo.id || index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-100">
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-bold text-lg shrink-0">
                  {hijo.nombreCompleto.charAt(0).toUpperCase()}
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">{hijo.nombreCompleto}</h3>
                  <p className="text-xs text-gray-500 mb-1">
                    {hijo.colegio || 'Sin colegio'} · {hijo.gradoNivel || 'Sin grado'}
                  </p>
                  <p className="text-xs text-amber-600 flex items-center gap-1">
                    <span className="material-symbols-outlined text-[14px]">warning</span>
                    Alergias: {hijo.alergias.join(', ')}
                  </p>
                </div>
              </div>
              <button className="text-sm text-gray-500 hover:text-blue-700 font-medium px-3 py-1.5 border border-gray-200 bg-white rounded shadow-sm hover:bg-gray-50 transition-colors">
                ✏️ Editar
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
