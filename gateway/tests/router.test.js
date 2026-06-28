'use strict';

/**
 * tests/router.test.js — Tests unitarios del Router.
 * Node.js 20 built-in test runner (node:test + node:assert).
 */

const { test } = require('node:test');
const assert = require('node:assert/strict');
const Router = require('../router');

test('resolve retorna el handler para ruta y método exactos', () => {
  const router = new Router();
  const handler = () => {};
  router.get('/health', handler);
  assert.strictEqual(router.resolve('GET', '/health'), handler);
});

test('resolve retorna null para ruta desconocida', () => {
  const router = new Router();
  assert.strictEqual(router.resolve('GET', '/unknown'), null);
});

test('resolve ignora la query string al hacer matching', () => {
  const router = new Router();
  const handler = () => {};
  router.get('/health', handler);
  assert.strictEqual(router.resolve('GET', '/health?foo=bar&x=1'), handler);
});

test('resolve es insensible al case del método HTTP', () => {
  const router = new Router();
  const handler = () => {};
  router.add('get', '/test', handler);
  assert.strictEqual(router.resolve('GET', '/test'), handler);
  assert.strictEqual(router.resolve('get', '/test'), handler);
});

test('add registra rutas DELETE y PATCH correctamente', () => {
  const router = new Router();
  const del = () => {};
  const patch = () => {};
  router.add('DELETE', '/resource', del);
  router.add('PATCH', '/resource', patch);
  assert.strictEqual(router.resolve('DELETE', '/resource'), del);
  assert.strictEqual(router.resolve('PATCH', '/resource'), patch);
  assert.strictEqual(router.resolve('GET', '/resource'), null);
});
