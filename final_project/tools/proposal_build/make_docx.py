"""Build the proposal .docx from proposal-full.md with pandoc and a styled reference doc.

Usage: python -I make_docx.py <out_dir> <target.docx>
"""
import os
import subprocess
import sys

import pypandoc
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BODY_EA, BODY_LATIN = "新細明體", "Times New Roman"
HEAD_EA, HEAD_LATIN = "微軟正黑體", "Arial"
CODE_FONT = "Consolas"


def set_fonts(style, latin, ea, size=None, bold=None, color=None):
    font = style.font
    font.name = latin
    if size:
        font.size = Pt(size)
    if bold is not None:
        font.bold = bold
    if color is not None:
        font.color.rgb = color
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        rfonts.set(qn(attr), latin)
    rfonts.set(qn("w:eastAsia"), ea)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rfonts.get(qn(attr)) is not None:
            del rfonts.attrib[qn(attr)]


def make_reference(path):
    pandoc = pypandoc.get_pandoc_path()
    with open(path, "wb") as fh:
        fh.write(subprocess.run([pandoc, "--print-default-data-file", "reference.docx"],
                                capture_output=True, check=True).stdout)
    doc = Document(path)
    for sec in doc.sections:
        sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
        sec.left_margin = sec.right_margin = Cm(2.5)
        sec.top_margin = sec.bottom_margin = Cm(2.5)
    styles = doc.styles
    for name in ("Normal", "Body Text", "First Paragraph", "Compact", "Block Text"):
        if name in [s.name for s in styles]:
            st = styles[name]
            set_fonts(st, BODY_LATIN, BODY_EA, 12)
            pf = st.paragraph_format
            pf.line_spacing = 1.5
            pf.space_after = Pt(6)
    if "Compact" in [s.name for s in styles]:
        styles["Compact"].paragraph_format.line_spacing = 1.2
        styles["Compact"].paragraph_format.space_after = Pt(2)
    dark = RGBColor(0x1F, 0x2A, 0x24)
    for name, size in (("Heading 1", 16), ("Heading 2", 13.5), ("Heading 3", 12)):
        st = styles[name]
        set_fonts(st, HEAD_LATIN, HEAD_EA, size, bold=True, color=dark)
        st.paragraph_format.space_before = Pt(12 if name != "Heading 3" else 8)
        st.paragraph_format.space_after = Pt(6)
    styles["Heading 1"].paragraph_format.page_break_before = True
    for name, size in (("Title", 22), ("Subtitle", 14), ("Author", 12), ("Date", 12)):
        if name in [s.name for s in styles]:
            st = styles[name]
            set_fonts(st, HEAD_LATIN, HEAD_EA, size, bold=(name == "Title"), color=dark)
            st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for name in ("Source Code", "Verbatim Char"):
        if name in [s.name for s in styles]:
            set_fonts(styles[name], CODE_FONT, "微軟正黑體", 9)
    for name in ("Image Caption", "Caption", "Table Caption"):
        if name in [s.name for s in styles]:
            set_fonts(styles[name], BODY_LATIN, BODY_EA, 10.5, bold=False)
            styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if "TOC Heading" in [s.name for s in styles]:
        set_fonts(styles["TOC Heading"], HEAD_LATIN, HEAD_EA, 16, bold=True, color=dark)
    doc.save(path)


def border_tables(path):
    doc = Document(path)
    for table in doc.tables:
        tbl_pr = table._tbl.tblPr
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{edge}")
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "4")
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), "8A938C")
            borders.append(el)
        existing = tbl_pr.find(qn("w:tblBorders"))
        if existing is not None:
            tbl_pr.remove(existing)
        tbl_pr.append(borders)
        for r_i, row in enumerate(table.rows):
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = 1.15
                    p.paragraph_format.space_after = Pt(1)
                    for run in p.runs:
                        run.font.size = Pt(9.5)
                        if r_i == 0:
                            run.font.bold = True
                if r_i == 0:
                    shd = OxmlElement("w:shd")
                    shd.set(qn("w:val"), "clear")
                    shd.set(qn("w:color"), "auto")
                    shd.set(qn("w:fill"), "E6ECE7")
                    cell._tc.get_or_add_tcPr().append(shd)
    doc.save(path)


def main(out_dir, target):
    ref = os.path.join(out_dir, "reference.docx")
    make_reference(ref)
    # autolink_bare_uris keeps URLs out of smart typography ("--" would become an en dash)
    pypandoc.convert_file(
        os.path.join(out_dir, "proposal-full.md"), "docx", outputfile=target,
        format="markdown+tex_math_dollars+pipe_tables+implicit_figures+autolink_bare_uris",
        extra_args=["--reference-doc", ref, "--toc", "--toc-depth=2",
                    "--resource-path", out_dir, "--standalone"],
    )
    border_tables(target)
    print("wrote", target)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
