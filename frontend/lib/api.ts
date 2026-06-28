const GATEWAY_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || 'http://localhost:3001';

export class ApiError extends Error {
  status: number;
  data: any;

  constructor(status: number, data: any) {
    super(data.detail || data.error || 'API Error');
    this.status = status;
    this.data = data;
  }
}

export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const url = `${GATEWAY_URL}${endpoint}`;
  
  // Incluimos credenciales para que se envíe/reciba la cookie httpOnly access_token
  const finalOptions: RequestInit = {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };

  const response = await fetch(url, finalOptions);

  if (!response.ok) {
    let errorData = {};
    try {
      errorData = await response.json();
    } catch {
      errorData = { error: 'Error inesperado del servidor' };
    }
    throw new ApiError(response.status, errorData);
  }

  // Si es 204 No Content, no intentamos parsear JSON
  if (response.status === 204) {
    return null;
  }

  return response.json();
}
