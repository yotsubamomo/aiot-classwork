/**
 * app.js — 把 core.js 的純邏輯接到真實世界。
 *
 * 這一層負責所有副作用：DOM 查詢與事件、localStorage 讀寫、剪貼簿、計時器。
 * 需要判斷或計算的部分一律呼叫 core.js，不在這裡重複實作。
 */

import {
  CITIES,
  DRAWER_TABS,
  LEGACY_STORAGE_KEY,
  NAME_MAX_LENGTH,
  STORAGE_KEY,
  TAGLINE_MAX_LENGTH,
  THEME_COLORS,
  THEME_LABELS,
  TICK_SOUND,
  WEATHER_CACHE_KEY,
  buildTimestampText,
  dayOfYear,
  formatClockText,
  formatMilliseconds,
  formatTaipeiDate,
  formatWeatherReadout,
  findCity,
  greeting,
  initialsFrom,
  isDrawerTab,
  isoWeek,
  minuteProgress,
  nextTheme,
  nextTabIndex,
  normalizeProjects,
  normalizeState,
  normalizeWeather,
  ringDashOffset,
  sanitizeLine,
  shortcutAction,
  splitDisplayName,
  stateFromLegacyPreferences,
  taipeiTimeParts,
  unixSeconds,
  weatherApiUrl
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
  brandMark: document.querySelector('.brand-mark'),
  nameDisplay: document.querySelector('#name-display'),
  nameTrail: document.querySelector('#name-trail'),
  nameInput: document.querySelector('#name-input'),
  taglineDisplay: document.querySelector('#tagline-display'),
  taglineInput: document.querySelector('#tagline-input'),
  greetingIcon: document.querySelector('#greeting-icon'),
  greetingText: document.querySelector('#greeting-text'),
  themeButton: document.querySelector('#theme-button'),
  themeLabel: document.querySelector('#theme-label'),
  format24: document.querySelector('#format-24'),
  format12: document.querySelector('#format-12'),
  soundButton: document.querySelector('#sound-button'),
  soundLabel: document.querySelector('#sound-label'),
  soundOnIcon: document.querySelector('#sound-on'),
  soundMutedIcon: document.querySelector('#sound-muted'),
  copyButton: document.querySelector('#copy-button'),
  focusButton: document.querySelector('#focus-button'),
  focusExit: document.querySelector('#focus-exit'),
  weatherReadout: document.querySelector('#weather-readout'),
  citySelect: document.querySelector('#city-select'),
  projectGrid: document.querySelector('#project-grid'),
  projectStatus: document.querySelector('#project-status'),
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
let lastTickSecond = null;

function renderClock(now) {
  elements.milliseconds.textContent = formatMilliseconds(now);
  elements.secondRing.style.strokeDashoffset =
    ringDashOffset(minuteProgress(now), RING_CIRCUMFERENCE).toFixed(2);

  const second = unixSeconds(now);
  if (second === lastRenderedSecond) return;
  lastRenderedSecond = second;

  // 每個整秒響一次。用獨立的計數避免偏好變更觸發的強制重畫在同一秒內重複發聲。
  if (state.soundEnabled && second !== lastTickSecond) tickAudio.play();
  lastTickSecond = second;

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
// 滴答聲：用 Web Audio API 合成，不載入任何音檔。
//
// 瀏覽器的自動播放政策規定：AudioContext 必須在使用者互動之後才能發聲，
// 所以音訊一律等到使用者按下音效鈕（或已開啟時的第一次互動）才初始化。
// =============================================================================
class TickAudioEngine {
  constructor() {
    this.context = null;
  }

  /** 建立或恢復 AudioContext。回傳是否真的可以發聲。 */
  async enable() {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return false;

    if (!this.context) this.context = new AudioContextClass();
    if (this.context.state === 'suspended') {
      try {
        await this.context.resume();
      } catch (_) {
        return false;
      }
    }
    return this.context.state === 'running';
  }

  /** 暫停音訊，關掉音效後立刻安靜下來。 */
  suspend() {
    if (this.context && this.context.state === 'running') this.context.suspend();
  }

  get running() {
    return this.context?.state === 'running';
  }

  /** 播放一次滴答。頻率與音量的包絡都來自 core.js 的 TICK_SOUND。 */
  play() {
    if (!this.running) return;

    const now = this.context.currentTime;
    const end = now + TICK_SOUND.durationSeconds;
    const oscillator = this.context.createOscillator();
    const gain = this.context.createGain();

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(TICK_SOUND.startFrequency, now);
    oscillator.frequency.exponentialRampToValueAtTime(TICK_SOUND.endFrequency, end);
    gain.gain.setValueAtTime(TICK_SOUND.peakGain, now);
    gain.gain.exponentialRampToValueAtTime(TICK_SOUND.endGain, end);

    oscillator.connect(gain).connect(this.context.destination);
    oscillator.start(now);
    oscillator.stop(end + 0.005);
  }
}

const tickAudio = new TickAudioEngine();

function renderSoundButton() {
  const on = state.soundEnabled;
  elements.soundButton.setAttribute('aria-pressed', String(on));
  elements.soundLabel.textContent = on ? 'Sound on' : 'Sound off';
  elements.soundOnIcon.hidden = !on;
  elements.soundMutedIcon.hidden = on;
}

async function toggleSound() {
  if (state.soundEnabled) {
    updateState({ soundEnabled: false });
    tickAudio.suspend();
    renderSoundButton();
    return;
  }

  const ready = await tickAudio.enable();
  if (!ready) {
    // 瀏覽器不支援或拒絕啟動音訊時，不要假裝已經開啟。
    showToast('Sound is not available in this browser');
    return;
  }
  updateState({ soundEnabled: true });
  renderSoundButton();
}

/**
 * 上次造訪時音效是開著的話，狀態會被還原，但音訊仍然需要一次使用者互動才能發聲。
 * 這裡掛一次性的監聽，使用者第一次點擊或按鍵時再把 AudioContext 接起來。
 */
function resumeSoundOnFirstGesture() {
  if (!state.soundEnabled) return;

  const resume = () => {
    tickAudio.enable();
    document.removeEventListener('pointerdown', resume);
    document.removeEventListener('keydown', resume);
  };
  document.addEventListener('pointerdown', resume, { once: true });
  document.addEventListener('keydown', resume, { once: true });
}

// =============================================================================
// 身分：名稱與標語的就地編輯。
//
// 顯示與輸入是同一個位置的兩個元素，交替顯示，不用 contenteditable——
// 原生 input 的選取、輸入法與 maxlength 行為都比較可預期。
// 送出前一律經過 core.js 的清理函式，空值就還原前一個值。
// =============================================================================
let editing = false;

function renderIdentity() {
  const { lead, trail } = splitDisplayName(state.name);
  elements.nameDisplay.firstChild.textContent = lead;
  elements.nameTrail.textContent = trail;
  elements.nameDisplay.title = state.name;
  elements.taglineDisplay.textContent = state.tagline;
  elements.brandMark.textContent = initialsFrom(state.name);
}

function setupEditable({ display, input, stateKey, maxLength }) {
  const commit = () => {
    if (!editing) return;
    finishEdit();
    updateState({
      [stateKey]: sanitizeLine(input.value, { maxLength, fallback: state[stateKey] })
    });
    renderIdentity();
  };

  const cancel = () => {
    if (!editing) return;
    finishEdit();
    renderIdentity();
  };

  function finishEdit() {
    editing = false;
    input.hidden = true;
    display.hidden = false;
    display.focus();
  }

  const startEdit = () => {
    if (editing) return;
    editing = true;
    input.value = state[stateKey];
    display.hidden = true;
    input.hidden = false;
    input.focus();
    input.select();
  };

  display.addEventListener('click', startEdit);
  display.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      startEdit();
    }
  });

  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      commit();
    } else if (event.key === 'Escape') {
      // 編輯中的 Escape 只取消這次編輯，不該一路關掉抽屜或離開 Zen。
      event.preventDefault();
      event.stopPropagation();
      cancel();
    }
  });

  input.addEventListener('blur', commit);
}

// =============================================================================
// 即時天氣（Open-Meteo，不需要 API key）。
//
// 外部服務一定會有失敗的時候，所以成功的讀數會被快取起來；取不到資料時顯示上次的值
// 並明確標示是離線資料與它的時間，完全沒有快取才顯示 unavailable——不編造數字。
// 天氣的任何失敗都不影響時鐘、抽屜等其他功能。
// =============================================================================
const WEATHER_TIMEOUT_MS = 8000;
const WEATHER_REFRESH_MS = 10 * 60 * 1000;

let weatherRetryButton = null;

function readWeatherCache() {
  try {
    const cached = JSON.parse(localStorage.getItem(WEATHER_CACHE_KEY));
    return cached && typeof cached === 'object' ? cached : {};
  } catch (_) {
    return {};
  }
}

function writeWeatherCache(weather) {
  try {
    const cache = readWeatherCache();
    cache[weather.cityId] = weather;
    localStorage.setItem(WEATHER_CACHE_KEY, JSON.stringify(cache));
  } catch (_) {
    // 快取只是加分，存不進去也不影響這次的顯示。
  }
}

/** 快取讀數的時間，用台北時間的時與分表示。 */
function cacheTimeLabel(observedAt) {
  const parts = taipeiTimeParts(new Date(observedAt), { format24h: true });
  return `${parts.hour}:${parts.minute}`;
}

function setWeatherReadout(text, { stale = false, showRetry = false } = {}) {
  elements.weatherReadout.textContent = text;
  elements.weatherReadout.classList.toggle('is-stale', stale);

  if (weatherRetryButton) {
    weatherRetryButton.remove();
    weatherRetryButton = null;
  }
  if (!showRetry) return;

  weatherRetryButton = document.createElement('button');
  weatherRetryButton.type = 'button';
  weatherRetryButton.className = 'retry-button';
  weatherRetryButton.textContent = 'Retry';
  weatherRetryButton.addEventListener('click', () => loadWeather());
  elements.weatherReadout.after(weatherRetryButton);
}

function showWeatherFallback(cityId) {
  const cached = readWeatherCache()[cityId];
  const cityLabel = findCity(cityId).label;

  if (cached && normalizeWeather({ current: { temperature_2m: cached.temperature, weather_code: cached.code } }, { cityId })) {
    setWeatherReadout(
      `${formatWeatherReadout(cached)} · offline, last seen ${cacheTimeLabel(cached.observedAt)}`,
      { stale: true, showRetry: true }
    );
    return;
  }
  setWeatherReadout(`Weather unavailable · ${cityLabel}`, { stale: true, showRetry: true });
}

async function loadWeather() {
  const cityId = state.selectedCity;
  setWeatherReadout(`Loading weather · ${findCity(cityId).label}`);

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), WEATHER_TIMEOUT_MS);

  try {
    const response = await fetch(weatherApiUrl(cityId), { signal: controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const weather = normalizeWeather(await response.json(), { cityId });
    if (!weather) throw new Error('unexpected payload');

    writeWeatherCache(weather);
    setWeatherReadout(formatWeatherReadout(weather));
  } catch (_) {
    // 網路錯誤、逾時、HTTP 失敗與格式不符都走同一條路：退回快取或明說拿不到。
    showWeatherFallback(cityId);
  } finally {
    clearTimeout(timeout);
  }
}

function setupCitySelect() {
  elements.citySelect.replaceChildren(...CITIES.map((city) => {
    const option = document.createElement('option');
    option.value = city.id;
    option.textContent = city.label;
    return option;
  }));
  elements.citySelect.value = state.selectedCity;

  elements.citySelect.addEventListener('change', () => {
    updateState({ selectedCity: elements.citySelect.value });
    loadWeather();
  });
}

// =============================================================================
// 非同步載入專案目錄。
//
// 資料放在獨立的 JSON 檔，頁面本身沒有任何寫死的專案內容——新增作品只要改資料檔。
// 讀回來的東西先經過 core.js 正規化，再用 DOM API 一個一個節點建出來；
// 所有文字都走 textContent，不用字串拼 HTML，資料內容就不可能被當成標記執行。
// =============================================================================
const PROJECTS_URL = './projects.json';
const PROJECTS_TIMEOUT_MS = 8000;

function setProjectStatus(message, { showRetry = false } = {}) {
  elements.projectStatus.textContent = '';

  if (!message) {
    elements.projectStatus.hidden = true;
    return;
  }

  elements.projectStatus.hidden = false;
  elements.projectStatus.append(message);

  if (!showRetry) return;
  const retry = document.createElement('button');
  retry.type = 'button';
  retry.className = 'retry-button';
  retry.textContent = 'Try again';
  retry.addEventListener('click', loadProjects);
  elements.projectStatus.append(' ', retry);
}

/** 用 DOM API 建一張專案卡片。所有文字都是文字節點，不是字串拼出來的標記。 */
function projectCard(project) {
  const card = document.createElement('article');
  card.className = 'project-card';

  if (project.category || project.badge) {
    const meta = document.createElement('p');
    meta.className = 'project-meta';
    if (project.category) {
      const category = document.createElement('span');
      category.className = 'project-category';
      category.textContent = project.category;
      meta.append(category);
    }
    if (project.badge) {
      const badge = document.createElement('span');
      badge.className = 'project-badge';
      badge.textContent = project.badge;
      meta.append(badge);
    }
    card.append(meta);
  }

  const title = document.createElement('h3');
  title.className = 'project-title';
  title.textContent = project.title;
  card.append(title);

  const description = document.createElement('p');
  description.className = 'project-description';
  description.textContent = project.description;
  card.append(description);

  if (project.techStack.length > 0) {
    const tags = document.createElement('ul');
    tags.className = 'tag-list';
    for (const tag of project.techStack) {
      const item = document.createElement('li');
      item.className = 'tag';
      item.textContent = tag;
      tags.append(item);
    }
    card.append(tags);
  }

  const links = [
    { url: project.githubUrl, label: 'Source' },
    { url: project.demoUrl, label: 'Demo' }
  ].filter(({ url }) => url);

  if (links.length > 0) {
    const row = document.createElement('p');
    row.className = 'project-links';
    for (const { url, label } of links) {
      const link = document.createElement('a');
      link.className = 'project-link';
      link.href = url;
      // 連結文字帶上專案名稱，螢幕閱讀器逐條瀏覽連結時才分得出是哪一個專案的。
      link.textContent = `${label} — ${project.title}`;
      row.append(link);
    }
    card.append(row);
  }

  return card;
}

function renderProjects(projects) {
  elements.projectGrid.replaceChildren(...projects.map(projectCard));
}

async function loadProjects() {
  setProjectStatus('Loading projects…');
  elements.projectGrid.replaceChildren();

  // 逾時控制：網路卡住時不要讓載入狀態永遠停在那裡。
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), PROJECTS_TIMEOUT_MS);

  try {
    // cache: 'no-cache' 會帶條件請求向伺服器確認新舊。
    // 少了這行，改完 projects.json 重新整理仍然會看到瀏覽器快取的舊清單。
    const response = await fetch(PROJECTS_URL, { cache: 'no-cache', signal: controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const projects = normalizeProjects(await response.json());
    renderProjects(projects);
    setProjectStatus(projects.length === 0 ? 'No projects to show yet.' : '');
  } catch (_) {
    // 網路錯誤、逾時、HTTP 失敗與 JSON 解析失敗都走同一條路：說清楚並提供重試。
    elements.projectGrid.replaceChildren();
    setProjectStatus('Could not load the project catalogue.', { showRetry: true });
  } finally {
    clearTimeout(timeout);
  }
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
elements.soundButton.addEventListener('click', toggleSound);
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

/** 焦點是否在會吃鍵盤輸入的控制項上（輸入框、下拉選單…）。 */
function isFormField(target) {
  if (!(target instanceof HTMLElement)) return false;
  return target.matches('input, select, textarea, [contenteditable="true"]');
}

window.addEventListener('keydown', (event) => {
  if (event.key === 'Tab') trapFocus(event);

  const action = shortcutAction({
    key: event.key,
    ctrlKey: event.ctrlKey,
    metaKey: event.metaKey,
    altKey: event.altKey,
    fromFormField: isFormField(event.target),
    editing,
    drawerOpen,
    zenMode: state.zenMode
  });
  if (!action) return;

  event.preventDefault();
  switch (action) {
    case 'close-drawer':
      closeDrawer();
      break;
    case 'exit-zen':
      setZenMode(false);
      break;
    case 'toggle-zen':
      setZenMode(!state.zenMode);
      break;
    case 'toggle-format':
      setTimeFormat(!state.format24h);
      break;
    case 'copy-time':
      copyTime();
      break;
  }
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
loadProjects();
renderIdentity();
renderSoundButton();
// 上次是開著的話，等第一次互動再把音訊接起來（自動播放政策）。
resumeSoundOnFirstGesture();
setupEditable({ display: elements.nameDisplay, input: elements.nameInput, stateKey: 'name', maxLength: NAME_MAX_LENGTH });
setupEditable({ display: elements.taglineDisplay, input: elements.taglineInput, stateKey: 'tagline', maxLength: TAGLINE_MAX_LENGTH });
setupCitySelect();
loadWeather();
// 留著當桌鐘的話，讀數每十分鐘自己更新一次。
setInterval(loadWeather, WEATHER_REFRESH_MS);
