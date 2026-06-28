'use strict';

/**
 * router.js — Mapa de rutas {method, path} → handler.
 *
 * Implementación mínima sin dependencias externas.
 * Matching exacto de path (no soporta parámetros dinámicos en esta fase).
 * La query string se ignora al hacer matching.
 *
 * Uso:
 *   const router = new Router();
 *   router.get('/health', handler);
 *   const fn = router.resolve('GET', '/health?foo=1');  // → handler
 */

class Router {
  constructor() {
    this._routes = [];
  }

  /** Registra una ruta para cualquier método HTTP. */
  add(method, path, handler) {
    this._routes.push({ method: method.toUpperCase(), path, handler });
  }

  /** Atajo para GET. */
  get(path, handler) {
    this.add('GET', path, handler);
  }

  /**
   * Busca el handler para (method, url).
   * Ignora la query string al comparar la ruta.
   * Retorna null si no hay coincidencia.
   */
  resolve(method, url) {
    const path = url.split('?')[0];
    const upperMethod = method.toUpperCase();
    for (const route of this._routes) {
      if (route.method === upperMethod && route.path === path) {
        return route.handler;
      }
    }
    return null;
  }
}

module.exports = Router;
