import { cookies } from 'next/headers'

async function getDashboardData() {
  const cookieStore = await cookies()
  const token = cookieStore.get('access_token')?.value
  const gatewayUrl = process.env.NEXT_PUBLIC_GATEWAY_INTERNAL_URL || process.env.NEXT_PUBLIC_GATEWAY_URL
  const headers: Record<string, string> = token ? { Cookie: `access_token=${token}` } : {}
  const [viajesRes, pagosRes] = await Promise.all([
    fetch(`${gatewayUrl}/api/v1/viajes/`, { cache: 'no-store', headers }),
    fetch(`${gatewayUrl}/api/v1/pagos/`, { cache: 'no-store', headers }),
  ])

  const viajesData = viajesRes.ok ? await viajesRes.json() : []
  const pagosData = pagosRes.ok ? await pagosRes.json() : []

  const viajes = viajesData.results ?? viajesData
  const pagos = pagosData.results ?? pagosData

  const viajesActivos = Array.isArray(viajes)
    ? viajes.filter((v: any) => v.estado === 'publicado').length
    : 0
  const pagosPendientes = Array.isArray(pagos)
    ? pagos.filter((p: any) => p.estado === 'pendiente').length
    : 0

  return { viajesActivos, pagosPendientes }
}

export default async function BackofficeDashboardPage() {
  const { viajesActivos, pagosPendientes } = await getDashboardData()
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard Administrativo</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-[var(--radius-card)] shadow-sm">
          <h2 className="text-gray-500 font-semibold mb-2">Viajes Activos</h2>
          <p className="text-4xl font-bold text-primary">{viajesActivos}</p>
        </div>
        <div className="bg-white p-6 rounded-[var(--radius-card)] shadow-sm">
          <h2 className="text-gray-500 font-semibold mb-2">Pagos Pendientes</h2>
          <p className="text-4xl font-bold text-warning">{pagosPendientes}</p>
        </div>
      </div>
    </div>
  );
}
