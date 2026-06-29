import Link from 'next/link'

export default function AlumnoLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-800 text-white px-6 py-4 flex items-center justify-between">
        <h1 className="font-bold text-lg">Tottem Hub — Portal Alumno</h1>
        <Link href="/login" className="text-xs text-blue-200 hover:text-white">Cerrar sesion</Link>
      </header>
      <main>{children}</main>
    </div>
  )
}