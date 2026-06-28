'use strict';

/**
 * middleware/cors.js — CORS implementado manualmente (sin librería).
 *
 * Comportamiento por caso:
 *   Sin header Origin  → request directo (no cross-origin). Pasa sin CORS headers.
 *   Origin autorizado + GET/POST/...  → añade headers CORS y llama next().
 *   Origin autorizado + OPTIONS       → preflight, responde 204 sin cuerpo.
 *   Origin no autorizado              → 403 sin headers CORS (ningún leak de info).
 *
 * Los orígenes permitidos se leen de config.CORS_ORIGINS (env var CORS_ORIGINS).
 * El header Vary: Origin indica a los caches que la respuesta varía por origen.
 */

const config = require('../config');

const ALLOW_METHODS = 'GET, POST, PUT, PATCH, DELETE, OPTIONS';
const ALLOW_HEADERS = 'Content-Type, Authorization, X-Requested-With, X-CSRF-Token';
const MAX_AGE = '86400'; // 24 h — cache del preflight en el browser

function cors(req, res, next) {
  const origin = req.headers['origin'];

  // Sin Origin: petición directa o same-origin. No aplica CORS.
  if (!origin) {
    next();
    return;
  }

  // Origin no autorizado
  if (!config.CORS_ORIGINS.includes(origin)) {
    res.writeHead(403, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Origin not allowed.' }));
    return;
  }

  // Origin autorizado — cabeceras CORS comunes a todos los métodos
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Methods', ALLOW_METHODS);
  res.setHeader('Access-Control-Allow-Headers', ALLOW_HEADERS);
  res.setHeader('Vary', 'Origin');

  // Preflight OPTIONS → respuesta inmediata 204
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Max-Age', MAX_AGE);
    res.writeHead(204);
    res.end();
    return;
  }

  next();
}

module.exports = cors;
