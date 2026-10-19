"""Appending a PDF's pages after another PDF (#66: the ChatGPT conversation appendix of the report).

Synthetic PDFs only (built here byte by byte); the author's material is never read by these tests.
The merge must keep every page of both files in order, copy the appended pages' objects byte for
byte apart from object numbers, keep the base file's catalog and information, and refuse inputs it
cannot copy faithfully."""
import re

import pytest

from hw2 import pdf_append


def make_pdf(n_pages: int, tag: str, *, note: bytes = b"(plain)", version: str = "1.4") -> bytes:
    """A small classic-xref PDF whose pages each carry a content stream naming the page."""
    objs = {1: b"<< /Type /Catalog /Pages 2 0 R /Lang (zh-TW) >>"}
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(n_pages))
    objs[2] = f"<< /Type /Pages /Kids [{kids}] /Count {n_pages} /MediaBox [0 0 200 200] >>".encode()
    for i in range(n_pages):
        content = f"BT /F1 12 Tf 20 100 Td ({tag} page {i + 1}) Tj ET".encode()
        objs[3 + 2 * i] = (f"<< /Type /Page /Parent 2 0 R /Contents {4 + 2 * i} 0 R /Note ".encode()
                           + note + b" >>")
        objs[4 + 2 * i] = b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream"
    info = 3 + 2 * n_pages
    objs[info] = b"<< /Producer (Test \\(writer\\)) /Title (\xfe\xff\x00A\x00B) /CreationDate (D:20261019095836+08'00') >>"
    return _serialize(objs, root=1, info=info, version=version)


def _serialize(objs: dict, root: int, info: int | None, version: str, prev: tuple | None = None) -> bytes:
    out = bytearray(prev[0] if prev else f"%PDF-{version}\n%\xe2\xe3\xcf\xd3\n".encode("latin-1"))
    offsets = {}
    for num in sorted(objs):
        offsets[num] = len(out)
        out += b"%d 0 obj\n" % num + objs[num] + b"\nendobj\n"
    start = len(out)
    out += b"xref\n"
    if prev:  # incremental update: one subsection per redefined object
        for num in sorted(offsets):
            out += b"%d 1\n%010d 00000 n\r\n" % (num, offsets[num])
    else:
        size = max(objs) + 1
        out += b"0 %d\n0000000000 65535 f\r\n" % size
        for num in range(1, size):
            out += b"%010d 00000 n\r\n" % offsets[num] if num in offsets else b"0000000000 00000 f\r\n"
    trailer = b"<< /Size %d /Root %d 0 R" % ((prev[2] if prev else max(objs) + 1), root)
    if info:
        trailer += b" /Info %d 0 R" % info
    if prev:
        trailer += b" /Prev %d" % prev[1]
    out += b"trailer\n" + trailer + b" >>\nstartxref\n%d\n%%%%EOF\n" % start
    return bytes(out)


def _pages_in_order(pdf: bytes) -> list[int]:
    p = pdf_append._Pdf(pdf)
    order = []

    def walk(num):
        d = p.dict_of(num)
        if p.data[d[b"/Type"][0]:d[b"/Type"][1]] == b"/Page":
            order.append(num)
            return
        for _, kid, _ in pdf_append._refs(p.data, d[b"/Kids"][2]):
            walk(kid)

    walk(p.pages_root())
    return order


def _content(pdf: bytes, page: int) -> bytes:
    p = pdf_append._Pdf(pdf)
    contents = p.ref_of(p.dict_of(page), b"/Contents")
    o = p.obj(contents)
    stream = p.data[o.stream[0]:o.stream[1]]
    return re.sub(rb"^stream\r?\n", b"", stream).rsplit(b"endstream", 1)[0].rstrip(b"\r\n")


def test_pages_of_both_files_in_order_and_unchanged():
    base, extra = make_pdf(3, "report"), make_pdf(2, "chat")
    merged = pdf_append.append_pages(base, extra)
    assert pdf_append.page_count(merged) == 5
    texts = [_content(merged, n) for n in _pages_in_order(merged)]
    assert texts == [b"BT /F1 12 Tf 20 100 Td (report page %d) Tj ET" % i for i in (1, 2, 3)] + \
                    [b"BT /F1 12 Tf 20 100 Td (chat page %d) Tj ET" % i for i in (1, 2)]


def test_cross_reference_offsets_point_at_their_objects():
    merged = pdf_append.append_pages(make_pdf(2, "a"), make_pdf(2, "b"))
    p = pdf_append._Pdf(merged)
    for num, (off, gen) in p.offsets.items():
        assert merged[off:].startswith(b"%d %d obj" % (num, gen)), num
    assert merged.startswith(b"%PDF-1.4\n") and merged.rstrip().endswith(b"%%EOF")


def test_base_catalog_and_information_are_kept_and_the_new_root_holds_both_trees():
    base, extra = make_pdf(1, "a"), make_pdf(1, "b")
    merged = pdf_append.append_pages(base, extra)
    p = pdf_append._Pdf(merged)
    assert p.root() == 1
    catalog = p.data[p.obj(1).value[0]:p.obj(1).value[1]]
    assert b"/Lang (zh-TW)" in catalog
    assert pdf_append.document_info(merged) == pdf_append.document_info(base)
    root = p.dict_of(p.pages_root())
    kids = [n for _, n, _ in pdf_append._refs(p.data, root[b"/Kids"][2])]
    assert len(kids) == 2 and kids[0] == 2
    for kid in kids:
        parent = p.ref_of(p.dict_of(kid), b"/Parent")
        assert parent == p.pages_root()
    inherited = p.data[p.obj(kids[1]).value[0]:p.obj(kids[1]).value[1]]
    assert b"/MediaBox [0 0 200 200]" in inherited     # the appended tree keeps its own attributes


def test_reference_lookalikes_inside_strings_are_not_renumbered():
    extra = make_pdf(1, "b", note=b"(see 3 0 R and 4 0 R)")
    merged = pdf_append.append_pages(make_pdf(4, "a"), extra)
    assert merged.count(b"(see 3 0 R and 4 0 R)") == 1


def test_the_newest_definition_of_an_incrementally_updated_object_is_used():
    first = make_pdf(2, "b")
    p = pdf_append._Pdf(first)
    sx = int(first.rsplit(b"startxref", 1)[1].split()[0])
    updated_page = b"<< /Type /Page /Parent 2 0 R /Contents 4 0 R /Rotate 90 /Note (updated) >>"
    updated = _serialize({3: updated_page}, root=1, info=None, version="1.4",
                         prev=(first, sx, max(p.offsets) + 1))
    merged = pdf_append.append_pages(make_pdf(1, "a"), updated)
    assert pdf_append.page_count(merged) == 3
    assert merged.count(b"/Note (updated)") == 1 and b"/Rotate 90" in merged


def test_version_is_the_higher_of_the_two():
    merged = pdf_append.append_pages(make_pdf(1, "a", version="1.4"), make_pdf(1, "b", version="1.7"))
    assert merged.startswith(b"%PDF-1.7\n")


def test_unsupported_inputs_are_refused():
    good = make_pdf(1, "a")
    xref_stream = good.replace(b"xref\n0 ", b"XREF\n0 ")
    with pytest.raises(pdf_append.PdfError):
        pdf_append.append_pages(good, xref_stream)
    with pytest.raises(pdf_append.PdfError):
        pdf_append.append_pages(good, b"not a pdf")
    bad_length = good.replace(b"<< /Length ", b"<< /Length 1", 1)
    with pytest.raises(pdf_append.PdfError):
        pdf_append.append_pages(good, bad_length)


def test_document_info_decodes_escapes_and_utf16():
    info = pdf_append.document_info(make_pdf(1, "a"))
    assert info["Producer"] == "Test (writer)"
    assert info["Title"] == "AB"
    assert info["CreationDate"] == "D:20261019095836+08'00'"


def test_whitespace_before_an_object_header_is_tolerated():
    """Some writers point the xref offset at the line break before "n 0 obj"."""
    pdf = make_pdf(1, "b")
    p = pdf_append._Pdf(pdf)
    off = p.offsets[1][0]
    shifted = pdf.replace(b"%010d 00000 n" % off, b"%010d 00000 n" % (off - 1), 1)
    assert shifted[off - 1:off] == b"\n"
    assert pdf_append.page_count(pdf_append.append_pages(make_pdf(1, "a"), shifted)) == 2
