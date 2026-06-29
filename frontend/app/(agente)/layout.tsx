import { NavBackoffice } from '@/components/agente/NavBackoffice'

export default function AgenteLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <NavBackoffice />
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  )
}