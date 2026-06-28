'use strict';

/**
 * tests/server.test.js — Tests de integración del servidor HTTP.
 *
 * Inicia el servidor en un puerto aleatorio (port 0), hace requests reales
 * via node:http y verifica las respuestas. El servidor se cierra al terminar.
 */

const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const server = require('../server');

let baseUrl;

before(async () => {
  await new Promise((resolve) => server.listen(0, resolve));
  baseUrl = `http://localhost:${server.address().port}`;
});

after(async () => {
  await new Promise((resolve) => server.close(resolve));
});

function request(method, path) {
  return new Promise((resolve, reject) => {
    const opts = new URL(`${baseUrl}${path}`);
    http.request(opts, { method }, (res) => {
      let body = '';
      res.on('data', (chunk) => (body += chunk));
      res.on('end', () => {
        resolve({ status: res.statusCode, body: JSON.parse(body), headers: res.headers });
      });
    }).on('error', reject).end();
  });
}

test('GET /health responde 200 con {status:"ok"}', async () => {
  const { status, body } = await request('GET', '/health');
  assert.strictEqual(status, 200);
  assert.deepStrictEqual(body, { status: 'ok' });
});

test('GET /health retorna Content-Type application/json', async () => {
  const { headers } = await request('GET', '/health');
  assert.ok(headers['content-type'].includes('application/json'));
});

test('ruta desconocida retorna 404 con campo error', async () => {
  const { status, body } = await request('GET', '/ruta-inexistente');
  assert.strictEqual(status, 404);
  assert.ok('error' in body);
});

test('POST /health retorna 404 (solo GET está registrado)', async () => {
  const { status } = await request('POST', '/health');
  assert.strictEqual(status, 404);
});
