// Node test of the V2 CSV load contract (assets/explore_load.js; Spec V2 「載入契約」, 次 seam).
//
//   node --test tests/js/explore_load.test.js
//
// One case per rejection reason, the cell rules (BOM, quotes, white space, scientific notation,
// negative numbers, empty cells), missing-row deletion, the target rule, and SR-V2-01: a LoadResult
// carries no kept / excluded state for any column (that is decided later, on the training rows).
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const L = require('../../assets/explore_load.js');

const UNIT = path.join(__dirname, '..', '..');

function rows(n, make) {
  const out = [];
  for (let i = 0; i < n; i++) out.push(make(i));
  return out.join('\n');
}
const header = 'a,b,y';
const okBody = rows(25, (i) => `${i},${i % 3 === 0 ? 'x' : 'z'},${2 * i + 1}`);

test('a well-formed CSV is accepted with column types, target and row counts', () => {
  const r = L.loadCsv(`${header}\n${okBody}\n`);
  assert.equal(r.ok, true);
  assert.deepEqual(r.columns, [{ name: 'a', index: 0, type: 'numeric' }, { name: 'b', index: 1, type: 'categorical' },
    { name: 'y', index: 2, type: 'numeric' }]);
  assert.deepEqual(r.target, { name: 'y', index: 2 });
  assert.equal(r.n_rows, 25);
  assert.equal(r.n_rows_read, 25);
  assert.equal(r.n_rows_dropped_missing, 0);
  assert.deepEqual(r.rows[3], [3, 'x', 7]);
});

test('SR-V2-01: the LoadResult has no kept / excluded state and no distribution of any column', () => {
  // a constant column and a 30-level categorical column: the load layer does not judge them
  const text = 'c,many,y\n' + rows(40, (i) => `1,L${i % 30},${i}`);
  const r = L.loadCsv(text);
  assert.equal(r.ok, true);
  const keys = new Set(Object.keys(r));
  assert.deepEqual([...keys].sort(), ['columns', 'limits', 'n_rows', 'n_rows_dropped_missing', 'n_rows_read', 'ok',
    'rows', 'sha256', 'target'].sort());
  r.columns.forEach((c) => assert.deepEqual(Object.keys(c).sort(), ['index', 'name', 'type']));
  const flat = JSON.stringify(r.columns) + JSON.stringify(r.target);
  for (const word of ['KEPT', 'EXCLUDED', 'status', 'levels', 'distinct', 'std', 'mean', 'baseline']) {
    assert.ok(!flat.includes(word), word);
  }
});

const reject = (text, reason, options) => {
  const r = L.loadCsv(text, options);
  assert.equal(r.ok, false, JSON.stringify(r).slice(0, 200));
  assert.equal(r.reason, reason, JSON.stringify(r.detail));
  assert.ok(L.REASONS.includes(r.reason));
  return r;
};

test('NOT_CSV: empty text, a single column, an unterminated quote, text after a closing quote', () => {
  reject('', 'NOT_CSV');
  reject('  \r\n \n', 'NOT_CSV');
  reject('justonecolumn\n1\n2\n', 'NOT_CSV');
  reject(`${header}\n"unterminated,1,2\n` + okBody, 'NOT_CSV');
  reject(`${header}\n"a"b,1,2\n` + okBody, 'NOT_CSV');
});

test('NO_HEADER: an empty column name, or a header that is all numbers', () => {
  reject(`a,,y\n${okBody}`, 'NO_HEADER');
  reject(`1,2,3\n${okBody}`, 'NO_HEADER');
});

test('RAGGED_ROWS: a data row with a different number of fields', () => {
  const r = reject(`${header}\n${okBody}\n1,2\n`, 'RAGGED_ROWS');
  assert.deepEqual(r.detail, { record: 26, expected: 3, found: 2 });
  reject(`${header}\n1,x,2,3\n${okBody}`, 'RAGGED_ROWS');
});

test('ENCODING: bytes that are not UTF-8, the replacement character, a NUL character', () => {
  const bytes = Buffer.concat([Buffer.from(`${header}\n`), Buffer.from([0xff, 0xfe, 0x41]), Buffer.from(`,x,1\n${okBody}`)]);
  reject(new Uint8Array(bytes), 'ENCODING');
  reject(`${header}\n�,x,1\n${okBody}`, 'ENCODING');
  reject(`${header}\n1\u0000,x,1\n${okBody}`, 'ENCODING');
});

test('TOO_LARGE: more rows or more columns than the load limits (never truncated)', () => {
  reject(`${header}\n${okBody}`, 'TOO_LARGE', { limits: { maxRows: 24 } });
  assert.equal(L.loadCsv(`${header}\n${okBody}`, { limits: { maxRows: 25 } }).ok, true);
  const wide = Array.from({ length: 61 }, (_, i) => `c${i}`).join(',');
  reject(`${wide}\n${Array.from({ length: 61 }, () => '1').join(',')}`, 'TOO_LARGE');
  assert.equal(L.LIMITS.maxRows, 50000);
  assert.equal(L.LIMITS.maxColumns, 60);
});

test('TOO_FEW_ROWS: fewer than 20 rows, also after the rows with a missing value are dropped', () => {
  reject(`${header}\n` + rows(19, (i) => `${i},x,${i}`), 'TOO_FEW_ROWS');
  const r = reject(`${header}\n` + rows(22, (i) => (i < 3 ? `${i},,${i}` : `${i},x,${i}`)), 'TOO_FEW_ROWS');
  assert.deepEqual(r.detail, { rows: 19, min_rows: 20, dropped_missing: 3 });
  assert.equal(L.loadCsv(`${header}\n` + rows(20, (i) => `${i},x,${i}`)).ok, true);
});

test('TARGET_NOT_NUMERIC: the default (last) or the chosen target must be numeric', () => {
  reject('a,y\n' + rows(25, (i) => `${i},v${i}`), 'TARGET_NOT_NUMERIC');
  reject(`${header}\n${okBody}`, 'TARGET_NOT_NUMERIC', { target: 'b' });
  const r = L.loadCsv(`${header}\n${okBody}`, { target: 'a' });
  assert.equal(r.ok, true);
  assert.deepEqual(r.target, { name: 'a', index: 0 });
  assert.deepEqual(L.loadCsv(`${header}\n${okBody}`, { target: 0 }).target, { name: 'a', index: 0 });
});

test('DUPLICATE_COLUMN: a repeated column name (after trimming)', () => {
  const r = reject(`a, a ,y\n${okBody}`, 'DUPLICATE_COLUMN');
  assert.deepEqual(r.detail, { name: 'a', columns: [0, 1] });
});

test('cells: BOM, quotes, white space, scientific notation, negative numbers, empty cells', () => {
  const text = '﻿"a" , b ,"y, value"\r\n' +
    rows(21, (i) => (i === 0 ? ' -1.5e3 ,"x, ""q""", 2E-2 ' : i === 1 ? '+.5,  z  ,-0' : i === 2 ? ',z,1' : `${i},"z",${-i}`))
      .replace(/\n/g, '\r\n') + '\r\n\r\n';
  const r = L.loadCsv(text);
  assert.equal(r.ok, true, JSON.stringify(r));
  assert.deepEqual(r.columns.map((c) => c.name), ['a', 'b', 'y, value']);
  assert.deepEqual(r.columns.map((c) => c.type), ['numeric', 'categorical', 'numeric']);
  assert.equal(r.n_rows_dropped_missing, 1);
  assert.equal(r.n_rows, 20);
  assert.deepEqual(r.rows[0], [-1500, 'x, "q"', 0.02]);
  assert.deepEqual(r.rows[1], [0.5, 'z', -0]);
  assert.equal(r.rows[2][0], 3);
  // the BOM is not part of the first name, but it is part of the hashed bytes
  assert.equal(r.sha256, L.sha256Hex(L.utf8Bytes(text)));
});

test('only literal decimal numbers make a numeric column (no hex, Infinity, NaN, separators, expressions)', () => {
  for (const bad of ['0x1A', 'Infinity', 'NaN', '1,000', '1_000', '2*3', '1e999', '１２', '1e', '.', '--1', '']) {
    assert.equal(L.isNumberLiteral(bad), false, bad);
  }
  for (const good of ['0', '-0', '+5', '5.', '.5', '1e5', '1E-5', '-2.5e+3', '007']) assert.equal(L.isNumberLiteral(good), true, good);
  const text = 'a,y\n' + rows(25, (i) => (i === 4 ? '0x1A,1' : `${i},${i}`));
  const r = L.loadCsv(text);
  assert.equal(r.ok, true);
  assert.equal(r.columns[0].type, 'categorical');
});

test('a quote inside an unquoted field is literal; quoted fields may hold line ends', () => {
  const text = 'name,y\n' + rows(24, (i) => `n${i},${i}`) + '\n12" pipe,1\n"two\nlines",2\n';
  const r = L.loadCsv(text);
  assert.equal(r.ok, true, JSON.stringify(r));
  assert.equal(r.n_rows, 26);
  assert.equal(r.rows[24][0], '12" pipe');
  assert.equal(r.rows[25][0], 'two\nlines');
});

test('the same content as text or as bytes gives the same result and the file sha256', () => {
  const bytes = fs.readFileSync(path.join(UNIT, 'assets', 'data', '50_Startups.csv'));
  const a = L.loadCsv(new Uint8Array(bytes));
  const b = L.loadCsv(bytes.toString('utf8'));
  assert.deepEqual(a, b);
  assert.equal(a.sha256, require('node:crypto').createHash('sha256').update(bytes).digest('hex'));
  assert.equal(a.n_rows, 50);
});

test('sha256 matches node:crypto on assorted inputs', () => {
  const crypto = require('node:crypto');
  for (const s of ['', 'abc', 'x'.repeat(55), 'y'.repeat(56), 'z'.repeat(64), '中文,測試\n'.repeat(300)]) {
    assert.equal(L.sha256Hex(L.utf8Bytes(s)), crypto.createHash('sha256').update(Buffer.from(s, 'utf8')).digest('hex'));
  }
});
