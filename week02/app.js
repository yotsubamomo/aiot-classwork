/**
 * app.js — 把 core.js 的純邏輯接到真實世界。
 *
 * 這一層負責所有副作用：DOM 查詢與事件、localStorage 讀寫、剪貼簿、計時器。
 * 需要判斷或計算的部分一律呼叫 core.js，不在這裡重複實作。
 */

import {
  DRAWER_TABS,
  LEGACY_STORAGE_KEY,
  STORAGE_KEY,
  THEME_COLORS,
  THEME_LABELS,
  buildTimestampText,
  dayOfYear,
  formatClockText,
  formatMilliseconds,
  formatTaipeiDate,
  greeting,
  isDrawerTab,
  isoWeek,
  minuteProgress,
  nextTheme,
  nextTabIndex,
  normalizeState,
  ringDashOffset,
  stateFromLegacyPreferences,
  taipeiTimeParts,
  unixSeconds
} from './core.js';

// =============================================================================
// DOM 選取：一次把需要的節點查好放進物件，避免每次事件都重新查詢。
// =============================================================================
const elements = {
  clock: document.querySelector('#clock'),
  meridiem: document.querySelector('#meridiem'),
  milliseconds: document.querySelector('#milliseconds'),
  epoch: document.querySelector('#epoch'),
  secondRing: document.querySelector('#second-ring'),
  date: document.querySelector('#date'),
  weekBadge: document.querySelector('#week-badge'),
  dayBadge: document.querySelector('#day-badge'),
  greetingIcon: document.querySelector('#greeting-icon'),
  greetingText: document.querySelector('#greeting-text'),
  themeButton: document.querySelector('#theme-button'),
  themeLabel: document.querySelector('#theme-label'),
  format24: document.querySelector('#format-24'),
  format12: document.querySelector('#format-12'),
  copyButton: document.querySelector('#copy-button'),
  focusButton: document.querySelector('#focus-button'),
  focusExit: document.querySelector('#focus-exit'),
  drawer: document.querySelector('#drawer'),
  drawerOverlay: document.querySelector('#drawer-overlay'),
  drawerClose: document.querySelector('#drawer-close'),
  drawerTabs: document.querySelector('.drawer-tabs'),
  portalButtons: document.querySelectorAll('.portal-button'),
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
  elements.themeLabel.textContent = `Theme · ${THEME_LABELS[state.theme]}`;
  elements.themeButton.setAttribute('aria-label', `Current theme is ${THEME_LABELS[state.theme]}. Switch to the next theme.`);
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
// 時鐘：以 requestAnimationFrame 連續更新。
//
// 每一幀只改寫毫秒與進度環——這兩個本來就每一幀都不一樣；
// 時、分、秒與日期只在跨秒時才寫回 DOM，避免每秒做六十次沒有意義的重繪。
// 進度環的 SVG 半徑是 45（viewBox 100），整圈長度就是 2πr。
// =============================================================================
const RING_CIRCUMFERENCE = 2 * Math.PI * 45;

let lastRenderedSecond = null;

function renderClock(now) {
  elements.milliseconds.textContent = formatMilliseconds(now);
  elements.secondRing.style.strokeDashoffset =
    ringDashOffset(minuteProgress(now), RING_CIRCUMFERENCE).toFixed(2);

  const second = unixSeconds(now);
  if (second === lastRenderedSecond) return;
  lastRenderedSecond = second;

  elements.clock.dateTime = now.toISOString();
  elements.clock.textContent = formatClockText(now, { format24h: state.format24h });
  elements.epoch.textContent = String(second);
  elements.date.textContent = formatTaipeiDate(now);
  elements.weekBadge.textContent = `Week ${isoWeek(now).week}`;
  elements.dayBadge.textContent = `Day ${dayOfYear(now)}`;

  const { text, icon } = greeting(now);
  elements.greetingIcon.textContent = icon;
  elements.greetingText.textContent = text;
  elements.meridiem.hidden = state.format24h;
  elements.meridiem.textContent = state.format24h
    ? ''
    : taipeiTimeParts(now, { format24h: false }).dayPeriod;
}

/** 立刻重畫一次，用在偏好變更後不等下一秒就要看到結果的情況。 */
function updateClock() {
  lastRenderedSecond = null;
  renderClock(new Date());
}

function startClock() {
  // 先同步畫一次，不必等第一幀，載入時就不會看到 --:--:-- 的預設值。
  updateClock();

  const frame = () => {
    renderClock(new Date());
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);

  // 分頁切走時瀏覽器會暫停 requestAnimationFrame，回來時立刻補畫一次，
  // 避免先看到凍結在離開前的舊時間。
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) updateClock();
  });
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
  showToast('Taipei time copied');
}

// =============================================================================
// 抽屜：Hero 保持乾淨，次要內容收在滑出面板裡。
//
// 無障礙重點：開啟時焦點移入面板並把 Tab 鎖在裡面，關閉後焦點回到原本的觸發按鈕；
// 關閉狀態用 inert，整塊內容會退出 Tab 順序與無障礙樹，不只是視覺上移開。
// =============================================================================
const FOCUSABLE = 'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';

let activeTab = DRAWER_TABS[0];
let drawerOpen = false;
let drawerTrigger = null;

function tabButton(name) {
  return elements.drawer.querySelector(`.drawer-tab[data-tab="${name}"]`);
}

function switchDrawerTab(name, { focusTab = false } = {}) {
  if (!isDrawerTab(name)) return;
  activeTab = name;

  for (const tab of DRAWER_TABS) {
    const button = tabButton(tab);
    const panel = document.querySelector(`#panel-${tab}`);
    const selected = tab === name;
    button.setAttribute('aria-selected', String(selected));
    button.tabIndex = selected ? 0 : -1;
    panel.hidden = !selected;
  }

  if (focusTab) tabButton(name).focus();
}

function openDrawer(name, trigger) {
  drawerTrigger = trigger ?? null;
  drawerOpen = true;
  switchDrawerTab(name);
  elements.drawer.removeAttribute('inert');
  document.body.classList.add('drawer-open');
  tabButton(activeTab).focus();
}

function closeDrawer() {
  if (!drawerOpen) return;
  drawerOpen = false;
  document.body.classList.remove('drawer-open');
  // 先把焦點移出去再設 inert，否則焦點會停在一個已經被移出無障礙樹的元素上。
  if (drawerTrigger) drawerTrigger.focus();
  else elements.drawer.blur();
  elements.drawer.setAttribute('inert', '');
  drawerTrigger = null;
}

/** 把 Tab 鎖在抽屜內，避免焦點跑到後面被遮住的頁面上。 */
function trapFocus(event) {
  if (event.key !== 'Tab' || !drawerOpen) return;
  const focusable = [...elements.drawer.querySelectorAll(FOCUSABLE)]
    .filter((node) => node.offsetParent !== null || node === document.activeElement);
  if (focusable.length === 0) return;

  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
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

for (const button of elements.portalButtons) {
  button.addEventListener('click', () => openDrawer(button.dataset.tab, button));
}

elements.drawerClose.addEventListener('click', closeDrawer);
elements.drawerOverlay.addEventListener('click', closeDrawer);

elements.drawerTabs.addEventListener('click', (event) => {
  const tab = event.target.closest('.drawer-tab');
  if (tab) switchDrawerTab(tab.dataset.tab);
});

// tablist 的方向鍵操作：切到哪一個分頁由 core.js 的純函式決定。
elements.drawerTabs.addEventListener('keydown', (event) => {
  const currentIndex = DRAWER_TABS.indexOf(activeTab);
  const nextIndex = nextTabIndex(currentIndex, event.key);
  if (nextIndex === currentIndex) return;
  event.preventDefault();
  switchDrawerTab(DRAWER_TABS[nextIndex], { focusTab: true });
});

window.addEventListener('keydown', (event) => {
  if (event.key === 'Tab') trapFocus(event);
  if (event.key !== 'Escape') return;
  // 抽屜開著時 ESC 先關抽屜，抽屜沒開才離開 Zen 模式。
  if (drawerOpen) closeDrawer();
  else if (state.zenMode) setZenMode(false);
});

// =============================================================================
// 啟動：先還原狀態樹，再把畫面同步到還原後的狀態。
// 這裡的 persist 全部關閉——啟動只是把畫面對齊既有狀態，不是使用者的新選擇。
// =============================================================================
state = readStoredState();
setTheme(state.theme, { persist: false });
setTimeFormat(state.format24h, { persist: false });
setZenMode(state.zenMode, { persist: false, moveFocus: false });
startClock();
