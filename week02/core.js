/**
 * core.js — DIC-1 的純邏輯模組。
 *
 * 教學重點：這個模組不碰 DOM、localStorage、fetch 或 AudioContext，
 * 也不自己取得「現在時間」——需要時間的函式一律由呼叫端把 Date 傳進來。
 * 沒有副作用的程式碼可以在瀏覽器與 Node 兩邊執行，測試才跑得起來。
 * 所有會碰到外界的動作都留在 app.js。
 */

/** 可循環切換的視覺主題代號，順序即為切換順序。 */
export const THEMES = ['aurora', 'minimal', 'sunset'];

/** 主題代號對應的顯示名稱。 */
export const THEME_LABELS = { aurora: 'Aurora', minimal: 'Minimal', sunset: 'Sunset' };

/** 主題代號對應的瀏覽器工具列顏色（<meta name="theme-color">）。 */
export const THEME_COLORS = { aurora: '#07120f', minimal: '#f7f7f5', sunset: '#f0eee6' };

/** 找不到已保存偏好時使用的預設值。 */
export const DEFAULT_PREFERENCES = { theme: 'sunset', format24: true };

/** 顯示名稱，同時用於複製出來的時間戳記文字。 */
export const DISPLAY_NAME = 'Momo';

/** 時間一律以台北時區計算，不跟隨訪客裝置的時區。 */
export const TIME_ZONE = 'Asia/Taipei';

/** 這個值是不是合法的主題代號。 */
export function isTheme(value) {
  return THEMES.includes(value);
}

/** 取得循環切換的下一個主題。 */
export function nextTheme(theme) {
  const index = THEMES.indexOf(theme);
  return THEMES[(index + 1) % THEMES.length];
}

/**
 * 把來源不可信的偏好物件整理成可安全使用的形狀。
 * 缺少的欄位、型別錯誤的欄位與未知的主題值一律回退到預設；多餘的欄位丟棄。
 */
export function normalizePreferences(raw) {
  const preferences = { ...DEFAULT_PREFERENCES };
  if (raw && typeof raw === 'object') {
    if (isTheme(raw.theme)) preferences.theme = raw.theme;
    if (typeof raw.format24 === 'boolean') preferences.format24 = raw.format24;
  }
  return preferences;
}

/**
 * 取出某個時刻在台北時區的時、分、秒與上下午標記。
 * 12 小時制才會有 dayPeriod。
 */
export function taipeiTimeParts(date, { format24 = true } = {}) {
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: TIME_ZONE,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: !format24,
    hourCycle: format24 ? 'h23' : undefined
  });
  return Object.fromEntries(
    formatter.formatToParts(date)
      .filter(({ type }) => ['hour', 'minute', 'second', 'dayPeriod'].includes(type))
      .map(({ type, value }) => [type, value])
  );
}

/** 台北時區的完整日期與星期，例如「2026年9月20日 星期日」。 */
export function formatTaipeiDate(date) {
  const day = new Intl.DateTimeFormat('zh-TW', {
    timeZone: TIME_ZONE,
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
  const weekday = new Intl.DateTimeFormat('zh-TW', {
    timeZone: TIME_ZONE,
    weekday: 'long'
  }).format(date);
  return `${day} ${weekday}`;
}

/** 時鐘上顯示的 HH:MM:SS 文字。 */
export function formatClockText(date, { format24 = true } = {}) {
  const parts = taipeiTimeParts(date, { format24 });
  return `${parts.hour}:${parts.minute}:${parts.second}`;
}

/** 複製按鈕產生的文字：名稱、日期、時間與時區身分。 */
export function buildTimestampText(date, { format24 = true, name = DISPLAY_NAME } = {}) {
  const parts = taipeiTimeParts(date, { format24 });
  const time = `${parts.hour}:${parts.minute}:${parts.second}${format24 ? '' : ` ${parts.dayPeriod}`}`;
  return `${name}｜${formatTaipeiDate(date)} ${time}｜Asia/Taipei (UTC+8)`;
}
