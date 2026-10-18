// Report build helper (#65), driven by `python -m hw2.report`: headless Chrome/Edge over the
// DevTools protocol, offline (every host name is unresolvable; any non-file request is reported).
//
//   node chrome_capture.js shots <browser> <profile dir> <index.html> <out dir>
//     Screenshots of the real dashboard (it reads assets/model_data.js, the exported results):
//     overview, model (the overall CV winner's method selected), compare (the "compare all" chart),
//     test (the held-out test block with the per-row prediction intervals), methods.
//   node chrome_capture.js pdf <browser> <profile dir> <report.html> <out.pdf>
//     Prints the built report HTML to PDF (A4, backgrounds, page numbers in the footer).
//
// The last line of stdout is a JSON summary. Exit code 1 on any failure.
'use strict';
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const [mode, browser, profile, input, output] = process.argv.slice(2);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function withPage(width, height, fn) {
  const port = 9300 + Math.floor(Math.random() * 600);
  const proc = spawn(browser, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
    `--window-size=${width},${height}`, '--host-resolver-rules=MAP * ~NOTFOUND', '--no-first-run',
    '--no-default-browser-check', '--disable-extensions', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
  try {
    let targets;
    for (let i = 0; i < 100 && !targets; i++) {
      try { targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); } catch (e) { await sleep(200); }
    }
    if (!targets) throw new Error('the browser did not start');
    const ws = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
    await new Promise((r, j) => { ws.addEventListener('open', r); ws.addEventListener('error', j); });
    let id = 0; const pending = new Map(); const events = []; const external = [];
    ws.addEventListener('message', (m) => {
      const msg = JSON.parse(m.data);
      if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); return; }
      events.push(msg);
      if (msg.method === 'Network.requestWillBeSent') {
        const u = msg.params.request.url;
        if (!/^(file:|data:|about:|blob:)/.test(u)) external.push(u);
      }
    });
    const send = (method, params = {}) => new Promise((r, j) => {
      const i = ++id; pending.set(i, (msg) => (msg.error ? j(new Error(`${method}: ${JSON.stringify(msg.error)}`)) : r(msg.result)));
      ws.send(JSON.stringify({ id: i, method, params }));
    });
    const evalJs = async (expr) => {
      const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
      if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails));
      return r.result.value;
    };
    await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
    await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
    const version = (await send('Browser.getVersion')).product;
    const load = async (url) => {
      events.length = 0;
      await send('Page.navigate', { url });
      for (let i = 0; i < 300 && !events.some((e) => e.method === 'Page.loadEventFired'); i++) await sleep(100);
      if (!events.some((e) => e.method === 'Page.loadEventFired')) throw new Error(`no load event for ${url}`);
    };
    const result = await fn({ send, evalJs, load });
    ws.close();
    return Object.assign({ browser: version, external_requests: external }, result);
  } finally {
    proc.kill();
    await sleep(300);
  }
}

async function shots() {
  fs.mkdirSync(output, { recursive: true });
  return withPage(1280, 900, async ({ send, evalJs, load }) => {
    await load(pathToFileURL(path.resolve(input)).href);
    let firstDraw = null;
    for (let i = 0; i < 100 && !firstDraw; i++) { firstDraw = await evalJs('window.HW2_PERF && window.HW2_PERF.firstDraw ? window.HW2_PERF.firstDraw.ms : null'); if (!firstDraw) await sleep(100); }
    if (!firstDraw) throw new Error('the dashboard did not draw the test scatter plot');
    const loadError = await evalJs("(() => { const e = document.getElementById('load-error'); return e && !e.hidden ? e.textContent : null; })()");
    if (loadError) throw new Error(`dashboard load error: ${loadError}`);
    await evalJs("document.documentElement.style.scrollBehavior = 'auto'; document.querySelectorAll('*').forEach(e => { e.style.transition = 'none'; e.style.animation = 'none'; }); true");
    const clip = async (sel) => {
      const b = JSON.parse(await evalJs(`(() => { const r = document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect();
        return JSON.stringify({ x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height }); })()`));
      return { x: Math.max(0, b.x - 8), y: Math.max(0, b.y - 8), width: b.w + 16, height: b.h + 16, scale: 1 };
    };
    const shoot = async (name, sel) => {
      await sleep(400);
      const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: await clip(sel) });
      fs.writeFileSync(path.join(output, `${name}.png`), Buffer.from(shot.data, 'base64'));
      return name;
    };
    const click = async (sel) => {
      const ok = await evalJs(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return false; e.click(); return true; })()`);
      if (!ok) throw new Error(`no element ${sel}`);
      await sleep(500);
    };
    const taken = [];
    const overall = await evalJs('window.MODEL_DATA.winners.overall.method');
    taken.push(await shoot('overview', '#overview'));
    await click(`[data-method="${overall}"]`);
    taken.push(await shoot('model', '#model'));
    taken.push(await shoot('test', '#test'));
    await click('#compare-all');
    taken.push(await shoot('compare', '#kchart-card'));
    await click('#compare-all');
    taken.push(await shoot('methods', '#methods'));
    const testModel = await evalJs("document.getElementById('test-model').textContent");
    return { shots: taken, overall_method: overall, test_block_model: testModel, first_draw_ms: Math.round(firstDraw) };
  });
}

async function pdf() {
  return withPage(1240, 1754, async ({ send, load }) => {
    await load(pathToFileURL(path.resolve(input)).href);
    await sleep(500);
    const r = await send('Page.printToPDF', {
      printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#57606a;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    });
    const buf = Buffer.from(r.data, 'base64');
    fs.writeFileSync(output, buf);
    const pages = (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
    return { pdf: path.resolve(output), bytes: buf.length, pages };
  });
}

(async () => {
  try {
    const out = mode === 'shots' ? await shots() : mode === 'pdf' ? await pdf() : null;
    if (!out) throw new Error(`unknown mode ${mode}`);
    process.stdout.write(JSON.stringify(out) + '\n');
  } catch (e) {
    process.stderr.write(String(e && e.stack || e) + '\n');
    process.exit(1);
  }
})();
