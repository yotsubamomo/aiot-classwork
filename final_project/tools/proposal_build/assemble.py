"""Assemble the proposal sections into one Markdown file with a unified reference list.

Usage: python -I assemble.py <proposal_dir> <out_dir>
Writes <out_dir>/proposal-full.md, <out_dir>/fig*.mmd and prints a citation mapping report.
"""
import os
import re
import sys

SECTIONS = [  # (file, family used for bare [n] citations)
    ("00-abstract.md", None),
    ("01-introduction.md", None),
    ("02-related-work.md", "R"),
    ("03-deep-research.md", None),
    ("04-proposed-scheme.md", "R"),
]
REF_FILES = {"01-introduction.md": "I", "02-related-work.md": "R", "03-deep-research.md": "D"}
# same work cited under different URLs in different drafts
MANUAL_ALIASES = [(("D", "4"), ("R", "11")), (("D", "16"), ("R", "5")), (("I", "8"), ("R", "11"))]
PREFER = {"R": 0, "I": 1, "D": 2}
CITE = re.compile(r"\[(I\d+|D\d+|\d+)\]")
RANGE = re.compile(r"\[(I|D)?(\d+)\][–-]\[(I|D)?(\d+)\]")


def parse_refs(text, fam):
    refs = {}
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"^(?:-\s*)?((?:\[(?:I|D)?\d+\])+)\s*(.+)$", line)
        if not m:
            continue
        keys = re.findall(r"\[(?:I|D)?(\d+)\]", m.group(1))
        for k in keys:
            refs[(fam, k)] = m.group(2).strip()
    return refs


def canon_keys(text):
    keys = set()
    for aid in re.findall(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})", text):
        keys.add("arxiv:" + aid)
    for doi in re.findall(r"10\.\d{4,9}/[^\s,，)）]+", text):
        keys.add("doi:" + doi.lower().rstrip(".;"))
    for url in re.findall(r"https?://[^\s，；)）]+", text):
        u = url.lower().rstrip(".;/")
        u = re.sub(r"^https?://(www\.)?", "", u)
        if "arxiv.org" in u:
            continue
        keys.add("url:" + u)
    return keys


def split_sections(md):
    """Return (body, references_text) after removing verification tables and the draft note."""
    lines = md.splitlines()
    out, skip, refs, in_refs = [], False, [], False
    seen_heading = False
    for line in lines:
        if line.startswith("## References"):
            in_refs = True
            continue
        if in_refs:
            refs.append(line)
            continue
        if line.startswith("## "):
            seen_heading = True
            skip = line.startswith("## 證據查證表") or line.startswith("## 查證紀錄")
            if skip:
                continue
        if skip:
            continue
        if not seen_heading and line.startswith(">"):
            continue
        out.append(line)
    return "\n".join(out).strip() + "\n", "\n".join(refs)


def expand_ranges(text):
    def rep(m):
        fam = m.group(1) or ""
        a, b = int(m.group(2)), int(m.group(4))
        if b <= a or b - a > 20:
            return m.group(0)
        return "".join(f"[{fam}{i}]" for i in range(a, b + 1))
    return RANGE.sub(rep, text)


def main(src, out):
    raw = {f: open(os.path.join(src, f), encoding="utf-8").read() for f, _ in SECTIONS}
    bodies, refs = {}, {}
    for f, _ in SECTIONS:
        body, reftext = split_sections(raw[f])
        bodies[f] = expand_ranges(body)
        if f in REF_FILES:
            refs.update(parse_refs(reftext, REF_FILES[f]))

    # union-find over references that share a canonical key
    parent = {k: k for k in refs}

    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    owner = {}
    for k, text in refs.items():
        for ck in canon_keys(text):
            if ck in owner:
                union(owner[ck], k)
            else:
                owner[ck] = k
    for a, b in MANUAL_ALIASES:
        if a in refs and b in refs:
            union(a, b)

    groups = {}
    for k in refs:
        groups.setdefault(find(k), []).append(k)

    def best_text(members):
        return refs[sorted(members, key=lambda k: (PREFER[k[0]], int(k[1])))[0]]

    # number by first citation in document order
    number, ordered = {}, []
    missing = set()
    for f, fam in SECTIONS:
        for tok in CITE.findall(bodies[f]):
            key = (tok[0], tok[1:]) if tok[0] in "ID" else (fam, tok)
            if key not in refs:
                missing.add((f, tok))
                continue
            root = find(key)
            if root not in number:
                number[root] = len(ordered) + 1
                ordered.append(root)

    def renumber(text, fam):
        def rep(m):
            tok = m.group(1)
            key = (tok[0], tok[1:]) if tok[0] in "ID" else (fam, tok)
            if key not in refs:
                return m.group(0)
            return f"[{number[find(key)]}]"
        text = CITE.sub(rep, text)
        # compress runs like [3][4][5] into [3]–[5]
        def comp(m):
            nums = [int(x) for x in re.findall(r"\d+", m.group(0))]
            nums = sorted(set(nums))
            parts, i = [], 0
            while i < len(nums):
                j = i
                while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                    j += 1
                parts.append(f"[{nums[i]}]–[{nums[j]}]" if j - i >= 2 else "".join(f"[{n}]" for n in nums[i:j + 1]))
                i = j + 1
            return "".join(parts)
        return re.sub(r"(?:\[\d+\]){2,}", comp, text)

    figs = []

    def mermaid(text):
        def rep(m):
            figs.append(m.group(1).strip())
            n = len(figs)
            cap = {1: "系統架構（依作業規範 ①–⑧ 模組編號）", 2: "處理流程"}.get(n, f"圖 {n}")
            width = {1: "16cm", 2: "15cm"}.get(n, "16cm")
            return f"![圖 {n}　{cap}](fig{n}.png){{width={width}}}"
        return re.sub(r"```mermaid\n(.*?)```", rep, text, flags=re.S)

    def headings(text, f):
        if f == "01-introduction.md":
            n = iter(range(1, 20))
            text = re.sub(r"^## ([A-F]\. )", lambda m: f"## 1.{next(n)} {m.group(1)}", text, flags=re.M)
        if f == "03-deep-research.md":
            text = re.sub(r"^## Q(\d)\. ", lambda m: f"## 3.{m.group(1)} Q{m.group(1)}. ", text, flags=re.M)
        return text

    parts = []
    for f, fam in SECTIONS:
        body = renumber(bodies[f], fam)
        body = headings(mermaid(body), f)
        parts.append(body)

    reflist = ["# 參考文獻 References", ""]
    for i, root in enumerate(ordered, 1):
        reflist.append(f"[{i}] {best_text(groups[root])}")
        reflist.append("")
    # cover page fields live next to the sections so they can be edited without touching code
    with open(os.path.join(src, "metadata.yaml"), encoding="utf-8") as fh:
        meta = fh.read().strip() + "\n\n"
    full = meta + "\n\n".join(parts) + "\n\n" + "\n".join(reflist)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "proposal-full.md"), "w", encoding="utf-8") as fh:
        fh.write(full)
    for i, code in enumerate(figs, 1):
        with open(os.path.join(out, f"fig{i}.mmd"), "w", encoding="utf-8") as fh:
            fh.write(code + "\n")

    print("references total in drafts:", len(refs), "| unique works:", len(groups), "| cited:", len(ordered))
    uncited = [sorted(g) for r, g in groups.items() if r not in number]
    print("uncited works (dropped from list):", uncited)
    print("unresolved citations:", sorted(missing))
    merged = [sorted(g) for g in groups.values() if len(g) > 1]
    print("merged duplicates:", merged)
    print("figures:", len(figs))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
