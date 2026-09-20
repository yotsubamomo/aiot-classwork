/**
 * app.js — 把 core.js 的純邏輯接到真實世界。
 *
 * 這一層負責所有副作用：DOM 查詢與事件、localStorage 讀寫、剪貼簿、計時器。
 * 需要判斷或計算的部分一律呼叫 core.js，不在這裡重複實作。
 */

import {
  LEGACY_STORAGE_KEY,
  STORAGE_KEY,
  THEME_COLORS,
  THEME_LABELS,
  buildTimestampText,
  formatClockText,
  formatTaipeiDate,
  nextTheme,
  normalizeState,
  stateFromLegacyPreferences,
  taipeiTimeParts
} from './core.js';

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

/**
 * 單一狀態樹：所有使用者偏好都在這個物件裡，也只有這個物件會被保存。
 * 先以預設值開場，載入完成後由 hydrateState() 覆寫。
 */
let state = normalizeState(null);

let toastTimer;

// =============================================================================
// localStorage：序列化與狀態還原。
//
// 儲存空間可能被封鎖（無痕視窗、瀏覽器設定），內容也可能是舊格式或被手動改過，
// 所以讀寫都包在 try／catch 裡，而且讀進來的東西一律先經過 normalizeState()。
// 存取失敗時網站完全照常運作，只是偏好不會被保存。
// =============================================================================
function readStoredState() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored !== null) return normalizeState(JSON.parse(stored));

    // 沒有新鍵時，把拆檔前留下的舊偏好搬過來，之後就只讀新鍵。
    const legacy = localStorage.getItem(LEGACY_STORAGE_KEY);
    if (legacy !== null) {
      const migrated = stateFromLegacyPreferences(JSON.parse(legacy));
      localStorage.setItem(STORAGE_KEY, JSON.stringify(migrated));
      localStorage.removeItem(LEGACY_STORAGE_KEY);
      return migrated;
    }
  } catch (_) {
    // 儲存不可用或內容無法解析時，直接使用預設狀態。
  }
  return normalizeState(null);
}

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (_) {
    // The page remains fully usable when storage is unavailable.
  }
}

/** 更新狀態樹的部分欄位並保存。所有偏好變更都走這個入口。 */
function updateState(changes) {
  state = normalizeState({ ...state, ...changes });
  saveState();
}

function setTheme(theme, { persist = true } = {}) {
  if (persist) updateState({ theme });
  else state = normalizeState({ ...state, theme });

  document.documentElement.dataset.theme = state.theme;
  elements.themeLabel.textContent = `主題 · ${THEME_LABELS[state.theme]}`;
  elements.themeButton.setAttribute('aria-label', `目前主題為 ${THEME_LABELS[state.theme]}，切換到下一個主題`);
  elements.themeColor.content = THEME_COLORS[state.theme];
}

function cycleTheme() {
  setTheme(nextTheme(state.theme));
}

function setTimeFormat(format24h, { persist = true } = {}) {
  if (persist) updateState({ format24h });
  else state = normalizeState({ ...state, format24h });

  elements.format24.setAttribute('aria-pressed', String(state.format24h));
  elements.format12.setAttribute('aria-pressed', String(!state.format24h));
  updateClock();
}

// =============================================================================
// 時鐘：每秒把 core.js 算出來的文字寫回畫面。
// =============================================================================
function updateClock() {
  const now = new Date();
  elements.clock.dateTime = now.toISOString();
  elements.clock.textContent = formatClockText(now, { format24h: state.format24h });
  elements.date.textContent = formatTaipeiDate(now);
  elements.meridiem.hidden = state.format24h;
  elements.meridiem.textContent = state.format24h
    ? ''
    : taipeiTimeParts(now, { format24h: false }).dayPeriod;
}

function showToast(message) {
  clearTimeout(toastTimer);
  elements.toastMessage.textContent = message;
  elements.toast.classList.add('visible');
  toastTimer = setTimeout(() => elements.toast.classList.remove('visible'), 3000);
}

async function copyTime() {
  const text = buildTimestampText(new Date(), { format24h: state.format24h, name: state.name });
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

/**
 * 專注模式（之後會擴充成規格的 Zen 模式）。
 * moveFocus 在啟動還原時關閉，避免頁面一載入就把焦點搶走。
 */
function setZenMode(enabled, { persist = true, moveFocus = true } = {}) {
  if (persist) updateState({ zenMode: enabled });
  else state = normalizeState({ ...state, zenMode: enabled });

  document.body.classList.toggle('focus-mode', state.zenMode);
  elements.focusButton.setAttribute('aria-pressed', String(state.zenMode));
  if (!moveFocus) return;
  if (state.zenMode) elements.focusExit.focus();
  else elements.focusButton.focus();
}

// =============================================================================
// 事件處理：所有使用者互動的進入點。
// =============================================================================
elements.themeButton.addEventListener('click', cycleTheme);
elements.format24.addEventListener('click', () => setTimeFormat(true));
elements.format12.addEventListener('click', () => setTimeFormat(false));
elements.copyButton.addEventListener('click', copyTime);
elements.focusButton.addEventListener('click', () => setZenMode(true));
elements.focusExit.addEventListener('click', () => setZenMode(false));
window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && state.zenMode) setZenMode(false);
});

// =============================================================================
// 啟動：先還原狀態樹，再把畫面同步到還原後的狀態。
// 這裡的 persist 全部關閉——啟動只是把畫面對齊既有狀態，不是使用者的新選擇。
// =============================================================================
state = readStoredState();
setTheme(state.theme, { persist: false });
setTimeFormat(state.format24h, { persist: false });
setZenMode(state.zenMode, { persist: false, moveFocus: false });
updateClock();
setInterval(updateClock, 1000);
