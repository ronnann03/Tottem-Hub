export default function AgenteLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex">
      {/* TODO: Sidebar de navegación del Backoffice */}
      <aside className="w-64 bg-primary text-white hidden md:block border-r border-gray-200">
        <div className="p-4 font-bold text-lg border-b border-white/20">
          Tottem Hub
        </div>
        <nav className="p-4">
          <ul className="space-y-2">
            <li>Dashboard</li>
            <li>Viajes</li>
            <li>Inscripciones</li>
            <li>Pagos</li>
          </ul>
        </nav>
      </aside>
      <main className="flex-1 bg-gray-100 overflow-y-auto">
        {/* TODO: Topbar de usuario */}
        <header className="bg-white border-b border-gray-200 p-4 shadow-sm">
          Topbar Backoffice
        </header>
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
