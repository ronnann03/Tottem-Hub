import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Tottem Hub",
  description: "Plataforma de gestión de viajes",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="antialiased bg-gray-50 text-gray-900 min-h-screen">
        {children}
      </body>
    </html>
  );
}
