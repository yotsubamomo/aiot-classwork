/**
 * core.js 的行為測試。
 *
 * 測試只驗證外部行為：給定輸入得到什麼輸出，不碰內部實作。
 * 需要時間的測試一律傳入固定的 Date，不依賴執行當下的時間。
 *
 * 執行方式（不需要安裝任何套件）：
 *   node --test
 */

import test from 'node:test';
import assert from 'node:assert/strict';

import {
  DEFAULT_PREFERENCES,
  THEMES,
  buildTimestampText,
  formatClockText,
  formatTaipeiDate,
  isTheme,
  nextTheme,
  normalizePreferences,
  taipeiTimeParts
} from '../core.js';

// 2026-09-20 14:30:05 台北時間（UTC+8）。
const AFTERNOON = new Date('2026-09-20T06:30:05Z');
// 2026-01-01 00:00:00 台北時間，用來檢查午夜的 12 小時制表示。
const MIDNIGHT = new Date('2025-12-31T16:00:00Z');
// 2026-06-15 12:00:00 台北時間，用來檢查正午的 12 小時制表示。
const NOON = new Date('2026-06-15T04:00:00Z');

test('24 小時制顯示補零的時分秒', () => {
  assert.equal(formatClockText(AFTERNOON, { format24: true }), '14:30:05');
});

test('12 小時制把下午兩點半顯示為 02:30:05', () => {
  assert.equal(formatClockText(AFTERNOON, { format24: false }), '02:30:05');
});

test('24 小時制的午夜是 00 點而不是 24 點', () => {
  assert.equal(formatClockText(MIDNIGHT, { format24: true }), '00:00:00');
});

test('12 小時制的午夜是 12 AM', () => {
  const parts = taipeiTimeParts(MIDNIGHT, { format24: false });
  assert.equal(parts.hour, '12');
  assert.equal(parts.dayPeriod, 'AM');
});

test('12 小時制的正午是 12 PM', () => {
  const parts = taipeiTimeParts(NOON, { format24: false });
  assert.equal(parts.hour, '12');
  assert.equal(parts.dayPeriod, 'PM');
});

test('24 小時制沒有上下午標記', () => {
  assert.equal(taipeiTimeParts(AFTERNOON, { format24: true }).dayPeriod, undefined);
});

test('時間依台北時區計算，不跟隨傳入時刻的 UTC 表示', () => {
  // 同一個時刻在 UTC 是 06:30，在台北是 14:30。
  assert.equal(AFTERNOON.toISOString(), '2026-09-20T06:30:05.000Z');
  assert.equal(formatClockText(AFTERNOON, { format24: true }), '14:30:05');
});

test('日期包含完整年月日與星期', () => {
  assert.equal(formatTaipeiDate(AFTERNOON), '2026年9月20日 星期日');
});

test('跨日的時刻以台北日期為準', () => {
  // UTC 仍是 2025-12-31，但台北已經是 2026-01-01。
  assert.equal(formatTaipeiDate(MIDNIGHT), '2026年1月1日 星期四');
});

test('24 小時制的時間戳記文字含名稱、日期、時間與時區', () => {
  assert.equal(
    buildTimestampText(AFTERNOON, { format24: true }),
    'Momo｜2026年9月20日 星期日 14:30:05｜Asia/Taipei (UTC+8)'
  );
});

test('12 小時制的時間戳記文字帶上下午標記', () => {
  assert.equal(
    buildTimestampText(AFTERNOON, { format24: false }),
    'Momo｜2026年9月20日 星期日 02:30:05 PM｜Asia/Taipei (UTC+8)'
  );
});

test('時間戳記可以使用自訂名稱', () => {
  assert.match(buildTimestampText(AFTERNOON, { name: 'Ada' }), /^Ada｜/);
});

test('主題依固定順序循環', () => {
  assert.equal(nextTheme('aurora'), 'minimal');
  assert.equal(nextTheme('minimal'), 'sunset');
  assert.equal(nextTheme('sunset'), 'aurora');
});

test('未知主題循環後回到第一個主題', () => {
  assert.equal(nextTheme('unknown'), THEMES[0]);
});

test('只有清單內的值算是合法主題', () => {
  assert.equal(isTheme('sunset'), true);
  assert.equal(isTheme('SUNSET'), false);
  assert.equal(isTheme(undefined), false);
});

test('沒有已保存偏好時使用預設值', () => {
  assert.deepEqual(normalizePreferences(null), DEFAULT_PREFERENCES);
  assert.deepEqual(normalizePreferences(undefined), DEFAULT_PREFERENCES);
  assert.deepEqual(normalizePreferences({}), DEFAULT_PREFERENCES);
});

test('保留合法的已保存偏好', () => {
  assert.deepEqual(
    normalizePreferences({ theme: 'aurora', format24: false }),
    { theme: 'aurora', format24: false }
  );
});

test('未知主題值回退到預設主題', () => {
  assert.equal(normalizePreferences({ theme: 'neon' }).theme, DEFAULT_PREFERENCES.theme);
});

test('型別錯誤的時間格式回退到預設值', () => {
  assert.equal(normalizePreferences({ format24: 'yes' }).format24, DEFAULT_PREFERENCES.format24);
});

test('丟棄未知欄位', () => {
  assert.deepEqual(
    normalizePreferences({ theme: 'minimal', format24: true, zenMode: true, injected: '<script>' }),
    { theme: 'minimal', format24: true }
  );
});

test('非物件的輸入不會造成例外', () => {
  assert.deepEqual(normalizePreferences('sunset'), DEFAULT_PREFERENCES);
  assert.deepEqual(normalizePreferences(42), DEFAULT_PREFERENCES);
  assert.deepEqual(normalizePreferences([]), DEFAULT_PREFERENCES);
});
