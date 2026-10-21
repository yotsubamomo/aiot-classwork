/* HW2 V2 Exploratory run: the CSV load contract (Spec V2 「載入契約」, first layer of 「前處理與洩漏邊界」).
 *
 * loadCsv(input, options) is a pure function: CSV text (a string, or UTF-8 bytes) -> LoadResult. It
 * only checks the CSV structure, cell by cell and row by row (SR-V2-01); it never computes a
 * distribution, a number of distinct values or a variance of any column, so it may look at every
 * row. Which columns become feature groups (category limit, constant columns) is decided by the
 * engine on the training rows only (assets/explore_engine.js), never here: a LoadResult has no
 * kept / excluded state for any column.
 *
 * Rules (the Python reference hw2/explore_reference.py implements the same ones):
 * - Text: UTF-8; one leading BOM is removed. Bytes that are not valid UTF-8, or text containing
 *   U+FFFD or U+0000, -> ENCODING.
 * - Records: comma separated; a record ends at CRLF, LF or CR outside quotes. A field that starts
 *   with a double quote (its first character) is quoted (RFC 4180): "" is a quote inside it, it may
 *   hold commas and line ends, and its closing quote may be followed only by spaces or tabs and then
 *   a comma, a line end or the end of the text; an unterminated quoted field, or other text after a
 *   closing quote, -> NOT_CSV. A quote inside an
 *   unquoted field is kept as a literal character. A record that is one empty or blank unquoted
 *   field (an empty line) is skipped.
 * - Cells are trimmed of ASCII white space (space, tab, CR, LF, FF, VT) on both ends; header names
 *   too. An empty cell (after trimming) is a missing value.
 * - Header: the first record. Fewer than 2 columns or no record at all (blank text) -> NOT_CSV;
 *   more than LIMITS.maxColumns columns -> TOO_LARGE; an empty name, or every name a number
 *   literal (a header-less file) -> NO_HEADER; a repeated name -> DUPLICATE_COLUMN.
 * - Every data record must have as many fields as the header -> otherwise RAGGED_ROWS. More than
 *   LIMITS.maxRows data records -> TOO_LARGE (never truncated).
 * - Column type: numeric when it has at least one non-empty cell and every non-empty cell is a
 *   decimal number literal ([+-]digits[.digits][e[+-]digits], ASCII digits only) whose value is
 *   finite; otherwise categorical (the trimmed string). Only literal numbers are accepted: no hex,
 *   no "Infinity"/"NaN", no thousands separators, nothing is evaluated (DA D-2).
 * - Missing values: every data row with an empty cell is dropped and counted; fewer than
 *   LIMITS.minRows rows left -> TOO_FEW_ROWS.
 * - Target: options.target (a column name or index), default the last column; it must be numeric
 *   -> otherwise TARGET_NOT_NUMERIC. The target is not a feature.
 * - The checks run in this order, so a text breaking several rules gets the first code: ENCODING,
 *   NOT_CSV, TOO_LARGE (rows, found while reading), NOT_CSV (one column), TOO_LARGE (columns),
 *   NO_HEADER, DUPLICATE_COLUMN, RAGGED_ROWS, TOO_FEW_ROWS, TARGET_NOT_NUMERIC.
 * - sha256: of the raw input (the bytes, or the UTF-8 encoding of the given string).
 *
 * The load limits are the Spec's candidate values; the final numbers are measured and recorded in
 * ACCEPTANCE (Spec V2 「載入契約」「運算預算與載入上限的數字」).
 *
 * inspectCsv(input, options) returns the LoadResult together with the column list (name, index, type)
 * whenever the structure checks got that far, so that the page can offer the target drop-down even when
 * the default target is rejected (TARGET_NOT_NUMERIC). Column names are kept in Map / array form, never
 * as keys of plain objects, so that names such as `__proto__` or `constructor` are ordinary data
 * (#74 R1-F2): `__proto__,__proto__,y` is DUPLICATE_COLUMN like any other repeated name.
 *
 * The URL entrance (#76 V2-T3; Spec V2 「載入契約」入口, 「離線與請求隔離」; DA derivation D-1):
 * this is the only file of the unit that may call the network, and only in fetchCsvBytes(), which the
 * page calls when the user presses 「載入 URL」. Per submission it makes at most one request, to the
 * submitted URL itself: one call, GET, credentials 'omit' (no cookie or HTTP authentication), redirect
 * 'error' (a redirect is not followed; it fails like a network error), no custom header (a CORS simple
 * request, no preflight), no retry. A timeout aborts the request and nothing is sent again. The
 * network function is injectable (options.fetchImpl) so that Node tests can prove all of this with a
 * mock; without it the browser's own function is used. checkUrl() accepts only an absolute http(s)
 * URL without user name or password; anything else is refused before any request. Failures are
 * reported as { ok: false, reason: 'URL_FETCH_FAILED', detail: { cause } } with cause 'network'
 * (network error, cross-origin refusal or redirect), 'http_status' (with the status), 'timeout' or
 * 'not_text' (the body contains a NUL byte: binary data, not text). A body that is text but not UTF-8
 * goes on to loadCsv and is ENCODING there, exactly as the same bytes from a local file.
 *
 * It works in the browser (window.HW2ExploreLoad) and in Node (module.exports). Strings from the CSV,
 * the URL and the server are data only: nothing here writes to the page or stores anything. */
(function (root, factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.HW2ExploreLoad = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var LIMITS = { maxRows: 50000, maxColumns: 60, minRows: 20 };
  var REASONS = ['NOT_CSV', 'NO_HEADER', 'RAGGED_ROWS', 'ENCODING', 'TOO_LARGE', 'TOO_FEW_ROWS',
    'TARGET_NOT_NUMERIC', 'DUPLICATE_COLUMN'];
  var URL_REASON = 'URL_FETCH_FAILED';
  var URL_CAUSES = ['network', 'http_status', 'timeout', 'not_text'];
  var URL_TIMEOUT_MS = 20000;
  var NUMBER_LITERAL = /^[+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$/;
  var EDGE_SPACE = /^[ \t\r\n\f\v]+|[ \t\r\n\f\v]+$/g;

  function trimCell(s) { return String(s).replace(EDGE_SPACE, ''); }
  function isNumberLiteral(s) { return NUMBER_LITERAL.test(s) && isFinite(Number(s)); }

  /* ---- UTF-8 and SHA-256 (pure, synchronous; no Web Crypto, which needs a secure context) ---- */
  function utf8Bytes(text) {
    if (typeof TextEncoder !== 'undefined') return new TextEncoder().encode(text);
    var out = [];
    for (var i = 0; i < text.length; i++) {
      var c = text.codePointAt(i);
      if (c > 0xffff) i++;
      if (c < 0x80) out.push(c);
      else if (c < 0x800) out.push(0xc0 | (c >> 6), 0x80 | (c & 63));
      else if (c < 0x10000) out.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
      else out.push(0xf0 | (c >> 18), 0x80 | ((c >> 12) & 63), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
    }
    return Uint8Array.from(out);
  }

  var K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2];

  function sha256Hex(bytes) {
    var n = bytes.length;
    var total = ((n + 9 + 63) >> 6) << 6;
    var m = new Uint8Array(total);
    m.set(bytes);
    m[n] = 0x80;
    var bitsHi = Math.floor(n / 0x20000000), bitsLo = (n * 8) >>> 0;
    m[total - 8] = bitsHi >>> 24; m[total - 7] = (bitsHi >>> 16) & 255; m[total - 6] = (bitsHi >>> 8) & 255; m[total - 5] = bitsHi & 255;
    m[total - 4] = bitsLo >>> 24; m[total - 3] = (bitsLo >>> 16) & 255; m[total - 2] = (bitsLo >>> 8) & 255; m[total - 1] = bitsLo & 255;
    var h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
    var w = new Array(64);
    function rotr(x, r) { return (x >>> r) | (x << (32 - r)); }
    for (var off = 0; off < total; off += 64) {
      for (var t = 0; t < 16; t++) {
        var j = off + 4 * t;
        w[t] = ((m[j] << 24) | (m[j + 1] << 16) | (m[j + 2] << 8) | m[j + 3]) >>> 0;
      }
      for (t = 16; t < 64; t++) {
        var s0 = rotr(w[t - 15], 7) ^ rotr(w[t - 15], 18) ^ (w[t - 15] >>> 3);
        var s1 = rotr(w[t - 2], 17) ^ rotr(w[t - 2], 19) ^ (w[t - 2] >>> 10);
        w[t] = (w[t - 16] + s0 + w[t - 7] + s1) >>> 0;
      }
      var a = h[0], b = h[1], c = h[2], d = h[3], e = h[4], f = h[5], g = h[6], hh = h[7];
      for (t = 0; t < 64; t++) {
        var S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25);
        var ch = (e & f) ^ (~e & g);
        var t1 = (hh + S1 + ch + K[t] + w[t]) >>> 0;
        var S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22);
        var maj = (a & b) ^ (a & c) ^ (b & c);
        var t2 = (S0 + maj) >>> 0;
        hh = g; g = f; f = e; e = (d + t1) >>> 0; d = c; c = b; b = a; a = (t1 + t2) >>> 0;
      }
      h[0] = (h[0] + a) >>> 0; h[1] = (h[1] + b) >>> 0; h[2] = (h[2] + c) >>> 0; h[3] = (h[3] + d) >>> 0;
      h[4] = (h[4] + e) >>> 0; h[5] = (h[5] + f) >>> 0; h[6] = (h[6] + g) >>> 0; h[7] = (h[7] + hh) >>> 0;
    }
    return h.map(function (x) { return ('00000000' + x.toString(16)).slice(-8); }).join('');
  }

  function decodeUtf8Strict(bytes) {
    if (typeof TextDecoder === 'undefined') throw new Error('no TextDecoder');
    return new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes);
  }

  function reject(reason, detail, sha) {
    return { ok: false, reason: reason, detail: detail || {}, sha256: sha || null };
  }

  /* RFC 4180 record reader. Returns {records} or {error: 'NOT_CSV' | 'TOO_LARGE', detail}. */
  function readRecords(text, maxDataRecords) {
    var records = [], record = [], field = '', quoted = false, i = 0, n = text.length;
    var atFieldStart = true, afterQuote = false, nonBlank = 0;
    function endField() { record.push({ text: field, quoted: quoted }); field = ''; quoted = false; atFieldStart = true; afterQuote = false; }
    function endRecord() {
      endField();
      var blank = record.length === 1 && !record[0].quoted && trimCell(record[0].text) === '';
      if (!blank) {
        records.push(record.map(function (f) { return f.text; }));
        nonBlank++;
      }
      record = [];
      return nonBlank - 1 > maxDataRecords;                /* the header is not a data record */
    }
    while (i < n) {
      var ch = text.charAt(i);
      if (quoted && !afterQuote) {
        if (ch === '"') {
          if (text.charAt(i + 1) === '"') { field += '"'; i += 2; continue; }
          afterQuote = true; i++; continue;
        }
        field += ch; i++; continue;
      }
      if (ch === ',') { endField(); i++; continue; }
      if (ch === '\r' || ch === '\n') {
        if (ch === '\r' && text.charAt(i + 1) === '\n') i++;
        i++;
        if (endRecord()) return { error: 'TOO_LARGE', detail: { rows_over: maxDataRecords } };
        continue;
      }
      if (afterQuote) {
        if (ch === ' ' || ch === '\t') { i++; continue; }
        return { error: 'NOT_CSV', detail: { problem: 'text_after_closing_quote', offset: i } };
      }
      if (atFieldStart && ch === '"') { quoted = true; atFieldStart = false; i++; continue; }
      atFieldStart = false;
      field += ch; i++;
    }
    if (quoted && !afterQuote) return { error: 'NOT_CSV', detail: { problem: 'unterminated_quoted_field' } };
    if (field !== '' || quoted || record.length) {
      if (endRecord()) return { error: 'TOO_LARGE', detail: { rows_over: maxDataRecords } };
    }
    return { records: records };
  }

  function resolveTarget(names, target) {
    if (target === undefined || target === null) return names.length - 1;
    if (typeof target === 'number') {
      if (target >= 0 && target < names.length && Math.floor(target) === target) return target;
      throw new Error('target index out of range');
    }
    var idx = names.indexOf(String(target));
    if (idx < 0) throw new Error('target column not found');
    return idx;
  }

  /* CSV text (string) or UTF-8 bytes (Uint8Array / ArrayBuffer) -> { load: LoadResult, columns }.
   * `columns` (name, index, type) is set once the header, the record lengths and the column types are
   * known (every reason from TOO_FEW_ROWS on); otherwise it is null. */
  function inspectCsv(input, options) {
    options = options || {};
    var limits = Object.assign({}, LIMITS, options.limits || {});
    var bytes, text;
    function out(load, cols) { return { load: load, columns: cols || null }; }
    if (typeof input === 'string') {
      text = input;
      bytes = utf8Bytes(text);
    } else {
      bytes = input instanceof Uint8Array ? input : new Uint8Array(input);
      try { text = decodeUtf8Strict(bytes); } catch (e) {
        return out(reject('ENCODING', { problem: 'not_utf8' }, sha256Hex(bytes)));
      }
    }
    var sha = sha256Hex(bytes);
    if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);
    if (text.indexOf('�') >= 0 || text.indexOf('\u0000') >= 0) {
      return out(reject('ENCODING', { problem: text.indexOf('\u0000') >= 0 ? 'nul_character' : 'replacement_character' }, sha));
    }
    if (trimCell(text) === '') return out(reject('NOT_CSV', { problem: 'empty' }, sha));
    var read = readRecords(text, limits.maxRows);
    if (read.error) return out(reject(read.error, read.detail, sha));
    var records = read.records;
    if (!records.length) return out(reject('NOT_CSV', { problem: 'empty' }, sha));
    var header = records[0].map(trimCell);
    var ncol = header.length;
    if (ncol < 2) return out(reject('NOT_CSV', { problem: 'fewer_than_two_columns', columns: ncol }, sha));
    if (ncol > limits.maxColumns) return out(reject('TOO_LARGE', { columns: ncol, max_columns: limits.maxColumns }, sha));
    var emptyAt = header.indexOf('');
    if (emptyAt >= 0) return out(reject('NO_HEADER', { problem: 'empty_column_name', column: emptyAt }, sha));
    if (header.every(isNumberLiteral)) return out(reject('NO_HEADER', { problem: 'numeric_header' }, sha));
    var seen = new Map();                         /* a Map: any name, `__proto__` included, is a plain key */
    for (var c = 0; c < ncol; c++) {
      if (seen.has(header[c])) {
        return out(reject('DUPLICATE_COLUMN', { name: header[c], columns: [seen.get(header[c]), c] }, sha));
      }
      seen.set(header[c], c);
    }
    var data = records.slice(1);
    for (var r = 0; r < data.length; r++) {
      if (data[r].length !== ncol) {
        return out(reject('RAGGED_ROWS', { record: r + 1, expected: ncol, found: data[r].length }, sha));
      }
    }
    if (data.length > limits.maxRows) return out(reject('TOO_LARGE', { rows: data.length, max_rows: limits.maxRows }, sha));
    var cells = data.map(function (row) { return row.map(trimCell); });
    var types = [];
    for (c = 0; c < ncol; c++) {
      var nonEmpty = 0, numeric = true;
      for (r = 0; r < cells.length; r++) {
        var v = cells[r][c];
        if (v === '') continue;
        nonEmpty++;
        if (!isNumberLiteral(v)) { numeric = false; break; }
      }
      types.push(numeric && nonEmpty > 0 ? 'numeric' : 'categorical');
    }
    var columns = header.map(function (name, j) { return { name: name, index: j, type: types[j] }; });
    var kept = [], dropped = 0;
    for (r = 0; r < cells.length; r++) {
      if (cells[r].indexOf('') >= 0) { dropped++; continue; }
      kept.push(cells[r].map(function (s, j) { return types[j] === 'numeric' ? Number(s) : s; }));
    }
    if (kept.length < limits.minRows) {
      return out(reject('TOO_FEW_ROWS', { rows: kept.length, min_rows: limits.minRows, dropped_missing: dropped }, sha), columns);
    }
    var t = resolveTarget(header, options.target);
    if (types[t] !== 'numeric') return out(reject('TARGET_NOT_NUMERIC', { target: header[t], index: t }, sha), columns);
    return out({
      ok: true,
      sha256: sha,
      columns: columns.map(function (col) { return { name: col.name, index: col.index, type: col.type }; }),
      target: { name: header[t], index: t },
      rows: kept,
      n_rows_read: data.length,
      n_rows_dropped_missing: dropped,
      n_rows: kept.length,
      limits: limits
    }, columns);
  }

  /* CSV text (string) or UTF-8 bytes (Uint8Array / ArrayBuffer) -> LoadResult. */
  function loadCsv(input, options) { return inspectCsv(input, options).load; }

  /* ---- the URL entrance (#76; DA D-1) ------------------------------------------------------------ */

  /* Only an absolute http: or https: URL without user name / password is read; anything else is
   * refused here, before any request ({ ok: false, problem }). */
  function checkUrl(text) {
    var s = trimCell(text === undefined || text === null ? '' : String(text));
    if (s === '') return { ok: false, problem: 'empty' };
    var u;
    try { u = new URL(s); } catch (e) { return { ok: false, problem: 'not_absolute_url' }; }
    if (u.protocol !== 'http:' && u.protocol !== 'https:') return { ok: false, problem: 'not_http' };
    if (u.username !== '' || u.password !== '') return { ok: false, problem: 'has_credentials' };
    return { ok: true, url: u.href };
  }

  /* The init of the single request: exactly these members (DA D-1; asserted by the Node tests). */
  function requestInit(signal) {
    var init = { method: 'GET', credentials: 'omit', redirect: 'error' };
    if (signal) init.signal = signal;
    return init;
  }

  /* The browser's own network function; used only when no fetchImpl is injected. */
  function defaultFetch(url, init) { return fetch(url, init); }

  function urlFailure(cause, extra) {
    return { ok: false, reason: URL_REASON, detail: Object.assign({ cause: cause }, extra || {}), sha256: null };
  }

  function hasNulByte(bytes) {
    for (var i = 0; i < bytes.length; i++) if (bytes[i] === 0) return true;
    return false;
  }

  /* Read the submitted URL once -> Promise of { ok: true, url, bytes, status } or a URL_FETCH_FAILED
   * failure, or { ok: false, input_error } (refused before any request), or { ok: false, cancelled }
   * when options.signal aborts it (the page left the custom dataset or a new submission replaced it).
   * options: fetchImpl (injected network function), signal, timeoutMs. It never sends a second
   * request: no retry on any failure, a redirect is an error, the timeout aborts. */
  function fetchCsvBytes(text, options) {
    options = options || {};
    var checked = checkUrl(text);
    if (!checked.ok) return Promise.resolve({ ok: false, input_error: checked.problem });
    var doFetch = options.fetchImpl || defaultFetch;
    var timeoutMs = options.timeoutMs > 0 ? options.timeoutMs : URL_TIMEOUT_MS;
    var abort = typeof AbortController === 'function' ? new AbortController() : null;
    var hasTimer = typeof setTimeout === 'function';
    return new Promise(function (resolve) {
      var settled = false, timer = null;
      function done(value) {
        if (settled) return;
        settled = true;
        if (timer !== null && typeof clearTimeout === 'function') clearTimeout(timer);
        resolve(value);
      }
      function stop(value) { done(value); if (abort) abort.abort(); }
      if (options.signal) {
        if (options.signal.aborted) { done({ ok: false, cancelled: true }); return; }
        options.signal.addEventListener('abort', function () { stop({ ok: false, cancelled: true }); });
      }
      if (hasTimer) timer = setTimeout(function () { stop(urlFailure('timeout', { timeout_ms: timeoutMs })); }, timeoutMs);
      var pending;
      try { pending = doFetch(checked.url, requestInit(abort ? abort.signal : null)); } catch (e) {
        done(urlFailure('network'));
        return;
      }
      Promise.resolve(pending).then(function (response) {
        if (settled) return null;
        if (!response || !response.ok) {
          done(urlFailure('http_status', { status: response ? Number(response.status) || 0 : 0,
            status_text: response && response.statusText ? String(response.statusText) : '' }));
          return null;
        }
        return Promise.resolve(response.arrayBuffer()).then(function (buffer) {
          var bytes = new Uint8Array(buffer);
          if (hasNulByte(bytes)) done(urlFailure('not_text', { bytes: bytes.length }));
          else done({ ok: true, url: checked.url, bytes: bytes, status: Number(response.status) || 0 });
        });
      }).then(null, function () { done(urlFailure('network')); });
    });
  }

  return {
    LIMITS: LIMITS,
    REASONS: REASONS,
    URL_REASON: URL_REASON,
    URL_CAUSES: URL_CAUSES,
    URL_TIMEOUT_MS: URL_TIMEOUT_MS,
    loadCsv: loadCsv,
    inspectCsv: inspectCsv,
    checkUrl: checkUrl,
    requestInit: requestInit,
    fetchCsvBytes: fetchCsvBytes,
    isNumberLiteral: isNumberLiteral,
    trimCell: trimCell,
    sha256Hex: sha256Hex,
    utf8Bytes: utf8Bytes
  };
});
