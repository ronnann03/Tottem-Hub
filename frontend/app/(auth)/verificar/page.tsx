"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { fetchApi, ApiError } from "@/lib/api";
import Link from "next/link";
import { Suspense } from "react";

function VerifyContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("El enlace de verificación no es válido o está incompleto.");
      return;
    }

    let isMounted = true;

    const verifyEmail = async () => {
      try {
        const result = await fetchApi(`/api/v1/auth/verificar/?token=${encodeURIComponent(token)}`, {
          method: "GET",
        });
        
        if (isMounted) {
          setStatus("success");
          setMessage(result.mensaje || "Cuenta activada correctamente. Ya puedes iniciar sesión.");
        }
      } catch (err: any) {
        if (isMounted) {
          setStatus("error");
          if (err instanceof ApiError) {
            setMessage(err.message || "No se pudo verificar el email.");
          } else {
            setMessage("Error de conexión al intentar verificar la cuenta.");
          }
        }
      }
    };

    verifyEmail();

    return () => {
      isMounted = false;
    };
  }, [token]);

  if (status === "loading") {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
        <p className="text-gray-600">Verificando tu cuenta...</p>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="text-center">
        <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
          <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold mb-2 text-gray-900">Error de verificación</h2>
        <p className="text-gray-600 mb-6">{message}</p>
        <Link
          href="/registro"
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-opacity-90"
        >
          Volver a registrarse
        </Link>
      </div>
    );
  }

  return (
    <div className="text-center">
      <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
        <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <h2 className="text-2xl font-bold mb-2 text-gray-900">¡Cuenta Activada!</h2>
      <p className="text-gray-600 mb-6">{message}</p>
      <Link
        href="/login"
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-opacity-90"
      >
        Ir al Login
      </Link>
    </div>
  );
}

export default function VerifyPage() {
  return (
    <Suspense fallback={<div className="text-center py-8 text-gray-500">Cargando...</div>}>
      <VerifyContent />
    </Suspense>
  );
}
