"""Append the pages of one PDF after the pages of another, without re-rendering anything (#66).

The report PDF must contain the author's ChatGPT conversation PDF as its appendix (assignment page:
the report "needs to include" the exported GPT conversation). The appendix pages are copied object
by object: page content streams, images and fonts are written byte for byte, only object numbers
are shifted. The page trees of both files are kept and placed under one new root ``/Pages`` node,
so attributes inherited inside each tree (resources, media box) stay where they were.

Supported input: PDFs with classic cross-reference tables (``xref`` ... ``trailer``), including
incremental updates (``/Prev``). Cross-reference streams and object streams (PDF 1.5 compression)
are refused with :class:`PdfError` instead of being guessed at; Chrome's Skia output and
"Microsoft: Print To PDF" both use classic tables.

No third-party package is needed (``requirements.txt`` is frozen).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_WS = b" \t\r\n\f\x00"
_DELIM = b"()<>[]{}/%"
_OBJ_HEAD = re.compile(rb"(\d+)\s+(\d+)\s+obj(?=[\s<\[/(%]|$)")
_XREF_ENTRY = re.compile(rb"(\d{10})[ ](\d{5})[ ]([nf])")
_INT = re.compile(rb"[+-]?\d+")
_VERSION = re.compile(rb"%PDF-(\d+)\.(\d+)")


class PdfError(ValueError):
    """The input is not a PDF this module can copy faithfully."""


def _skip_ws(data: bytes, i: int, end: int) -> int:
    while i < end:
        c = data[i]
        if c in _WS:
            i += 1
        elif c == 0x25:  # % comment, up to the end of the line
            while i < end and data[i] not in b"\r\n":
                i += 1
        else:
            break
    return i


def _lex(data: bytes, i: int, end: int):
    """Yield (kind, start, stop) for the tokens of data[i:end].

    Kinds: ``<<``, ``>>``, ``[``, ``]``, ``{``, ``}``, ``name``, ``str`` (literal), ``hex``,
    ``int`` and ``kw`` (any other regular token: reals, ``R``, ``obj``, ``stream``, ``true``...)."""
    while True:
        i = _skip_ws(data, i, end)
        if i >= end:
            return
        c = data[i]
        if c == 0x28:  # ( literal string: balanced parentheses, backslash escapes
            j, depth = i + 1, 1
            while j < end and depth:
                b = data[j]
                if b == 0x5C:
                    j += 2
                    continue
                if b == 0x28:
                    depth += 1
                elif b == 0x29:
                    depth -= 1
                j += 1
            if depth:
                raise PdfError(f"unterminated literal string at byte {i}")
            yield "str", i, j
            i = j
        elif c == 0x3C:  # < hex string or <<
            if data[i + 1:i + 2] == b"<":
                yield "<<", i, i + 2
                i += 2
            else:
                j = data.find(b">", i, end)
                if j < 0:
                    raise PdfError(f"unterminated hex string at byte {i}")
                yield "hex", i, j + 1
                i = j + 1
        elif c == 0x3E:
            if data[i + 1:i + 2] != b">":
                raise PdfError(f"unexpected '>' at byte {i}")
            yield ">>", i, i + 2
            i += 2
        elif c in b"[]{}":
            yield chr(c), i, i + 1
            i += 1
        elif c == 0x2F:  # /name
            j = i + 1
            while j < end and data[j] not in _WS and data[j] not in _DELIM:
                j += 1
            yield "name", i, j
            i = j
        else:
            j = i
            while j < end and data[j] not in _WS and data[j] not in _DELIM:
                j += 1
            if j == i:
                raise PdfError(f"unexpected byte {data[i:i + 1]!r} at byte {i}")
            yield ("int" if _INT.fullmatch(data, i, j) else "kw"), i, j
            i = j


def _value_end(data: bytes, toks: list, k: int) -> int:
    """Index just past the value that starts at toks[k] (a dict, array, ref or single token)."""
    kind = toks[k][0]
    if kind in ("<<", "[", "{"):
        close = {"<<": ">>", "[": "]", "{": "}"}
        depth, j = 0, k
        while j < len(toks):
            if toks[j][0] in close:
                depth += 1
            elif toks[j][0] in (">>", "]", "}"):
                depth -= 1
                if depth == 0:
                    return j + 1
            j += 1
        raise PdfError("unbalanced dictionary or array")
    if (kind == "int" and k + 2 < len(toks) and toks[k + 1][0] == "int"
            and toks[k + 2][0] == "kw" and data[toks[k + 2][1]:toks[k + 2][2]] == b"R"):
        return k + 3  # an indirect reference "n g R"
    return k + 1


def _refs(data: bytes, toks: list):
    """Yield (index_of_first_int, num, gen) for every "n g R" reference in toks."""
    for k in range(len(toks) - 2):
        if (toks[k][0] == "int" and toks[k + 1][0] == "int" and toks[k + 2][0] == "kw"
                and data[toks[k + 2][1]:toks[k + 2][2]] == b"R"):
            yield k, int(data[toks[k][1]:toks[k][2]]), int(data[toks[k + 1][1]:toks[k + 1][2]])


def _dict_entries(data: bytes, s: int, e: int) -> dict[bytes, tuple[int, int, list]]:
    """Top-level entries of the dictionary in data[s:e]: {key: (value_start, value_stop, tokens)}."""
    toks = list(_lex(data, s, e))
    if not toks or toks[0][0] != "<<":
        raise PdfError(f"expected a dictionary at byte {s}")
    out, k = {}, 1
    while k < len(toks) and toks[k][0] != ">>":
        if toks[k][0] != "name":
            raise PdfError(f"expected a name key at byte {toks[k][1]}")
        key = data[toks[k][1]:toks[k][2]]
        j = _value_end(data, toks, k + 1)
        out[key] = (toks[k + 1][1], toks[j - 1][2], toks[k + 1:j])
        k = j
    return out


@dataclass
class _Obj:
    num: int
    gen: int
    value: tuple[int, int]            # span of the object's value (dictionary, array, ...)
    stream: tuple[int, int] | None    # span from the "stream" keyword through "endstream"


class _Pdf:
    """Objects of one PDF file, located through its classic cross-reference tables."""

    def __init__(self, data: bytes):
        self.data = data
        m = _VERSION.match(data)
        if not m:
            raise PdfError("missing %PDF- header")
        self.version = (int(m.group(1)), int(m.group(2)))
        self.offsets: dict[int, tuple[int, int]] = {}   # num -> (offset, gen), in-use objects only
        self.trailer: dict[bytes, tuple[int, int, list]] = {}
        self._read_xref_chain()
        self._cache: dict[int, _Obj] = {}

    # -- cross-reference tables -----------------------------------------------------------------
    def _read_xref_chain(self):
        data = self.data
        sx = data.rfind(b"startxref")
        if sx < 0:
            raise PdfError("missing startxref")
        toks = list(_lex(data, sx + len(b"startxref"), min(len(data), sx + 40)))
        if not toks or toks[0][0] != "int":
            raise PdfError("malformed startxref")
        offset = int(data[toks[0][1]:toks[0][2]])
        seen_free: set[int] = set()
        visited: set[int] = set()
        first = True
        while offset is not None:
            if offset in visited:
                raise PdfError("cyclic /Prev chain")
            visited.add(offset)
            pos = _skip_ws(data, offset, len(data))
            if not data.startswith(b"xref", pos):
                raise PdfError("cross-reference streams are not supported")
            pos += 4
            while True:
                pos = _skip_ws(data, pos, len(data))
                if data.startswith(b"trailer", pos):
                    break
                head = re.compile(rb"(\d+)\s+(\d+)").match(data, pos)
                if not head:
                    raise PdfError(f"malformed xref subsection at byte {pos}")
                start, count = int(head.group(1)), int(head.group(2))
                pos = head.end()
                for n in range(start, start + count):
                    pos = _skip_ws(data, pos, len(data))
                    entry = _XREF_ENTRY.match(data, pos)
                    if not entry:
                        raise PdfError(f"malformed xref entry at byte {pos}")
                    pos = entry.end()
                    if n in self.offsets or n in seen_free:
                        continue  # a newer section already defined this object
                    if entry.group(3) == b"n":
                        self.offsets[n] = (int(entry.group(1)), int(entry.group(2)))
                    else:
                        seen_free.add(n)
            tpos = _skip_ws(data, pos + len(b"trailer"), len(data))
            tend = self._dict_end(tpos)
            entries = _dict_entries(data, tpos, tend)
            if b"/XRefStm" in entries:
                raise PdfError("hybrid files with cross-reference streams are not supported")
            if first:
                self.trailer = entries
                first = False
            prev = entries.get(b"/Prev")
            offset = int(data[prev[0]:prev[1]]) if prev else None
        if b"/Root" not in self.trailer:
            raise PdfError("trailer has no /Root")

    def _dict_end(self, s: int) -> int:
        depth = 0
        for kind, _, e in _lex(self.data, s, len(self.data)):
            if kind == "<<":
                depth += 1
            elif kind == ">>":
                depth -= 1
                if depth == 0:
                    return e
        raise PdfError(f"unterminated dictionary at byte {s}")

    # -- objects --------------------------------------------------------------------------------
    def obj(self, num: int) -> _Obj:
        if num in self._cache:
            return self._cache[num]
        if num not in self.offsets:
            raise PdfError(f"object {num} is not in the cross-reference table")
        data = self.data
        off, gen = self.offsets[num]
        # Some writers ("Microsoft: Print To PDF") point at the line break before the header.
        m = _OBJ_HEAD.match(data, _skip_ws(data, off, len(data)))
        if not m or int(m.group(1)) != num:
            raise PdfError(f"object {num} is not at its xref offset {off}")
        vs = m.end()
        depth, stop = 0, None
        for kind, s, e in _lex(data, vs, len(data)):
            if kind in ("<<", "[", "{"):
                depth += 1
            elif kind in (">>", "]", "}"):
                depth -= 1
            elif kind == "kw" and depth == 0 and data[s:e] in (b"stream", b"endobj"):
                stop = (s, e)
                break
        if stop is None:
            raise PdfError(f"object {num} has no endobj")
        s, e = stop
        if data[s:e] == b"endobj":
            o = _Obj(num, int(m.group(2)), (vs, s), None)
        else:
            p = e + (2 if data[e:e + 2] == b"\r\n" else 1)
            length = self.stream_length(vs, s)
            q = _skip_ws(data, p + length, len(data))
            if not data.startswith(b"endstream", q):
                raise PdfError(f"object {num}: stream /Length does not end at endstream")
            q += len(b"endstream")
            r = _skip_ws(data, q, len(data))
            if not data.startswith(b"endobj", r):
                raise PdfError(f"object {num}: no endobj after endstream")
            o = _Obj(num, int(m.group(2)), (vs, s), (s, q))
        self._cache[num] = o
        return o

    def stream_length(self, s: int, e: int) -> int:
        entries = _dict_entries(self.data, s, self._dict_end(s))
        if b"/Length" not in entries:
            raise PdfError(f"stream without /Length at byte {s}")
        vs, ve, toks = entries[b"/Length"]
        refs = list(_refs(self.data, toks))
        if refs:
            target = self.obj(refs[0][1])
            text = self.data[target.value[0]:target.value[1]].strip()
            if not _INT.fullmatch(text):
                raise PdfError("indirect /Length is not an integer")
            return int(text)
        return int(self.data[vs:ve])

    def value_tokens(self, num: int) -> list:
        o = self.obj(num)
        return list(_lex(self.data, *o.value))

    def dict_of(self, num: int) -> dict[bytes, tuple[int, int, list]]:
        o = self.obj(num)
        s = _skip_ws(self.data, o.value[0], o.value[1])
        return _dict_entries(self.data, s, self._dict_end(s))

    def ref_of(self, entries, key: bytes) -> int:
        if key not in entries:
            raise PdfError(f"missing {key.decode()}")
        refs = list(_refs(self.data, entries[key][2]))
        if not refs:
            raise PdfError(f"{key.decode()} is not a reference")
        return refs[0][1]

    def int_of(self, entries, key: bytes) -> int:
        if key not in entries:
            raise PdfError(f"missing {key.decode()}")
        vs, ve, _ = entries[key]
        return int(self.data[vs:ve])

    def root(self) -> int:
        return self.ref_of(self.trailer, b"/Root")

    def pages_root(self) -> int:
        return self.ref_of(self.dict_of(self.root()), b"/Pages")

    def reachable(self, start: int) -> set[int]:
        seen, todo = set(), [start]
        while todo:
            n = todo.pop()
            if n in seen:
                continue
            if n not in self.offsets:
                raise PdfError(f"reference to missing object {n}")
            seen.add(n)
            todo.extend(num for _, num, _ in _refs(self.data, self.value_tokens(n)))
        return seen


def _renumber(data: bytes, span: tuple[int, int], mapping: dict[int, int]) -> bytes:
    """data[span] with every "n g R" reference renumbered through mapping (strings untouched)."""
    s, e = span
    toks = list(_lex(data, s, e))
    out, pos = [], s
    for k, num, _ in _refs(data, toks):
        out.append(data[pos:toks[k][1]])
        out.append(str(mapping[num]).encode())
        pos = toks[k][2]
    out.append(data[pos:e])
    return b"".join(out)


def _insert_after_dict_open(value: bytes, insertion: bytes) -> bytes:
    i = value.find(b"<<")
    if i < 0:
        raise PdfError("expected a dictionary")
    return value[:i + 2] + insertion + value[i + 2:]


def _replace_ref(value: bytes, key: bytes, new_num: int) -> bytes:
    """value (a dictionary) with the reference of its top-level key replaced by new_num."""
    s = _skip_ws(value, 0, len(value))
    entries = _dict_entries(value, s, len(value))
    if key not in entries:
        raise PdfError(f"missing {key.decode()}")
    refs = list(_refs(value, entries[key][2]))
    if not refs:
        raise PdfError(f"{key.decode()} is not a reference")
    first = entries[key][2][refs[0][0]]
    return value[:first[1]] + str(new_num).encode() + value[first[2]:]


def page_count(pdf: bytes) -> int:
    """Number of leaf pages reachable from the document's page tree."""
    p = _Pdf(pdf)

    def count(num: int, depth: int = 0) -> int:
        if depth > 64:
            raise PdfError("page tree too deep")
        d = p.dict_of(num)
        kind = p.data[d[b"/Type"][0]:d[b"/Type"][1]] if b"/Type" in d else b""
        if kind == b"/Page":
            return 1
        kids = d.get(b"/Kids")
        if kids is None:
            raise PdfError(f"page-tree node {num} has no /Kids")
        return sum(count(n, depth + 1) for _, n, _ in _refs(p.data, kids[2]))

    return count(p.pages_root())


def _decode_literal(raw: bytes) -> str:
    """Text of a PDF literal string token ``(...)``: escapes resolved, UTF-16BE or PDFDocEncoding
    (read as Latin-1, which matches it for printable ASCII)."""
    body, out, i = raw[1:-1], bytearray(), 0
    escapes = {ord("n"): 10, ord("r"): 13, ord("t"): 9, ord("b"): 8, ord("f"): 12}
    while i < len(body):
        c = body[i]
        if c != 0x5C:
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= len(body):
            break
        c = body[i]
        if c in escapes:
            out.append(escapes[c])
            i += 1
        elif 0x30 <= c <= 0x37:
            j = i
            while j < len(body) and j < i + 3 and 0x30 <= body[j] <= 0x37:
                j += 1
            out.append(int(body[i:j], 8) & 0xFF)
            i = j
        elif c in b"\r\n":  # line continuation
            i += 2 if body[i:i + 2] == b"\r\n" else 1
        else:
            out.append(c)
            i += 1
    data = bytes(out)
    if data.startswith(b"\xfe\xff"):
        return data[2:].decode("utf-16-be", errors="replace")
    return data.decode("latin-1")


def document_info(pdf: bytes) -> dict[str, str]:
    """The literal-string entries of the document information dictionary (Title, Producer...)."""
    p = _Pdf(pdf)
    if b"/Info" not in p.trailer:
        return {}
    entries = p.dict_of(p.ref_of(p.trailer, b"/Info"))
    out = {}
    for key, (vs, ve, toks) in entries.items():
        if len(toks) == 1 and toks[0][0] == "str":
            out[key[1:].decode("latin-1")] = _decode_literal(p.data[vs:ve])
    return out


def append_pages(base: bytes, extra: bytes) -> bytes:
    """A new PDF: every page of ``base``, then every page of ``extra``.

    All objects of ``base`` are kept with their numbers (its catalog, document information and
    tagging stay as they were); the objects of ``extra`` reachable from its page tree are appended
    with shifted numbers. A new root ``/Pages`` node holds the two original page trees in order.
    """
    a, b = _Pdf(base), _Pdf(extra)
    a_catalog, a_pages = a.root(), a.pages_root()
    b_pages = b.pages_root()
    for pdf, root in ((a, a_pages), (b, b_pages)):
        if b"/Parent" in pdf.dict_of(root):
            raise PdfError("the root page-tree node has a /Parent")
    a_count = a.int_of(a.dict_of(a_pages), b"/Count")
    b_count = b.int_of(b.dict_of(b_pages), b"/Count")
    keep_b = b.reachable(b_pages)
    shift = max(a.offsets)
    mapping = {n: n + shift for n in keep_b}
    new_root = max(mapping.values()) + 1
    version = max(a.version, b.version)

    out = bytearray(b"%%PDF-%d.%d\n%%\xe2\xe3\xcf\xd3\n" % version)
    xref: dict[int, tuple[int, int]] = {}

    def write(num: int, gen: int, value: bytes, stream: bytes | None):
        xref[num] = (len(out), gen)
        out.extend(b"%d %d obj\n" % (num, gen))
        out.extend(value.strip(_WS))
        if stream is not None:
            out.extend(b"\n")
            out.extend(stream)
        out.extend(b"\nendobj\n")

    parent = b"/Parent %d 0 R " % new_root
    for num in sorted(a.offsets):
        o = a.obj(num)
        value = a.data[o.value[0]:o.value[1]]
        if num == a_pages:
            value = _insert_after_dict_open(value, parent)
        if num == a_catalog:
            value = _replace_ref(value, b"/Pages", new_root)
        write(num, o.gen, value, a.data[o.stream[0]:o.stream[1]] if o.stream else None)
    for num in sorted(keep_b):
        o = b.obj(num)
        value = _renumber(b.data, o.value, mapping)
        if num == b_pages:
            value = _insert_after_dict_open(value, parent)
        write(mapping[num], o.gen, value, b.data[o.stream[0]:o.stream[1]] if o.stream else None)
    write(new_root, 0, b"<< /Type /Pages /Kids [%d 0 R %d 0 R] /Count %d >>"
          % (a_pages, mapping[b_pages], a_count + b_count), None)

    size = new_root + 1
    start = len(out)
    out.extend(b"xref\n0 %d\n" % size)
    for n in range(size):
        if n in xref:
            out.extend(b"%010d %05d n\r\n" % xref[n])
        else:
            out.extend(b"0000000000 65535 f\r\n" if n == 0 else b"0000000000 00000 f\r\n")
    trailer = b"<< /Size %d /Root %d %d R" % (size, a_catalog, a.offsets[a_catalog][1])
    if b"/Info" in a.trailer:
        info = a.ref_of(a.trailer, b"/Info")
        trailer += b" /Info %d %d R" % (info, a.offsets[info][1])
    out.extend(b"trailer\n" + trailer + b" >>\nstartxref\n%d\n%%%%EOF\n" % start)
    return bytes(out)
