import { redirect } from "next/navigation";

export default function RootPage() {
  // En Next.js App Router con grupos, la página raíz suele redirigir
  // a la landing pública o manejar el home global.
  // Por ahora redirigimos a la landing de viajes
  redirect("/viajes");
}
