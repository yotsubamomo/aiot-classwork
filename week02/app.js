/**
 * app.js — 把 core.js 的純邏輯接到真實世界。
 *
 * 這一層負責所有副作用：DOM 查詢與事件、localStorage 讀寫、剪貼簿、計時器。
 * 需要判斷或計算的部分一律呼叫 core.js，不在這裡重複實作。
 */

import {
  DISPLAY_NAME,
  THEME_COLORS,
  THEME_LABELS,
  buildTimestampText,
  formatClockText,
  formatTaipeiDate,
  nextTheme,
  normalizePreferences,
  taipeiTimeParts
} from './core.js';

/** localStorage 的鍵名。 */
const STORAGE_KEY = 'momo-preferences';

// =============================================================================
// DOM 選取：一次把需要的節點查好放進物件，避免每次事件都重新查詢。
// =============================================================================
const elements = {
  clock: document.querySelector('#clock'),
  meridiem: document.querySelector('#meridiem'),
  date: document.querySelector('#date'),
  themeButton: document.querySelector('#theme-button'),
  themeLabel: document.querySelector('#theme-label'),
  format24: document.querySelector('#format-24'),
  format12: document.querySelector('#format-12'),
  copyButton: document.querySelector('#copy-button'),
  focusButton: document.querySelector('#focus-button'),
  focusExit: document.querySelector('#focus-exit'),
  toast: document.querySelector('#toast'),
  toastMessage: document.querySelector('#toast-message'),
  themeColor: document.querySelector('meta[name="theme-color"]')
};

const state = {
  theme: document.documentElement.dataset.theme,
  format24: true,
  focusMode: false
};

let toastTimer;

// =============================================================================
// localStorage：序列化與狀態還原。
// 儲存空間可能被封鎖或內容被竄改，所以讀寫都包在 try／catch 裡，
// 失敗時網站仍然完全可用，只是偏好不會被保存。
// =============================================================================
function loadPreferences() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    const preferences = normalizePreferences(saved);
    state.theme = preferences.theme;
    state.format24 = preferences.format24;
  } catch (_) {
    // Storage is optional; keep defaults when it is unavailable or invalid.
  }
}

function savePreferences() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ theme: state.theme, format24: state.format24 }));
  } catch (_) {
    // The page remains fully usable when storage is unavailable.
  }
}

function setTheme(theme, persist = true) {
  state.theme = theme;
  document.documentElement.dataset.theme = theme;
  elements.themeLabel.textContent = `主題 · ${THEME_LABELS[theme]}`;
  elements.themeButton.setAttribute('aria-label', `目前主題為 ${THEME_LABELS[theme]}，切換到下一個主題`);
  elements.themeColor.content = THEME_COLORS[theme];
  if (persist) savePreferences();
}

function cycleTheme() {
  setTheme(nextTheme(state.theme));
}

function setTimeFormat(format24, persist = true) {
  state.format24 = format24;
  elements.format24.setAttribute('aria-pressed', String(format24));
  elements.format12.setAttribute('aria-pressed', String(!format24));
  if (persist) savePreferences();
  updateClock();
}

// =============================================================================
// 時鐘：每秒把 core.js 算出來的文字寫回畫面。
// =============================================================================
function updateClock() {
  const now = new Date();
  elements.clock.dateTime = now.toISOString();
  elements.clock.textContent = formatClockText(now, { format24: state.format24 });
  elements.date.textContent = formatTaipeiDate(now);
  elements.meridiem.hidden = state.format24;
  elements.meridiem.textContent = state.format24
    ? ''
    : taipeiTimeParts(now, { format24: false }).dayPeriod;
}

function showToast(message) {
  clearTimeout(toastTimer);
  elements.toastMessage.textContent = message;
  elements.toast.classList.add('visible');
  toastTimer = setTimeout(() => elements.toast.classList.remove('visible'), 3000);
}

async function copyTime() {
  const text = buildTimestampText(new Date(), { format24: state.format24, name: DISPLAY_NAME });
  try {
    await navigator.clipboard.writeText(text);
  } catch (_) {
    // 較舊的瀏覽器或非安全來源沒有 Clipboard API，改用暫時的 textarea 複製。
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.setAttribute('readonly', '');
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    textArea.remove();
  }
  showToast('已複製台北時間');
}

function setFocusMode(enabled) {
  state.focusMode = enabled;
  document.body.classList.toggle('focus-mode', enabled);
  elements.focusButton.setAttribute('aria-pressed', String(enabled));
  if (enabled) elements.focusExit.focus();
  else elements.focusButton.focus();
}

// =============================================================================
// 事件處理：所有使用者互動的進入點。
// =============================================================================
elements.themeButton.addEventListener('click', cycleTheme);
elements.format24.addEventListener('click', () => setTimeFormat(true));
elements.format12.addEventListener('click', () => setTimeFormat(false));
elements.copyButton.addEventListener('click', copyTime);
elements.focusButton.addEventListener('click', () => setFocusMode(true));
elements.focusExit.addEventListener('click', () => setFocusMode(false));
window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && state.focusMode) setFocusMode(false);
});

// =============================================================================
// 啟動：先還原偏好，再把畫面同步到還原後的狀態。
// =============================================================================
loadPreferences();
setTheme(state.theme, false);
setTimeFormat(state.format24, false);
updateClock();
setInterval(updateClock, 1000);
