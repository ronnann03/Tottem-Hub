'use strict';

/**
 * tests/cors.test.js — Tests de integración del middleware CORS.
 *
 * El origen permitido en Docker es http://localhost:3000 (CORS_ORIGINS env var).
 * Los tests verifican:
 *   - Requests sin Origin: pasan sin CORS headers (no cross-origin).
 *   - Origen autorizado GET: headers CORS presentes, respuesta normal.
 *   - Origen autorizado OPTIONS: preflight 204 con todos los headers requeridos.
 *   - Origen no autorizado: 403 sin headers CORS.
 */

const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const server = require('../server');

const ALLOWED_ORIGIN = 'http://localhost:3000';
const BLOCKED_ORIGIN = 'https://evil.com';

let port;

before(async () => {
  await new Promise((resolve) => server.listen(0, resolve));
  port = server.address().port;
});

after(async () => {
  await new Promise((resolve) => server.close(resolve));
});

function request(method, path, headers = {}) {
  return new Promise((resolve, reject) => {
    const opts = { hostname: 'localhost', port, path, method, headers };
    const req = http.request(opts, (res) => {
      let body = '';
      res.on('data', (c) => (body += c));
      res.on('end', () => {
        let parsed;
        try { parsed = JSON.parse(body); } catch { parsed = body; }
        resolve({ status: res.statusCode, headers: res.headers, body: parsed });
      });
    });
    req.on('error', reject);
    req.end();
  });
}

// ─── Sin header Origin (petición directa) ────────────────────────────────────

test('sin Origin: pasa sin CORS headers y retorna 200', async () => {
  const { status, headers } = await request('GET', '/health');
  assert.strictEqual(status, 200);
  assert.strictEqual(headers['access-control-allow-origin'], undefined);
});

// ─── Origen autorizado — requests normales ────────────────────────────────────

test('origen autorizado: GET añade Access-Control-Allow-Origin correcto', async () => {
  const { status, headers } = await request('GET', '/health', { origin: ALLOWED_ORIGIN });
  assert.strictEqual(status, 200);
  assert.strictEqual(headers['access-control-allow-origin'], ALLOWED_ORIGIN);
});

test('origen autorizado: respuesta incluye Access-Control-Allow-Credentials true', async () => {
  const { headers } = await request('GET', '/health', { origin: ALLOWED_ORIGIN });
  assert.strictEqual(headers['access-control-allow-credentials'], 'true');
});

test('origen autorizado: respuesta incluye Vary: Origin', async () => {
  const { headers } = await request('GET', '/health', { origin: ALLOWED_ORIGIN });
  assert.ok(headers['vary'] && headers['vary'].includes('Origin'));
});

// ─── Preflight OPTIONS ────────────────────────────────────────────────────────

test('origen autorizado + OPTIONS: responde 204 (preflight)', async () => {
  const { status } = await request('OPTIONS', '/health', {
    origin: ALLOWED_ORIGIN,
    'access-control-request-method': 'GET',
  });
  assert.strictEqual(status, 204);
});

test('preflight incluye Access-Control-Allow-Methods con GET y POST', async () => {
  const { headers } = await request('OPTIONS', '/health', {
    origin: ALLOWED_ORIGIN,
    'access-control-request-method': 'GET',
  });
  const methods = headers['access-control-allow-methods'] || '';
  assert.ok(methods.includes('GET'));
  assert.ok(methods.includes('POST'));
});

test('preflight incluye Access-Control-Allow-Headers', async () => {
  const { headers } = await request('OPTIONS', '/health', {
    origin: ALLOWED_ORIGIN,
    'access-control-request-method': 'POST',
    'access-control-request-headers': 'Content-Type',
  });
  assert.ok(headers['access-control-allow-headers']);
});

// ─── Origen no autorizado ─────────────────────────────────────────────────────

test('origen no autorizado: GET retorna 403', async () => {
  const { status } = await request('GET', '/health', { origin: BLOCKED_ORIGIN });
  assert.strictEqual(status, 403);
});

test('origen no autorizado: OPTIONS preflight también retorna 403', async () => {
  const { status } = await request('OPTIONS', '/health', {
    origin: BLOCKED_ORIGIN,
    'access-control-request-method': 'GET',
  });
  assert.strictEqual(status, 403);
});

test('origen no autorizado: respuesta no incluye Access-Control-Allow-Origin', async () => {
  const { headers } = await request('GET', '/health', { origin: BLOCKED_ORIGIN });
  assert.strictEqual(headers['access-control-allow-origin'], undefined);
});
