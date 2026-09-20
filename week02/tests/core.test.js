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
  CITIES,
  CITY_IDS,
  DEFAULT_STATE,
  DRAWER_TABS,
  GREETINGS,
  MAX_TECH_TAGS,
  NAME_MAX_LENGTH,
  THEMES,
  TICK_SOUND,
  buildTimestampText,
  dayOfYear,
  describeWeatherCode,
  findCity,
  formatClockText,
  formatMilliseconds,
  formatTaipeiDate,
  formatTemperature,
  formatWeatherReadout,
  greeting,
  greetingKey,
  initialsFrom,
  isCity,
  isDrawerTab,
  isTheme,
  isoWeek,
  minuteProgress,
  nextTabIndex,
  nextTheme,
  normalizeProject,
  normalizeProjects,
  normalizeState,
  normalizeWeather,
  ringDashOffset,
  safeUrl,
  sanitizeLine,
  shortcutAction,
  splitDisplayName,
  stateFromLegacyPreferences,
  taipeiCalendarDate,
  taipeiTimeParts,
  unixSeconds,
  weatherApiUrl
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
// 日曆：年積日與 ISO 週數
// -----------------------------------------------------------------------------

test('日曆日期以台北為準，不是 UTC 的日期', () => {
  // UTC 還是 9/20 下午，台北已經是 9/21 凌晨。
  const afterTaipeiMidnight = new Date('2026-09-20T16:30:00Z');
  assert.deepEqual(taipeiCalendarDate(afterTaipeiMidnight), { year: 2026, month: 9, day: 21 });
  assert.equal(dayOfYear(afterTaipeiMidnight), 264);
});

test('年積日從 1 月 1 日的第 1 天開始算', () => {
  assert.equal(dayOfYear(MIDNIGHT), 1);
});

test('平年 3 月 1 日是第 60 天', () => {
  assert.equal(dayOfYear(new Date('2026-03-01T04:00:00Z')), 60);
});

test('閏年 2 月 29 日是第 60 天、3 月 1 日是第 61 天', () => {
  assert.equal(dayOfYear(new Date('2028-02-29T04:00:00Z')), 60);
  assert.equal(dayOfYear(new Date('2028-03-01T04:00:00Z')), 61);
});

test('平年的最後一天是第 365 天，閏年是第 366 天', () => {
  assert.equal(dayOfYear(new Date('2026-12-31T04:00:00Z')), 365);
  assert.equal(dayOfYear(new Date('2028-12-31T04:00:00Z')), 366);
});

test('一般日期的 ISO 週數', () => {
  assert.deepEqual(isoWeek(AFTERNOON), { week: 38, isoYear: 2026 });
});

test('1 月 1 日是星期四時屬於當年的第 1 週', () => {
  // 2026-01-01 是星期四。
  assert.deepEqual(isoWeek(MIDNIGHT), { week: 1, isoYear: 2026 });
});

test('年初幾天可能仍屬於前一年的最後一週', () => {
  // 台北的 2027-01-01 是星期五，依 ISO 屬於 2026 年第 53 週。
  assert.deepEqual(isoWeek(new Date('2026-12-31T16:30:00Z')), { week: 53, isoYear: 2026 });
  // 台北的 2028-01-01 是星期六，屬於 2027 年第 52 週。
  assert.deepEqual(isoWeek(new Date('2027-12-31T16:30:00Z')), { week: 52, isoYear: 2027 });
});

test('年底可能出現第 53 週', () => {
  assert.deepEqual(isoWeek(new Date('2026-12-31T04:00:00Z')), { week: 53, isoYear: 2026 });
});

test('閏年 2 月 29 日與 3 月 1 日落在同一週', () => {
  assert.deepEqual(isoWeek(new Date('2028-02-29T04:00:00Z')), { week: 9, isoYear: 2028 });
  assert.deepEqual(isoWeek(new Date('2028-03-01T04:00:00Z')), { week: 9, isoYear: 2028 });
});

// -----------------------------------------------------------------------------
// 時段問候語
// -----------------------------------------------------------------------------

test('問候語依台北時間的時段變化', () => {
  const at = (taipeiTime) => greetingKey(new Date(taipeiTime));
  // 台北時間 = UTC + 8，測試值直接寫成對應的 UTC 時刻。
  assert.equal(at('2026-09-19T21:00:00Z'), 'morning');   // 台北 05:00
  assert.equal(at('2026-09-20T02:00:00Z'), 'morning');   // 台北 10:00
  assert.equal(at('2026-09-20T04:00:00Z'), 'afternoon'); // 台北 12:00
  assert.equal(at('2026-09-20T08:00:00Z'), 'afternoon'); // 台北 16:00
  assert.equal(at('2026-09-20T10:00:00Z'), 'evening');   // 台北 18:00
  assert.equal(at('2026-09-20T13:00:00Z'), 'evening');   // 台北 21:00
  assert.equal(at('2026-09-20T14:00:00Z'), 'night');     // 台北 22:00
  assert.equal(at('2026-09-20T18:00:00Z'), 'night');     // 台北隔日 02:00
});

test('時段交界的前一分鐘仍屬於前一個時段', () => {
  assert.equal(greetingKey(new Date('2026-09-19T20:59:00Z')), 'night');     // 台北 04:59
  assert.equal(greetingKey(new Date('2026-09-20T03:59:00Z')), 'morning');   // 台北 11:59
  assert.equal(greetingKey(new Date('2026-09-20T09:59:00Z')), 'afternoon'); // 台北 17:59
  assert.equal(greetingKey(new Date('2026-09-20T13:59:00Z')), 'evening');   // 台北 21:59
});

test('問候語帶有文字與圖示', () => {
  const result = greeting(new Date('2026-09-20T02:00:00Z'));
  assert.equal(result.text, 'Good morning');
  assert.ok(result.icon.length > 0);
});

test('四個時段都有對應的問候語', () => {
  assert.deepEqual(Object.keys(GREETINGS).sort(), ['afternoon', 'evening', 'morning', 'night']);
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
// 天氣
// -----------------------------------------------------------------------------

test('城市清單就是規格要求的五個科技城市', () => {
  assert.deepEqual(CITY_IDS, ['taichung', 'taipei', 'hsinchu', 'tainan', 'kaohsiung']);
});

test('每個城市都有顯示名稱與座標', () => {
  for (const city of CITIES) {
    assert.equal(typeof city.label, 'string');
    assert.ok(city.label.length > 0);
    assert.equal(typeof city.latitude, 'number');
    assert.equal(typeof city.longitude, 'number');
  }
});

test('未知城市代號回退到清單第一個', () => {
  assert.equal(findCity('tokyo').id, 'taichung');
  assert.equal(findCity(undefined).id, 'taichung');
  assert.equal(findCity('tainan').id, 'tainan');
});

test('天氣網址帶上該城市的座標與台北時區', () => {
  const url = new URL(weatherApiUrl('kaohsiung'));
  assert.equal(url.origin, 'https://api.open-meteo.com');
  assert.equal(url.pathname, '/v1/forecast');
  assert.equal(url.searchParams.get('latitude'), '22.6273');
  assert.equal(url.searchParams.get('longitude'), '120.3014');
  assert.equal(url.searchParams.get('current'), 'temperature_2m,weather_code');
  assert.equal(url.searchParams.get('timezone'), 'Asia/Taipei');
});

test('天氣網址不含任何 API key', () => {
  const url = new URL(weatherApiUrl('taipei'));
  assert.equal(url.searchParams.get('apikey'), null);
  assert.equal(url.searchParams.get('key'), null);
});

test('主要天氣分組都有對應的圖示與描述', () => {
  assert.equal(describeWeatherCode(0).label, 'Clear sky');
  assert.equal(describeWeatherCode(2).label, 'Partly cloudy');
  assert.equal(describeWeatherCode(3).label, 'Overcast');
  assert.equal(describeWeatherCode(45).label, 'Fog');
  assert.equal(describeWeatherCode(53).label, 'Drizzle');
  assert.equal(describeWeatherCode(65).label, 'Rain');
  assert.equal(describeWeatherCode(73).label, 'Snow');
  assert.equal(describeWeatherCode(81).label, 'Rain showers');
  assert.equal(describeWeatherCode(86).label, 'Snow showers');
  assert.equal(describeWeatherCode(95).label, 'Thunderstorm');
});

test('未知或缺少的天氣代碼回退到中性圖示，不會爆掉', () => {
  for (const code of [7, 999, -1, undefined, null, 'rain']) {
    const result = describeWeatherCode(code);
    assert.equal(result.label, 'Unknown conditions');
    assert.ok(result.icon.length > 0);
  }
});

test('溫度四捨五入到整數並帶單位', () => {
  assert.equal(formatTemperature(26.4), '26°C');
  assert.equal(formatTemperature(26.5), '27°C');
  assert.equal(formatTemperature(-3.2), '-3°C');
  assert.equal(formatTemperature(0), '0°C');
});

test('完整的天氣回應會被接受', () => {
  const result = normalizeWeather(
    { current: { temperature_2m: 26.4, weather_code: 2 } },
    { cityId: 'taipei', observedAt: 1789917000000 }
  );
  assert.deepEqual(result, {
    cityId: 'taipei',
    temperature: 26.4,
    code: 2,
    observedAt: 1789917000000
  });
});

test('缺少欄位或型別不對的天氣回應視為不可用', () => {
  assert.equal(normalizeWeather(null, { cityId: 'taipei' }), null);
  assert.equal(normalizeWeather({}, { cityId: 'taipei' }), null);
  assert.equal(normalizeWeather({ current: {} }, { cityId: 'taipei' }), null);
  assert.equal(normalizeWeather({ current: { temperature_2m: '26', weather_code: 2 } }, { cityId: 'taipei' }), null);
  assert.equal(normalizeWeather({ current: { temperature_2m: 26, weather_code: null } }, { cityId: 'taipei' }), null);
  assert.equal(normalizeWeather({ current: { temperature_2m: NaN, weather_code: 2 } }, { cityId: 'taipei' }), null);
});

test('天氣回應裡的未知城市代號回退到預設城市', () => {
  const result = normalizeWeather({ current: { temperature_2m: 20, weather_code: 0 } }, { cityId: 'tokyo' });
  assert.equal(result.cityId, 'taichung');
});

test('天氣列文字含溫度、圖示與城市名稱', () => {
  const readout = formatWeatherReadout({ cityId: 'taichung', temperature: 26.4, code: 2, observedAt: 0 });
  assert.match(readout, /^26°C /);
  assert.match(readout, / · Taichung$/);
});

// -----------------------------------------------------------------------------
// 專案目錄資料
// -----------------------------------------------------------------------------

const FULL_PROJECT = {
  id: 'edge-vision',
  title: 'Edge AI Vision Inspection',
  category: 'Edge Computing',
  badge: 'Featured',
  description: 'Real-time defect inspection on an embedded board.',
  techStack: ['YOLOv8', 'TensorRT', 'Python'],
  githubUrl: 'https://github.com/example/edge-vision',
  demoUrl: 'https://example.com/demo'
};

test('完整的專案資料原樣保留', () => {
  assert.deepEqual(normalizeProject(FULL_PROJECT), {
    id: 'edge-vision',
    title: 'Edge AI Vision Inspection',
    category: 'Edge Computing',
    badge: 'Featured',
    description: 'Real-time defect inspection on an embedded board.',
    techStack: ['YOLOv8', 'TensorRT', 'Python'],
    githubUrl: 'https://github.com/example/edge-vision',
    demoUrl: 'https://example.com/demo'
  });
});

test('缺少 id、標題或描述的項目視為不合格', () => {
  assert.equal(normalizeProject({ ...FULL_PROJECT, id: '' }), null);
  assert.equal(normalizeProject({ ...FULL_PROJECT, title: '   ' }), null);
  assert.equal(normalizeProject({ ...FULL_PROJECT, description: undefined }), null);
});

test('非物件的項目視為不合格', () => {
  assert.equal(normalizeProject(null), null);
  assert.equal(normalizeProject('project'), null);
  assert.equal(normalizeProject([]), null);
});

test('缺少選填欄位時仍然合格，只是那些欄位是空的', () => {
  const result = normalizeProject({ id: 'a', title: 'A', description: 'B' });
  assert.equal(result.category, '');
  assert.equal(result.badge, '');
  assert.deepEqual(result.techStack, []);
  assert.equal(result.githubUrl, null);
  assert.equal(result.demoUrl, null);
});

test('techStack 型別錯誤時當成沒有標籤', () => {
  assert.deepEqual(normalizeProject({ ...FULL_PROJECT, techStack: 'Python' }).techStack, []);
  assert.deepEqual(normalizeProject({ ...FULL_PROJECT, techStack: null }).techStack, []);
});

test('techStack 內的空值被丟掉，數量上限被遵守', () => {
  const messy = { ...FULL_PROJECT, techStack: ['  A  ', '', null, 'B', 'C', 'D', 'E', 'F', 'G'] };
  const tags = normalizeProject(messy).techStack;
  assert.equal(tags[0], 'A');
  assert.ok(tags.length <= MAX_TECH_TAGS, `got ${tags.length} tags`);
  assert.ok(!tags.includes(''));
});

test('只有 http 與 https 的網址會被接受', () => {
  assert.equal(safeUrl('https://example.com/a'), 'https://example.com/a');
  assert.equal(safeUrl('http://example.com/a'), 'http://example.com/a');
  assert.equal(safeUrl('javascript:alert(1)'), null);
  assert.equal(safeUrl('data:text/html,<script>'), null);
  assert.equal(safeUrl('#'), null);
  assert.equal(safeUrl(''), null);
  assert.equal(safeUrl(42), null);
});

test('危險的連結不會變成卡片上的連結', () => {
  const result = normalizeProject({ ...FULL_PROJECT, githubUrl: 'javascript:alert(1)', demoUrl: '#' });
  assert.equal(result.githubUrl, null);
  assert.equal(result.demoUrl, null);
});

test('整份目錄中結構不符的項目被丟掉，其餘照常保留', () => {
  const list = [FULL_PROJECT, { title: 'no id' }, null, { ...FULL_PROJECT, id: 'second' }];
  const result = normalizeProjects(list);
  assert.equal(result.length, 2);
  assert.deepEqual(result.map((p) => p.id), ['edge-vision', 'second']);
});

test('空陣列與非陣列都回傳空清單', () => {
  assert.deepEqual(normalizeProjects([]), []);
  assert.deepEqual(normalizeProjects(null), []);
  assert.deepEqual(normalizeProjects({ projects: [] }), []);
});

// -----------------------------------------------------------------------------
// 滴答聲的合成參數
// -----------------------------------------------------------------------------

test('滴答聲從高頻滑到低頻，聽起來才像機械撞擊而不是嗶聲', () => {
  assert.ok(TICK_SOUND.startFrequency > TICK_SOUND.endFrequency);
});

test('滴答聲的頻率落在人耳聽得到的範圍', () => {
  assert.ok(TICK_SOUND.endFrequency >= 20, '低頻不能低於聽覺下限');
  assert.ok(TICK_SOUND.startFrequency <= 20000, '高頻不能超過聽覺上限');
});

test('滴答聲極短，不會蓋過下一秒', () => {
  assert.ok(TICK_SOUND.durationSeconds > 0);
  assert.ok(TICK_SOUND.durationSeconds < 0.2, '單次滴答必須遠短於一秒');
});

test('音量溫和且衰減到接近零', () => {
  assert.ok(TICK_SOUND.peakGain > 0 && TICK_SOUND.peakGain <= 0.2, '避免刺耳的音量');
  assert.ok(TICK_SOUND.endGain > 0, 'exponentialRamp 的目標值不能是 0');
  assert.ok(TICK_SOUND.endGain < TICK_SOUND.peakGain);
});

// -----------------------------------------------------------------------------
// 鍵盤快捷鍵
// -----------------------------------------------------------------------------

test('Z、T、C 各自對應一個動作，大小寫都算', () => {
  assert.equal(shortcutAction({ key: 'z' }), 'toggle-zen');
  assert.equal(shortcutAction({ key: 'Z' }), 'toggle-zen');
  assert.equal(shortcutAction({ key: 't' }), 'toggle-format');
  assert.equal(shortcutAction({ key: 'T' }), 'toggle-format');
  assert.equal(shortcutAction({ key: 'c' }), 'copy-time');
  assert.equal(shortcutAction({ key: 'C' }), 'copy-time');
});

test('沒有對應動作的按鍵回傳 null', () => {
  assert.equal(shortcutAction({ key: 'a' }), null);
  assert.equal(shortcutAction({ key: 'Enter' }), null);
  assert.equal(shortcutAction({ key: '1' }), null);
  assert.equal(shortcutAction({}), null);
});

test('按著 Ctrl、Cmd 或 Alt 時完全不攔截', () => {
  assert.equal(shortcutAction({ key: 'c', ctrlKey: true }), null);
  assert.equal(shortcutAction({ key: 'c', metaKey: true }), null);
  assert.equal(shortcutAction({ key: 't', altKey: true }), null);
  assert.equal(shortcutAction({ key: 'Escape', ctrlKey: true }), null);
});

test('焦點在輸入框或選單上時不攔截字母鍵', () => {
  assert.equal(shortcutAction({ key: 'z', fromFormField: true }), null);
  assert.equal(shortcutAction({ key: 'c', fromFormField: true }), null);
});

test('正在編輯名稱或標語時不攔截任何鍵', () => {
  assert.equal(shortcutAction({ key: 'z', editing: true }), null);
  assert.equal(shortcutAction({ key: 'Escape', editing: true, zenMode: true }), null);
});

test('Escape 在抽屜開啟時先關抽屜', () => {
  assert.equal(shortcutAction({ key: 'Escape', drawerOpen: true, zenMode: true }), 'close-drawer');
});

test('Escape 在抽屜未開時才離開 Zen 模式', () => {
  assert.equal(shortcutAction({ key: 'Escape', drawerOpen: false, zenMode: true }), 'exit-zen');
});

test('Escape 在沒有抽屜也沒有 Zen 時什麼都不做', () => {
  assert.equal(shortcutAction({ key: 'Escape' }), null);
});

test('Z 在 Zen 模式開啟時仍回傳切換動作，用來離開', () => {
  assert.equal(shortcutAction({ key: 'z', zenMode: true }), 'toggle-zen');
});

// -----------------------------------------------------------------------------
// 名稱呈現
// -----------------------------------------------------------------------------

test('有空白的名字從第一個空白切開', () => {
  assert.deepEqual(splitDisplayName('Ada Lovelace'), { lead: 'Ada', trail: 'Lovelace' });
});

test('多個詞的名字只切第一個空白，其餘留在第二行', () => {
  assert.deepEqual(splitDisplayName('Huan Chen Lee'), { lead: 'Huan', trail: 'Chen Lee' });
});

test('單一個詞的名字對半切', () => {
  assert.deepEqual(splitDisplayName('Momo'), { lead: 'Mo', trail: 'mo' });
  assert.deepEqual(splitDisplayName('Ada'), { lead: 'Ad', trail: 'a' });
});

test('只有一個字元時第二行留空', () => {
  assert.deepEqual(splitDisplayName('M'), { lead: 'M', trail: '' });
});

test('拆字前會先清理，空值回退到預設名稱', () => {
  assert.deepEqual(splitDisplayName('  Ada   Lovelace  '), { lead: 'Ada', trail: 'Lovelace' });
  assert.deepEqual(splitDisplayName('   '), splitDisplayName(DEFAULT_STATE.name));
  assert.deepEqual(splitDisplayName(null), splitDisplayName(DEFAULT_STATE.name));
});

test('兩個詞以上的縮寫取前兩個詞的首字母', () => {
  assert.equal(initialsFrom('Huan Chen'), 'HC');
  assert.equal(initialsFrom('ada lovelace king'), 'AL');
});

test('單一個詞的縮寫取前兩個字元', () => {
  assert.equal(initialsFrom('Momo'), 'MO');
  assert.equal(initialsFrom('M'), 'M');
});

test('縮寫一律大寫，空值回退到預設名稱的縮寫', () => {
  assert.equal(initialsFrom('ada'), 'AD');
  assert.equal(initialsFrom(''), initialsFrom(DEFAULT_STATE.name));
  assert.equal(initialsFrom(undefined), initialsFrom(DEFAULT_STATE.name));
});

// -----------------------------------------------------------------------------
// 抽屜分頁
// -----------------------------------------------------------------------------

test('抽屜有 Projects、About、Connect 三個分頁', () => {
  assert.deepEqual(DRAWER_TABS, ['projects', 'about', 'connect']);
});

test('只有清單內的值算是合法分頁', () => {
  assert.equal(isDrawerTab('about'), true);
  assert.equal(isDrawerTab('About'), false);
  assert.equal(isDrawerTab('settings'), false);
});

test('右方向鍵往後切，走到最後一個會繞回第一個', () => {
  assert.equal(nextTabIndex(0, 'ArrowRight'), 1);
  assert.equal(nextTabIndex(1, 'ArrowRight'), 2);
  assert.equal(nextTabIndex(2, 'ArrowRight'), 0);
});

test('左方向鍵往前切，走到第一個會繞回最後一個', () => {
  assert.equal(nextTabIndex(2, 'ArrowLeft'), 1);
  assert.equal(nextTabIndex(1, 'ArrowLeft'), 0);
  assert.equal(nextTabIndex(0, 'ArrowLeft'), 2);
});

test('上下方向鍵與左右方向鍵作用相同', () => {
  assert.equal(nextTabIndex(0, 'ArrowDown'), 1);
  assert.equal(nextTabIndex(0, 'ArrowUp'), 2);
});

test('Home 與 End 跳到頭尾', () => {
  assert.equal(nextTabIndex(1, 'Home'), 0);
  assert.equal(nextTabIndex(1, 'End'), 2);
});

test('其他按鍵維持原本的分頁', () => {
  assert.equal(nextTabIndex(1, 'Enter'), 1);
  assert.equal(nextTabIndex(1, 'a'), 1);
  assert.equal(nextTabIndex(1, 'Escape'), 1);
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
