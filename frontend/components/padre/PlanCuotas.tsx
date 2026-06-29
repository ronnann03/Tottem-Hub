interface Cuota {
  id: string
  numero_cuota: number
  descripcion: string
  importe: number
  fecha_vencimiento: string
  estado?: 'pagado' | 'revision' | 'pendiente' | 'vencida'
}

interface PlanCuotasProps {
  cuotas: Cuota[]
  totalPagado: number
  saldoPendiente: number
}

const ESTADO_CONFIG = {
  pagado:   { color: 'bg-green-100 text-green-800 border-green-200', icon: '✓', label: 'Pagado' },
  revision: { color: 'bg-yellow-100 text-yellow-800 border-yellow-200', icon: '⏳', label: 'En revision' },
  pendiente:{ color: 'bg-gray-100 text-gray-600 border-gray-200', icon: '○', label: 'Pendiente' },
  vencida:  { color: 'bg-red-100 text-red-800 border-red-200', icon: '!', label: 'Vencida' },
}

export function PlanCuotas({ cuotas, totalPagado, saldoPendiente }: PlanCuotasProps) {
  return (
    <div>
      <h2 className="text-lg font-bold text-gray-900 mb-4">Plan de pagos</h2>
      <div className="space-y-3 mb-6">
        {cuotas.map((cuota) => {
          const estado = cuota.estado ?? 'pendiente'
          const cfg = ESTADO_CONFIG[estado]
          const vencida = new Date(cuota.fecha_vencimiento) < new Date() && estado === 'pendiente'
          const estadoFinal = vencida ? 'vencida' : estado
          const cfgFinal = ESTADO_CONFIG[estadoFinal]
          return (
            <div key={cuota.id} className={`border rounded-lg p-4 flex items-center justify-between ${cfgFinal.color}`}>
              <div>
                <p className="font-semibold text-sm">Cuota {cuota.numero_cuota}: {cuota.descripcion}</p>
                <p className="text-xs mt-0.5">Vence: {cuota.fecha_vencimiento}</p>
              </div>
              <div className="text-right">
                <p className="font-bold">S/ {cuota.importe}</p>
                <span className="text-xs">{cfgFinal.icon} {cfgFinal.label}</span>
              </div>
            </div>
          )
        })}
      </div>
      <div className="bg-gray-50 rounded-lg p-4 flex justify-between text-sm">
        <div><p className="text-gray-500">Total pagado</p><p className="font-bold text-green-700">S/ {totalPagado}</p></div>
        <div className="text-right"><p className="text-gray-500">Saldo pendiente</p><p className="font-bold text-red-700">S/ {saldoPendiente}</p></div>
      </div>
    </div>
  )
}