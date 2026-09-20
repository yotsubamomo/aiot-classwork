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
  DEFAULT_STATE,
  NAME_MAX_LENGTH,
  THEMES,
  buildTimestampText,
  formatClockText,
  formatMilliseconds,
  formatTaipeiDate,
  isCity,
  isTheme,
  minuteProgress,
  nextTheme,
  normalizeState,
  ringDashOffset,
  sanitizeLine,
  stateFromLegacyPreferences,
  taipeiTimeParts,
  unixSeconds
} from '../core.js';

// 2026-09-20 14:30:05 台北時間（UTC+8）。
const AFTERNOON = new Date('2026-09-20T06:30:05Z');
// 2026-01-01 00:00:00 台北時間，用來檢查午夜的 12 小時制表示。
const MIDNIGHT = new Date('2025-12-31T16:00:00Z');
// 2026-06-15 12:00:00 台北時間，用來檢查正午的 12 小時制表示。
const NOON = new Date('2026-06-15T04:00:00Z');

// -----------------------------------------------------------------------------
// 時間與日期
// -----------------------------------------------------------------------------

test('24 小時制顯示補零的時分秒', () => {
  assert.equal(formatClockText(AFTERNOON, { format24h: true }), '14:30:05');
});

test('12 小時制把下午兩點半顯示為 02:30:05', () => {
  assert.equal(formatClockText(AFTERNOON, { format24h: false }), '02:30:05');
});

test('24 小時制的午夜是 00 點而不是 24 點', () => {
  assert.equal(formatClockText(MIDNIGHT, { format24h: true }), '00:00:00');
});

test('12 小時制的午夜是 12 AM', () => {
  const parts = taipeiTimeParts(MIDNIGHT, { format24h: false });
  assert.equal(parts.hour, '12');
  assert.equal(parts.dayPeriod, 'AM');
});

test('12 小時制的正午是 12 PM', () => {
  const parts = taipeiTimeParts(NOON, { format24h: false });
  assert.equal(parts.hour, '12');
  assert.equal(parts.dayPeriod, 'PM');
});

test('24 小時制沒有上下午標記', () => {
  assert.equal(taipeiTimeParts(AFTERNOON, { format24h: true }).dayPeriod, undefined);
});

test('時間依台北時區計算，不跟隨傳入時刻的 UTC 表示', () => {
  // 同一個時刻在 UTC 是 06:30，在台北是 14:30。
  assert.equal(AFTERNOON.toISOString(), '2026-09-20T06:30:05.000Z');
  assert.equal(formatClockText(AFTERNOON, { format24h: true }), '14:30:05');
});

test('日期包含完整年月日與星期', () => {
  assert.equal(formatTaipeiDate(AFTERNOON), 'Sunday, September 20, 2026');
});

test('跨日的時刻以台北日期為準', () => {
  // UTC 仍是 2025-12-31，但台北已經是 2026-01-01。
  assert.equal(formatTaipeiDate(MIDNIGHT), 'Thursday, January 1, 2026');
});

test('24 小時制的時間戳記文字含名稱、日期、時間與時區', () => {
  assert.equal(
    buildTimestampText(AFTERNOON, { format24h: true }),
    'Momo · Sunday, September 20, 2026 · 14:30:05 · Asia/Taipei (UTC+8)'
  );
});

test('12 小時制的時間戳記文字帶上下午標記', () => {
  assert.equal(
    buildTimestampText(AFTERNOON, { format24h: false }),
    'Momo · Sunday, September 20, 2026 · 02:30:05 PM · Asia/Taipei (UTC+8)'
  );
});

test('時間戳記使用狀態樹裡的名稱', () => {
  assert.match(buildTimestampText(AFTERNOON, { name: 'Ada' }), /^Ada · /);
});

// -----------------------------------------------------------------------------
// 秒數進度環、毫秒與 UNIX timestamp
// -----------------------------------------------------------------------------

test('整分鐘的進度是 0', () => {
  assert.equal(minuteProgress(new Date('2026-09-20T06:30:00.000Z')), 0);
});

test('半分鐘的進度是 0.5', () => {
  assert.equal(minuteProgress(new Date('2026-09-20T06:30:30.000Z')), 0.5);
});

test('59.999 秒的進度接近 1 但還沒滿', () => {
  const progress = minuteProgress(new Date('2026-09-20T06:30:59.999Z'));
  assert.ok(progress > 0.9999, `progress was ${progress}`);
  assert.ok(progress < 1, `progress was ${progress}`);
});

test('跨分鐘時進度歸零', () => {
  assert.equal(minuteProgress(new Date('2026-09-20T06:31:00.000Z')), 0);
});

test('毫秒也算進進度，同一秒內會持續前進', () => {
  const early = minuteProgress(new Date('2026-09-20T06:30:10.100Z'));
  const late = minuteProgress(new Date('2026-09-20T06:30:10.900Z'));
  assert.ok(late > early, '同一秒內的進度必須增加');
});

test('進度 0 時整圈留白，進度 1 時畫滿', () => {
  const circumference = 282.743;
  assert.equal(ringDashOffset(0, circumference), circumference);
  assert.equal(ringDashOffset(1, circumference), 0);
  assert.ok(Math.abs(ringDashOffset(0.5, circumference) - circumference / 2) < 0.001);
});

test('超出範圍的進度會被夾回 0 到 1', () => {
  const circumference = 282.743;
  assert.equal(ringDashOffset(-2, circumference), circumference);
  assert.equal(ringDashOffset(5, circumference), 0);
});

test('毫秒補零成三位數', () => {
  assert.equal(formatMilliseconds(new Date('2026-09-20T06:30:10.005Z')), '005');
  assert.equal(formatMilliseconds(new Date('2026-09-20T06:30:10.042Z')), '042');
  assert.equal(formatMilliseconds(new Date('2026-09-20T06:30:10.999Z')), '999');
  assert.equal(formatMilliseconds(new Date('2026-09-20T06:30:10.000Z')), '000');
});

test('UNIX timestamp 是無條件捨去到秒的 epoch 秒數', () => {
  assert.equal(unixSeconds(new Date('2026-09-20T06:30:05.000Z')), 1789885805);
  assert.equal(unixSeconds(new Date('2026-09-20T06:30:05.999Z')), 1789885805);
});

test('UNIX timestamp 不受顯示時區影響', () => {
  // 同一個時刻不論以哪個時區呈現，epoch 秒數都一樣。
  assert.equal(unixSeconds(AFTERNOON), Math.floor(AFTERNOON.getTime() / 1000));
});

// -----------------------------------------------------------------------------
// 主題與城市
// -----------------------------------------------------------------------------

test('主題依固定順序循環', () => {
  assert.equal(nextTheme('aurora'), 'minimal');
  assert.equal(nextTheme('minimal'), 'sunset');
  assert.equal(nextTheme('sunset'), 'aurora');
});

test('未知主題循環後回到第一個主題', () => {
  assert.equal(nextTheme('unknown'), THEMES[0]);
});

test('預設主題是深色的 Cyber Ambient（aurora）', () => {
  assert.equal(DEFAULT_STATE.theme, 'aurora');
});

test('只有清單內的值算是合法主題', () => {
  assert.equal(isTheme('sunset'), true);
  assert.equal(isTheme('SUNSET'), false);
  assert.equal(isTheme(undefined), false);
});

test('只有清單內的值算是合法城市', () => {
  assert.equal(isCity('taichung'), true);
  assert.equal(isCity('Taichung'), false);
  assert.equal(isCity('tokyo'), false);
});

// -----------------------------------------------------------------------------
// 單行文字清理
// -----------------------------------------------------------------------------

test('清理文字會去除前後空白', () => {
  assert.equal(sanitizeLine('  Momo  '), 'Momo');
});

test('清理文字會把換行與連續空白收斂成單一空格', () => {
  assert.equal(sanitizeLine('Momo\n\nthe\t  builder'), 'Momo the builder');
});

test('清理文字會截斷超長輸入', () => {
  const long = 'x'.repeat(NAME_MAX_LENGTH + 20);
  assert.equal(sanitizeLine(long).length, NAME_MAX_LENGTH);
});

test('空白字串與非字串回退到 fallback', () => {
  assert.equal(sanitizeLine('   ', { fallback: 'Momo' }), 'Momo');
  assert.equal(sanitizeLine(null, { fallback: 'Momo' }), 'Momo');
  assert.equal(sanitizeLine(42, { fallback: 'Momo' }), 'Momo');
});

// -----------------------------------------------------------------------------
// 狀態樹正規化
// -----------------------------------------------------------------------------

test('沒有已保存狀態時使用預設值', () => {
  assert.deepEqual(normalizeState(null), DEFAULT_STATE);
  assert.deepEqual(normalizeState(undefined), DEFAULT_STATE);
  assert.deepEqual(normalizeState({}), DEFAULT_STATE);
});

test('正規化後永遠是完整的七個欄位', () => {
  assert.deepEqual(
    Object.keys(normalizeState({ theme: 'aurora' })).sort(),
    ['format24h', 'name', 'selectedCity', 'soundEnabled', 'tagline', 'theme', 'zenMode']
  );
});

test('保留合法的已保存狀態', () => {
  const saved = {
    name: 'Ada',
    tagline: 'Edge AI',
    theme: 'aurora',
    format24h: false,
    soundEnabled: true,
    selectedCity: 'tainan',
    zenMode: true
  };
  assert.deepEqual(normalizeState(saved), saved);
});

test('缺少的欄位各自回退到預設，不影響其他欄位', () => {
  const result = normalizeState({ theme: 'minimal', soundEnabled: true });
  assert.equal(result.theme, 'minimal');
  assert.equal(result.soundEnabled, true);
  assert.equal(result.name, DEFAULT_STATE.name);
  assert.equal(result.selectedCity, DEFAULT_STATE.selectedCity);
});

test('未知主題值回退到預設主題', () => {
  assert.equal(normalizeState({ theme: 'neon' }).theme, DEFAULT_STATE.theme);
});

test('未知城市值回退到預設城市', () => {
  assert.equal(normalizeState({ selectedCity: 'tokyo' }).selectedCity, DEFAULT_STATE.selectedCity);
});

test('型別錯誤的布林欄位回退到預設值', () => {
  const result = normalizeState({ format24h: 'yes', soundEnabled: 1, zenMode: 'true' });
  assert.equal(result.format24h, DEFAULT_STATE.format24h);
  assert.equal(result.soundEnabled, DEFAULT_STATE.soundEnabled);
  assert.equal(result.zenMode, DEFAULT_STATE.zenMode);
});

test('名稱與標語會被清理，空值回退到預設', () => {
  const result = normalizeState({ name: '  Ada\nLovelace ', tagline: '   ' });
  assert.equal(result.name, 'Ada Lovelace');
  assert.equal(result.tagline, DEFAULT_STATE.tagline);
});

test('丟棄未知欄位', () => {
  const result = normalizeState({ theme: 'minimal', injected: '<script>', apiKey: 'secret' });
  assert.equal(result.injected, undefined);
  assert.equal(result.apiKey, undefined);
});

test('非物件的輸入不會造成例外', () => {
  assert.deepEqual(normalizeState('sunset'), DEFAULT_STATE);
  assert.deepEqual(normalizeState(42), DEFAULT_STATE);
  assert.deepEqual(normalizeState([]), DEFAULT_STATE);
});

test('正規化不會改動傳入的物件', () => {
  const raw = { theme: 'aurora' };
  normalizeState(raw);
  assert.deepEqual(raw, { theme: 'aurora' });
});

// -----------------------------------------------------------------------------
// 舊偏好搬移
// -----------------------------------------------------------------------------

test('舊偏好的主題與時間格式會被搬到新狀態樹', () => {
  const result = stateFromLegacyPreferences({ theme: 'minimal', format24: false });
  assert.equal(result.theme, 'minimal');
  assert.equal(result.format24h, false);
});

test('舊偏好沒有的欄位使用預設值', () => {
  const result = stateFromLegacyPreferences({ theme: 'minimal', format24: false });
  assert.equal(result.name, DEFAULT_STATE.name);
  assert.equal(result.soundEnabled, DEFAULT_STATE.soundEnabled);
  assert.equal(result.selectedCity, DEFAULT_STATE.selectedCity);
  assert.equal(result.zenMode, DEFAULT_STATE.zenMode);
});

test('沒有舊偏好或格式無法辨識時使用預設狀態', () => {
  assert.deepEqual(stateFromLegacyPreferences(null), DEFAULT_STATE);
  assert.deepEqual(stateFromLegacyPreferences({ theme: 'neon', format24: 'yes' }), DEFAULT_STATE);
});
