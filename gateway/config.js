'use strict';

/**
 * config.js — Configuración del Gateway leída desde variables de entorno.
 *
 * En Docker las vars vienen del bloque `environment` de docker-compose.
 * En desarrollo local se cargan desde .env mediante dotenv (si existe).
 * dotenv.config() no lanza si el archivo no existe.
 */

require('dotenv').config();

module.exports = {
  PORT: parseInt(process.env.PORT || '3001', 10),
  BACKEND_URL: process.env.BACKEND_URL || 'http://backend:8000',
  REDIS_URL: process.env.REDIS_URL || 'redis://redis:6379',
  CORS_ORIGINS: (process.env.CORS_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean),
  RATE_LIMIT_WINDOW_MS: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000', 10),
  RATE_LIMIT_MAX: parseInt(process.env.RATE_LIMIT_MAX || '100', 10),
  MAX_FILE_SIZE_BYTES: parseInt(process.env.MAX_FILE_SIZE_BYTES || '10485760', 10),
};
