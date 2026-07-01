import { AlertCard } from '@/components/ui/AlertCard'

interface Alerta {
  tipo: 'warning' | 'error' | 'info'
  titulo: string
  mensaje: string
  href: string
}

interface AlertasPendientesProps {
  alertas: Alerta[]
}

export function AlertasPendientes({ alertas }: AlertasPendientesProps) {
  if (alertas.length === 0) return null
  return (
    <div className="mb-8">
      <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Alertas y Pendientes</h2>
      <div className="space-y-3">
        {alertas.map((alerta, i) => (
          <AlertCard 
            key={i} 
            tipo={alerta.tipo} 
            titulo={alerta.titulo} 
            mensaje={alerta.mensaje} 
            href={alerta.href} 
            icon={alerta.tipo === 'error' ? '🔴' : alerta.tipo === 'warning' ? '🟡' : '🔵'}
          />
        ))}
      </div>
    </div>
  )
}