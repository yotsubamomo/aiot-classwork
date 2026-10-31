"""Build the proposal slides (.pptx) and narrated video (.mp4 + .srt) from doc/proposal/slides.md.

Usage: python -I build_slides.py [--pptx-only]
slides.md is the source of truth; the .pptx is regenerated, so do not edit it by hand.
"""
import asyncio
import os
import re
import shutil
import subprocess
import sys

import edge_tts
import imageio_ffmpeg
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
PROPOSAL = os.path.normpath(os.path.join(HERE, "..", "..", "doc", "proposal"))
SRC = os.path.join(PROPOSAL, "slides.md")
OUT = os.path.join(HERE, ".out")

FONT, CODE_FONT = "Microsoft JhengHei", "Consolas"
INK = RGBColor(0x1F, 0x2A, 0x24)
MUTED = RGBColor(0x5B, 0x66, 0x5F)
ACCENT = RGBColor(0x2F, 0x6B, 0x4F)
ACCENT_SOFT = RGBColor(0xE3, 0xEE, 0xE7)
ROW_ALT = RGBColor(0xF4, 0xF6, 0xF3)
CODE_BG = RGBColor(0xF1, 0xF3, 0xF0)
W, H = Inches(13.333), Inches(7.5)
LEFT, RIGHT = Inches(0.7), Inches(0.7)
CONTENT_TOP, CONTENT_BOTTOM = Inches(1.55), Inches(6.45)

# ---------------------------------------------------------------- parsing


def parse(path):
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    slides = []
    for chunk in re.split(r"^## ", text, flags=re.M)[1:]:
        title, _, rest = chunk.partition("\n")
        body, _, script = rest.partition("### 逐字稿")
        slide = {"title": title.strip(), "layout": "bullets", "bullets": [], "table": [], "image": None,
                 "mermaid": None, "code": None, "source": None, "notes": [], "script": script.strip()}
        diagram = re.search(r"```mermaid\n(.*?)```", body, flags=re.S)
        if diagram:
            slide["mermaid"] = diagram.group(1).strip()
            body = body.replace(diagram.group(0), "")
        code = re.search(r"```[a-z]*\n(.*?)```", body, flags=re.S)
        if code:
            slide["code"] = code.group(1).rstrip("\n")
            body = body.replace(code.group(0), "")
        for line in body.splitlines():
            s = line.strip()
            if not s:
                continue
            if s.startswith("layout:"):
                slide["layout"] = s.split(":", 1)[1].strip()
            elif s.startswith("來源："):
                slide["source"] = s
            elif s.startswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    slide["table"].append(cells)
            elif s.startswith("!["):
                slide["image"] = re.search(r"\((.*?)\)", s).group(1)
            elif s.startswith("- "):
                level = 1 if len(line) - len(line.lstrip(" ")) >= 2 else 0
                slide["bullets"].append((level, s[2:].strip()))
            else:
                slide["notes"].append(s)
        slides.append(slide)
    return meta, slides


# ---------------------------------------------------------------- pptx helpers


def style_run(run, size, bold=False, color=INK, font=FONT):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font
    rpr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {})
            rpr.append(el)
        el.set("typeface", font)


def textbox(slide, x, y, w, h, text, size, bold=False, color=INK, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, font=FONT):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        style_run(run, size, bold, color, font)
    return tb


def set_bullet(paragraph, level, size):
    ppr = paragraph._p.get_or_add_pPr()
    indent = int(Pt(size) * 1.1)
    ppr.set("marL", str(indent * (level + 1) + (Inches(0.1) if level else 0)))
    ppr.set("indent", str(-indent))
    for tag in ("a:buNone", "a:buChar", "a:buFont"):
        for el in ppr.findall(qn(tag)):
            ppr.remove(el)
    bu_font = ppr.makeelement(qn("a:buFont"), {"typeface": "Arial"})
    bu_char = ppr.makeelement(qn("a:buChar"), {"char": "•" if level == 0 else "–"})
    ppr.append(bu_font)
    ppr.append(bu_char)


def add_title(slide, title, page, total, footer):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, LEFT, Inches(0.55), Inches(0.09), Inches(0.62))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()
    textbox(slide, LEFT + Inches(0.25), Inches(0.45), W - LEFT - RIGHT - Inches(0.25), Inches(0.85),
            title, 30, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, LEFT, Inches(1.32), W - LEFT - RIGHT, Emu(9525))
    rule.fill.solid()
    rule.fill.fore_color.rgb = ACCENT_SOFT
    rule.line.fill.background()
    textbox(slide, LEFT, Inches(7.0), Inches(8), Inches(0.35), footer, 11, color=MUTED)
    textbox(slide, W - RIGHT - Inches(1.5), Inches(7.0), Inches(1.5), Inches(0.35),
            f"{page} / {total}", 11, color=MUTED, align=PP_ALIGN.RIGHT)


def add_source(slide, source):
    if source:
        textbox(slide, LEFT, Inches(6.55), W - LEFT - RIGHT, Inches(0.4), source, 11, color=MUTED)


def render_mermaid(slides, out_dir):
    """Render per-slide Mermaid blocks to PNG with mermaid-cli and a local Chrome."""
    import json
    chrome = next((p for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                               r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
                   if os.path.exists(p)), None)
    if chrome is None:
        sys.exit("Chrome not found; needed to render Mermaid diagrams")
    profile = os.path.join(out_dir, "chrome-profile")
    os.makedirs(profile, exist_ok=True)
    pconf = os.path.join(out_dir, "puppeteer.json")
    with open(pconf, "w", encoding="utf-8") as fh:
        json.dump({"executablePath": chrome, "headless": "new",
                   "args": ["--no-sandbox", "--disable-gpu", f"--user-data-dir={profile}"]}, fh)
    mconf = os.path.normpath(os.path.join(HERE, "..", "proposal_build", "mermaid.json"))
    env = dict(os.environ, PUPPETEER_SKIP_DOWNLOAD="true")
    for i, s in enumerate(slides, 1):
        if not s["mermaid"]:
            continue
        src = os.path.join(out_dir, f"diagram{i:02d}.mmd")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(s["mermaid"] + "\n")
        dst = src[:-4] + ".png"
        subprocess.run([shutil.which("npx") or "npx", "-y", "@mermaid-js/mermaid-cli@11.4.2", "-i", src,
                        "-o", dst, "-s", "3", "-b", "white", "-p", pconf, "-c", mconf],
                       check=True, env=env, cwd=out_dir, capture_output=True)
        s["image_path"] = dst


def add_bullets(slide, bullets, top, bottom):
    chars = sum(len(t) for _, t in bullets)
    size = 24 if chars < 220 else 22 if chars < 330 else 20
    tb = slide.shapes.add_textbox(LEFT, top, W - LEFT - RIGHT, bottom - top)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (level, text) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(10 if level == 0 else 4)
        p.line_spacing = 1.15
        set_bullet(p, level, size)
        quote = text.startswith("「")
        run = p.add_run()
        run.text = text
        style_run(run, size - 2 * level, bold=quote, color=ACCENT if quote else INK)


def add_table(slide, rows, top, bottom, note_lines):
    ncols = len(rows[0])
    lens = [max(len(r[c]) for r in rows) for c in range(ncols)]
    weights = [min(max(l, 6), 60) for l in lens]
    total_w = W - LEFT - RIGHT
    chars = sum(len(c) for r in rows for c in r)
    size = 18 if chars < 300 else 16 if chars < 520 else 14
    height = bottom - top - (Inches(0.7) if note_lines else 0)
    shape = slide.shapes.add_table(len(rows), ncols, LEFT, top, total_w, height)
    table = shape.table
    for c in range(ncols):
        table.columns[c].width = int(total_w * weights[c] / sum(weights))
    for r, row in enumerate(rows):
        table.rows[r].height = Inches(0.4)
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = ACCENT if r == 0 else (ROW_ALT if r % 2 == 0 else RGBColor(0xFF, 0xFF, 0xFF))
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = val
            style_run(run, size, bold=(r == 0 or c == 0),
                      color=RGBColor(0xFF, 0xFF, 0xFF) if r == 0 else INK)
    if note_lines:
        textbox(slide, LEFT, bottom - Inches(0.6), total_w, Inches(0.6), "\n".join(note_lines), 14,
                color=ACCENT)


def add_image(slide, path, top, bottom):
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    box_w, box_h = W - LEFT - RIGHT, bottom - top
    scale = min(box_w / iw, box_h / ih)
    w, h = int(iw * scale), int(ih * scale)
    slide.shapes.add_picture(path, int((W - w) / 2), top, w, h)


def add_code(slide, code, top, bottom):
    lines = code.splitlines()
    size = 20 if len(lines) <= 12 else 17 if len(lines) <= 15 else 15
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, LEFT, top, W - LEFT - RIGHT, bottom - top)
    box.fill.solid()
    box.fill.fore_color.rgb = CODE_BG
    box.line.color.rgb = ACCENT_SOFT
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_top = Inches(0.25)
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.05
        run = p.add_run()
        run.text = line
        style_run(run, size, bold=(i == 0), color=INK, font=CODE_FONT)


def add_title_slide(slide, s, meta):
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.9), W, Inches(1.6))
    band.fill.solid()
    band.fill.fore_color.rgb = ACCENT
    band.line.fill.background()
    textbox(slide, LEFT, Inches(1.9), W - LEFT - RIGHT, Inches(1.2), meta.get("title", s["title"]), 40,
            bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    textbox(slide, LEFT, Inches(3.2), W - LEFT - RIGHT, Inches(0.8), meta.get("subtitle", ""), 22,
            color=MUTED, align=PP_ALIGN.CENTER)
    textbox(slide, LEFT, Inches(6.35), W - LEFT - RIGHT, Inches(0.7), meta.get("footer", ""), 20,
            color=RGBColor(0xFF, 0xFF, 0xFF), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def build_pptx(meta, slides, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    blank = prs.slide_layouts[6]
    for i, s in enumerate(slides, 1):
        slide = prs.slides.add_slide(blank)
        if s["layout"] == "title":
            add_title_slide(slide, s, meta)
        else:
            add_title(slide, s["title"], i, len(slides), meta.get("footer", ""))
            bottom = CONTENT_BOTTOM if s["source"] else Inches(6.85)
            if s["layout"] == "figure" and (s.get("image_path") or s["image"]):
                add_image(slide, s.get("image_path") or os.path.join(PROPOSAL, s["image"]), CONTENT_TOP, bottom)
            elif s["layout"] == "table" and s["table"]:
                add_table(slide, s["table"], CONTENT_TOP, bottom, s["notes"])
            elif s["layout"] == "code" and s["code"]:
                add_code(slide, s["code"], CONTENT_TOP, bottom)
            else:
                add_bullets(slide, s["bullets"], CONTENT_TOP, bottom)
            add_source(slide, s["source"])
        slide.notes_slide.notes_text_frame.text = s["script"]
    prs.save(path)


def export_pngs(pptx_path, out_dir):
    script = (
        "$p = New-Object -ComObject PowerPoint.Application; "
        f"$d = $p.Presentations.Open('{pptx_path}', $true, $false, $false); "
        "try { $i = 0; foreach ($s in $d.Slides) { $i++; "
        f"$s.Export(('{out_dir}\\slide{{0:D2}}.png' -f $i), 'PNG', 1920, 1080) }}; 'slides: ' + $i }} "
        "finally { $d.Close(); $p.Quit() }"
    )
    out = subprocess.run(["powershell", "-NoProfile", "-Command", script], check=True,
                         capture_output=True, text=True)
    print(out.stdout.strip())


# ---------------------------------------------------------------- audio and video

LEAD, TAIL = 0.4, 0.7  # seconds of silence before and after each slide's narration


async def tts(text, voice, path):
    await edge_tts.Communicate(text, voice).save(path)


def duration(ffmpeg, path):
    err = subprocess.run([ffmpeg, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def chunks(script, limit=22):
    """Split narration into subtitle lines at punctuation, each at most `limit` characters."""
    parts = re.findall(r"[^。！？；，、：]+[。！？；，、：]?", script.replace("\n", ""))
    out, cur = [], ""
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if cur and len(cur) + len(p) > limit:
            out.append(cur)
            cur = p
        else:
            cur += p
        while len(cur) > limit:
            out.append(cur[:limit])
            cur = cur[limit:]
    if cur:
        out.append(cur)
    return [c.rstrip("，、：；") for c in out]


def ts(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def build_video(slides, voice, out_dir, mp4_path, srt_path):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    segs, srt, offset, n = [], [], 0.0, 1
    for i, s in enumerate(slides, 1):
        audio = os.path.join(out_dir, f"slide{i:02d}.mp3")
        asyncio.run(tts(s["script"], voice, audio))
        dur = duration(ffmpeg, audio)
        seg_len = LEAD + dur + TAIL
        lines = chunks(s["script"])
        weights = [len(c) for c in lines]
        t = offset + LEAD
        for c, w in zip(lines, weights):
            span = dur * w / sum(weights)
            srt.append(f"{n}\n{ts(t)} --> {ts(t + span)}\n{c}\n")
            n += 1
            t += span
        seg = os.path.join(out_dir, f"seg{i:02d}.mp4")
        subprocess.run([
            ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-loop", "1",
            "-i", os.path.join(out_dir, f"slide{i:02d}.png"), "-i", audio,
            "-filter_complex",
            f"[0:v]scale=1600:900,pad=1920:1080:160:0:color=0x1C2420,format=yuv420p[v];"
            f"[1:a]adelay={int(LEAD * 1000)}:all=1,apad[a]",
            "-map", "[v]", "-map", "[a]", "-t", f"{seg_len:.3f}", "-r", "30",
            "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", seg,
        ], check=True)
        segs.append(seg)
        offset += seg_len
        print(f"slide {i:2d}: narration {dur:5.1f}s")
    with open(srt_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(srt))
    listfile = os.path.join(out_dir, "segments.txt")
    with open(listfile, "w", encoding="utf-8") as fh:
        fh.writelines(f"file '{os.path.basename(p)}'\n" for p in segs)
    joined = os.path.join(out_dir, "joined.mp4")
    subprocess.run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", "segments.txt", "-c", "copy", "joined.mp4"], check=True, cwd=out_dir)
    shutil.copy2(srt_path, os.path.join(out_dir, "subs.srt"))
    style = ("FontName=Microsoft JhengHei,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
             "BorderStyle=1,Outline=1,Shadow=0,Alignment=2,MarginV=8")
    subprocess.run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", "joined.mp4",
                    "-vf", f"subtitles=subs.srt:force_style='{style}'",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "copy",
                    "final.mp4"], check=True, cwd=out_dir)
    shutil.copy2(os.path.join(out_dir, "final.mp4"), mp4_path)
    print(f"video length {offset / 60:.1f} min")


def main():
    pptx_only = "--pptx-only" in sys.argv
    if os.path.isdir(OUT):
        shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    meta, slides = parse(SRC)
    render_mermaid(slides, OUT)
    pptx_path = os.path.join(PROPOSAL, "proposal-slides.pptx")
    build_pptx(meta, slides, pptx_path)
    export_pngs(pptx_path, OUT)
    print("wrote", pptx_path)
    if pptx_only:
        return
    build_video(slides, meta.get("voice", "zh-TW-HsiaoChenNeural"), OUT,
                os.path.join(PROPOSAL, "proposal-video.mp4"), os.path.join(PROPOSAL, "proposal-video.srt"))
    print("wrote", os.path.join(PROPOSAL, "proposal-video.mp4"))


if __name__ == "__main__":
    main()
