/**
 * core.js — DIC-1 的純邏輯模組。
 *
 * 教學重點：這個模組不碰 DOM、localStorage、fetch 或 AudioContext，
 * 也不自己取得「現在時間」——需要時間的函式一律由呼叫端把 Date 傳進來。
 * 沒有副作用的程式碼可以在瀏覽器與 Node 兩邊執行，測試才跑得起來。
 * 所有會碰到外界的動作都留在 app.js。
 */

/** 單一狀態樹在 localStorage 的鍵名。 */
export const STORAGE_KEY = 'aiot_user_state';

/** 拆檔前使用的舊鍵名，只在一次性搬移時讀取。 */
export const LEGACY_STORAGE_KEY = 'momo-preferences';

/** 可循環切換的視覺主題代號，順序即為切換順序。 */
export const THEMES = ['aurora', 'minimal', 'sunset'];

/** 主題代號對應的顯示名稱。 */
export const THEME_LABELS = { aurora: 'Aurora', minimal: 'Minimal', sunset: 'Sunset' };

/** 主題代號對應的瀏覽器工具列顏色（<meta name="theme-color">）。 */
export const THEME_COLORS = { aurora: '#07120f', minimal: '#f7f7f5', sunset: '#f0eee6' };

/** 天氣可選的城市代號。座標等細節在天氣功能落地時補上。 */
export const CITIES = ['taichung', 'taipei', 'hsinchu', 'tainan', 'kaohsiung'];

/** 名稱與標語的長度上限，避免單一欄位撐破版面。 */
export const NAME_MAX_LENGTH = 40;
export const TAGLINE_MAX_LENGTH = 80;

/** 時間一律以台北時區計算，不跟隨訪客裝置的時區。 */
export const TIME_ZONE = 'Asia/Taipei';

/**
 * 所有使用者偏好的單一狀態樹。
 * 這七個欄位就是會被保存的全部內容，不多也不少。
 */
export const DEFAULT_STATE = Object.freeze({
  name: 'Momo',
  tagline: 'AIoT & Data Analytics',
  theme: 'aurora',
  format24h: true,
  soundEnabled: false,
  selectedCity: 'taichung',
  zenMode: false
});

/** 這個值是不是合法的主題代號。 */
export function isTheme(value) {
  return THEMES.includes(value);
}

/** 這個值是不是合法的城市代號。 */
export function isCity(value) {
  return CITIES.includes(value);
}

/** 取得循環切換的下一個主題。 */
export function nextTheme(theme) {
  const index = THEMES.indexOf(theme);
  return THEMES[(index + 1) % THEMES.length];
}

/**
 * 把使用者輸入或儲存內容整理成單行文字。
 * 換行與連續空白收斂成單一空格，前後空白去除，超長截斷；
 * 空字串或非字串回退到 fallback。
 */
export function sanitizeLine(value, { maxLength = NAME_MAX_LENGTH, fallback = '' } = {}) {
  if (typeof value !== 'string') return fallback;
  const cleaned = value.replace(/\s+/g, ' ').trim();
  if (!cleaned) return fallback;
  return cleaned.slice(0, maxLength);
}

/**
 * 把來源不可信的物件整理成完整且可安全使用的狀態樹。
 *
 * 儲存內容可能是舊版格式、被手動竄改，或根本不是物件，
 * 所以每個欄位都各自驗證：型別錯誤、超出允許值或缺少的欄位一律回退到預設，
 * 未知欄位直接丟棄。回傳值永遠是完整的七個欄位。
 */
export function normalizeState(raw) {
  const state = { ...DEFAULT_STATE };
  if (raw && typeof raw === 'object' && !Array.isArray(raw)) {
    state.name = sanitizeLine(raw.name, { maxLength: NAME_MAX_LENGTH, fallback: DEFAULT_STATE.name });
    state.tagline = sanitizeLine(raw.tagline, { maxLength: TAGLINE_MAX_LENGTH, fallback: DEFAULT_STATE.tagline });
    if (isTheme(raw.theme)) state.theme = raw.theme;
    if (typeof raw.format24h === 'boolean') state.format24h = raw.format24h;
    if (typeof raw.soundEnabled === 'boolean') state.soundEnabled = raw.soundEnabled;
    if (isCity(raw.selectedCity)) state.selectedCity = raw.selectedCity;
    if (typeof raw.zenMode === 'boolean') state.zenMode = raw.zenMode;
  }
  return state;
}

/** 從拆檔前的舊偏好格式建出狀態樹，其餘欄位使用預設值。 */
export function stateFromLegacyPreferences(legacy) {
  const state = { ...DEFAULT_STATE };
  if (legacy && typeof legacy === 'object' && !Array.isArray(legacy)) {
    if (isTheme(legacy.theme)) state.theme = legacy.theme;
    if (typeof legacy.format24 === 'boolean') state.format24h = legacy.format24;
  }
  return state;
}

/**
 * 取出某個時刻在台北時區的時、分、秒與上下午標記。
 * 12 小時制才會有 dayPeriod。
 */
export function taipeiTimeParts(date, { format24h = true } = {}) {
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: TIME_ZONE,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: !format24h,
    hourCycle: format24h ? 'h23' : undefined
  });
  return Object.fromEntries(
    formatter.formatToParts(date)
      .filter(({ type }) => ['hour', 'minute', 'second', 'dayPeriod'].includes(type))
      .map(({ type, value }) => [type, value])
  );
}

/** 台北時區的完整日期，例如「Sunday, September 20, 2026」。 */
export function formatTaipeiDate(date) {
  return new Intl.DateTimeFormat('en-US', {
    timeZone: TIME_ZONE,
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
}

/**
 * 這一分鐘已經走了多少比例（0 到 1，不含 1）。
 *
 * 直接用 epoch 毫秒取餘數，而不是讀時、分、秒：秒與毫秒在整點偏移的時區裡
 * 都是一樣的，台北是 UTC+8 整點偏移，所以分鐘邊界完全對齊。
 * 帶上毫秒才能讓進度環連續移動，而不是每秒跳一格。
 */
export function minuteProgress(date) {
  const withinMinute = ((date.getTime() % 60000) + 60000) % 60000;
  return withinMinute / 60000;
}

/** 進度環的 stroke-dashoffset：進度 0 時整圈留白，進度 1 時畫滿。 */
export function ringDashOffset(progress, circumference) {
  const clamped = Math.min(Math.max(progress, 0), 1);
  return circumference * (1 - clamped);
}

/** 補零到三位的毫秒文字。 */
export function formatMilliseconds(date) {
  const ms = ((date.getTime() % 1000) + 1000) % 1000;
  return String(ms).padStart(3, '0');
}

/** UNIX timestamp（秒）。 */
export function unixSeconds(date) {
  return Math.floor(date.getTime() / 1000);
}

/** 時鐘上顯示的 HH:MM:SS 文字。 */
export function formatClockText(date, { format24h = true } = {}) {
  const parts = taipeiTimeParts(date, { format24h });
  return `${parts.hour}:${parts.minute}:${parts.second}`;
}

/** 複製按鈕產生的文字：名稱、日期、時間與時區身分。 */
export function buildTimestampText(date, { format24h = true, name = DEFAULT_STATE.name } = {}) {
  const parts = taipeiTimeParts(date, { format24h });
  const time = `${parts.hour}:${parts.minute}:${parts.second}${format24h ? '' : ` ${parts.dayPeriod}`}`;
  return `${name} · ${formatTaipeiDate(date)} · ${time} · Asia/Taipei (UTC+8)`;
}
