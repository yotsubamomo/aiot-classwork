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
 * Large inputs (#77; DA decision-20261022-issue77-resource-limits C2-R3): there is no byte limit (C2-R2).
 * When the bytes are in hand but cannot be decoded into one string (a JS engine refuses strings longer
 * than about 2^29 characters, i.e. an input larger than about 512 MiB, or the memory runs out), the same
 * checks are made on the bytes instead (inspectBytes): strict UTF-8 in chunks, U+FFFD / NUL, the RFC 4180
 * records counted byte by byte with the same rules and order as readRecords, the header record decoded on
 * its own, the record lengths. So an input over the row or column limit is TOO_LARGE whatever its size,
 * and every other reason is the one the text path would give. Only when all of these pass -- the input
 * is within the limits but this browser cannot hold it as text -- the result is not a LoadResult reason
 * but `{ ok: false, reason: null, environment_error: { stage, error, message, bytes } }`: the size made the
 * browser fail, which is reported as such (no new reason code; never ENCODING or a network cause). An
 * input that the text path can decode gets exactly the LoadResult it got before. options.decode (tests
 * only) replaces the decoder, to force this path on small inputs. In the URL entrance a body that the
 * browser cannot hold in memory (a RangeError from response.arrayBuffer()) is the same environment_error,
 * not URL_FETCH_FAILED / network: the response did arrive. SHA-256 is computed block by block from the
 * bytes, without a padded copy of the whole input.
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

  /* SHA-256 of the bytes, block by block (no padded copy of the whole input; #77 large inputs). */
  function sha256Hex(bytes) {
    var n = bytes.length;
    var h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
    var w = new Array(64);
    function rotr(x, r) { return (x >>> r) | (x << (32 - r)); }
    function block(m, off) {
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
    var full = n - (n % 64);
    for (var off = 0; off < full; off += 64) block(bytes, off);
    var restLen = n - full, tailLen = restLen + 9 <= 64 ? 64 : 128, tail = new Uint8Array(tailLen);
    for (var i = 0; i < restLen; i++) tail[i] = bytes[full + i];
    tail[restLen] = 0x80;
    var bitsHi = Math.floor(n / 0x20000000), bitsLo = (n * 8) >>> 0;
    tail[tailLen - 8] = bitsHi >>> 24; tail[tailLen - 7] = (bitsHi >>> 16) & 255; tail[tailLen - 6] = (bitsHi >>> 8) & 255; tail[tailLen - 5] = bitsHi & 255;
    tail[tailLen - 4] = bitsLo >>> 24; tail[tailLen - 3] = (bitsLo >>> 16) & 255; tail[tailLen - 2] = (bitsLo >>> 8) & 255; tail[tailLen - 1] = bitsLo & 255;
    for (off = 0; off < tailLen; off += 64) block(tail, off);
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

  /* The header checks, in order: NOT_CSV (one column), TOO_LARGE (columns), NO_HEADER, DUPLICATE_COLUMN. */
  function headerReason(header, limits, sha) {
    var ncol = header.length;
    if (ncol < 2) return reject('NOT_CSV', { problem: 'fewer_than_two_columns', columns: ncol }, sha);
    if (ncol > limits.maxColumns) return reject('TOO_LARGE', { columns: ncol, max_columns: limits.maxColumns }, sha);
    var emptyAt = header.indexOf('');
    if (emptyAt >= 0) return reject('NO_HEADER', { problem: 'empty_column_name', column: emptyAt }, sha);
    if (header.every(isNumberLiteral)) return reject('NO_HEADER', { problem: 'numeric_header' }, sha);
    var seen = new Map();                         /* a Map: any name, `__proto__` included, is a plain key */
    for (var c = 0; c < ncol; c++) {
      if (seen.has(header[c])) return reject('DUPLICATE_COLUMN', { name: header[c], columns: [seen.get(header[c]), c] }, sha);
      seen.set(header[c], c);
    }
    return null;
  }

  var CHUNK = 1 << 24;                            /* 16 MiB: decoded strings in the byte path stay small */
  function isSpaceByte(b) { return b === 0x20 || b === 0x09 || b === 0x0d || b === 0x0a || b === 0x0c || b === 0x0b; }

  /* The byte path (#77, C2-R3): the checks of the text path on bytes that could not be decoded into one
   * string; `error` is why decoding failed. Same reasons, details and order as the text path; when they all
   * pass, an environment_error (the input is within the limits but too large for this browser as text). */
  function inspectBytes(bytes, limits, error) {
    var sha = sha256Hex(bytes), n = bytes.length, i, b;
    var decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }), hasNul = false, hasFffd = false;
    try {
      for (i = 0; i < n; i += CHUNK) {
        var piece = decoder.decode(bytes.subarray(i, Math.min(n, i + CHUNK)), { stream: true });
        if (!hasNul && piece.indexOf('\u0000') >= 0) hasNul = true;
        if (!hasFffd && piece.indexOf('\ufffd') >= 0) hasFffd = true;
      }
      var last = decoder.decode();
      if (last.indexOf('\u0000') >= 0) hasNul = true;
      if (last.indexOf('\ufffd') >= 0) hasFffd = true;
    } catch (e) {
      return reject('ENCODING', { problem: 'not_utf8' }, sha);
    }
    var start = n >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf ? 3 : 0;
    if (hasNul || hasFffd) return reject('ENCODING', { problem: hasNul ? 'nul_character' : 'replacement_character' }, sha);
    var allSpace = true;
    for (i = start; i < n && allSpace; i++) if (!isSpaceByte(bytes[i])) allSpace = false;
    if (allSpace) return reject('NOT_CSV', { problem: 'empty' }, sha);
    /* readRecords on bytes: the structural characters are ASCII, which never occur inside a multi-byte
     * UTF-8 sequence; `unit` counts UTF-16 code units after the BOM, for the NOT_CSV offset. */
    var maxRows = limits.maxRows, nonBlank = 0, quoted = false, afterQuote = false, atFieldStart = true;
    var fields = 0, fieldLen = 0, fieldSpace = true, unit = 0;
    var hdrFrom = -1, hdrTo = -1, recStart = start, ncol = -1, ragged = null;
    function endField() { fields++; fieldLen = 0; fieldSpace = true; quoted = false; atFieldStart = true; afterQuote = false; }
    function endRecord(endAt) {
      var onlyField = fields === 0;               /* the field being closed is the record's first */
      var blank = onlyField && !quoted && fieldSpace;
      endField();
      if (!blank) {
        nonBlank++;
        if (nonBlank === 1) { hdrFrom = recStart; hdrTo = endAt; ncol = fields; }
        else if (ragged === null && fields !== ncol) ragged = { record: nonBlank - 1, found: fields };
      }
      fields = 0;
      return nonBlank - 1 > maxRows;
    }
    for (i = start; i < n;) {
      b = bytes[i];
      if (quoted && !afterQuote) {
        if (b === 0x22) {
          if (bytes[i + 1] === 0x22) { fieldLen++; i += 2; unit += 2; continue; }
          afterQuote = true; i++; unit++; continue;
        }
        fieldLen++; i++; unit += (b & 0xc0) !== 0x80 ? (b >= 0xf0 ? 2 : 1) : 0; continue;
      }
      if (b === 0x2c) { endField(); i++; unit++; continue; }
      if (b === 0x0d || b === 0x0a) {
        var endAt = i;
        if (b === 0x0d && bytes[i + 1] === 0x0a) { i++; unit++; }
        i++; unit++;
        if (endRecord(endAt)) return reject('TOO_LARGE', { rows_over: maxRows }, sha);
        recStart = i;
        continue;
      }
      if (afterQuote) {
        if (b === 0x20 || b === 0x09) { i++; unit++; continue; }
        return reject('NOT_CSV', { problem: 'text_after_closing_quote', offset: unit }, sha);
      }
      if (atFieldStart && b === 0x22) { quoted = true; atFieldStart = false; i++; unit++; continue; }
      atFieldStart = false;
      if (!(b === 0x20 || b === 0x09 || b === 0x0c || b === 0x0b)) fieldSpace = false;
      fieldLen++; i++; unit += (b & 0xc0) !== 0x80 ? (b >= 0xf0 ? 2 : 1) : 0;
    }
    if (quoted && !afterQuote) return reject('NOT_CSV', { problem: 'unterminated_quoted_field' }, sha);
    if (fieldLen > 0 || quoted || fields > 0) {
      if (endRecord(n)) return reject('TOO_LARGE', { rows_over: maxRows }, sha);
    }
    if (nonBlank === 0) return reject('NOT_CSV', { problem: 'empty' }, sha);
    var headerText = new TextDecoder('utf-8', { ignoreBOM: true }).decode(bytes.subarray(hdrFrom, hdrTo));
    var header = readRecords(headerText, 1).records[0].map(trimCell);
    var bad = headerReason(header, limits, sha);
    if (bad) return bad;
    if (ragged) return reject('RAGGED_ROWS', { record: ragged.record, expected: ncol, found: ragged.found }, sha);
    return { ok: false, reason: null, sha256: sha, detail: {},
      environment_error: { stage: 'decode', error: error && error.name ? String(error.name) : 'Error',
        message: error && error.message !== undefined ? String(error.message) : String(error), bytes: n } };
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
      try { text = (options.decode || decodeUtf8Strict)(bytes); } catch (e) {
        /* invalid UTF-8 is a TypeError; anything else is the input's size (string length, memory) */
        if (e && e.name === 'TypeError') return out(reject('ENCODING', { problem: 'not_utf8' }, sha256Hex(bytes)));
        return out(inspectBytes(bytes, limits, e));
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
    var bad = headerReason(header, limits, sha), c;
    if (bad) return out(bad);
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
        }, function (e) {
          /* the response arrived; the browser could not hold its body (C2-R3 (b)): not a network cause */
          if (e && e.name === 'RangeError') {
            done({ ok: false, reason: null, sha256: null, detail: {}, environment_error: { stage: 'read_body', error: 'RangeError',
              message: e.message !== undefined ? String(e.message) : '', status: Number(response.status) || 0 } });
            return;
          }
          throw e;
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
    inspectBytes: inspectBytes,
    utf8Bytes: utf8Bytes
  };
});
