'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const NAV_ITEMS = [
  { href: '/backoffice/viajes', label: 'Viajes', icon: '✈️' },
  { href: '/backoffice/inscripciones', label: 'Inscripciones', icon: '👥' },
  { href: '/backoffice/pagos', label: 'Pagos', icon: '💳' },
  { href: '/backoffice/documentos', label: 'Documentos', icon: '📄' },
  { href: '/backoffice/comunicados', label: 'Comunicados', icon: '📢' },
  { href: '/backoffice/notificaciones', label: 'Notificaciones', icon: '🔔' },
]

export function NavBackoffice() {
  const pathname = usePathname()
  return (
    <aside className="w-64 min-h-screen bg-blue-900 text-white flex flex-col">
      <div className="px-6 py-5 border-b border-blue-800">
        <h1 className="font-bold text-lg">Tottem Hub</h1>
        <p className="text-xs text-blue-300 mt-0.5">Panel de agente</p>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV_ITEMS.map(item => {
          const activo = pathname.startsWith(item.href)
          return (
            <Link key={item.href} href={item.href} className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${activo ? 'bg-blue-700 text-white' : 'text-blue-200 hover:bg-blue-800 hover:text-white'}`}>
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>
      <div className="px-6 py-4 border-t border-blue-800">
        <Link href="/login" className="text-xs text-blue-300 hover:text-white">Cerrar sesion</Link>
      </div>
    </aside>
  )
}