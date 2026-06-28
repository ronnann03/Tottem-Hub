export default function BackofficeDashboardPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard Administrativo</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-[var(--radius-card)] shadow-sm">
          <h2 className="text-gray-500 font-semibold mb-2">Viajes Activos</h2>
          <p className="text-4xl font-bold text-primary">12</p>
        </div>
        <div className="bg-white p-6 rounded-[var(--radius-card)] shadow-sm">
          <h2 className="text-gray-500 font-semibold mb-2">Pagos Pendientes</h2>
          <p className="text-4xl font-bold text-warning">5</p>
        </div>
      </div>
    </div>
  );
}
