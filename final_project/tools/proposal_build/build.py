"""Rebuild doc/proposal/proposal.docx and proposal.pdf from the Markdown sections.

Usage (from any directory): python -I build.py
The Markdown sections are the source of truth; edits made directly in the .docx are overwritten.
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROPOSAL = os.path.normpath(os.path.join(HERE, "..", "..", "doc", "proposal"))
OUT = os.path.join(HERE, ".out")
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

sys.path.insert(0, HERE)
import assemble  # noqa: E402
import make_docx  # noqa: E402


def render_figures():
    chrome = next((p for p in CHROME_CANDIDATES if os.path.exists(p)), None)
    if chrome is None:
        sys.exit("Chrome not found; install it or edit CHROME_CANDIDATES in build.py")
    profile = os.path.join(OUT, "chrome-profile")
    os.makedirs(profile, exist_ok=True)
    pconf = os.path.join(OUT, "puppeteer.json")
    with open(pconf, "w", encoding="utf-8") as fh:
        json.dump({"executablePath": chrome, "headless": "new",
                   "args": ["--no-sandbox", "--disable-gpu", f"--user-data-dir={profile}"]}, fh)
    env = dict(os.environ, PUPPETEER_SKIP_DOWNLOAD="true")
    npx = shutil.which("npx") or "npx"
    for name in sorted(f for f in os.listdir(OUT) if f.startswith("fig") and f.endswith(".mmd")):
        src = os.path.join(OUT, name)
        dst = src[:-4] + ".png"
        subprocess.run([npx, "-y", "@mermaid-js/mermaid-cli@11.4.2", "-i", src, "-o", dst, "-s", "2",
                        "-b", "white", "-p", pconf, "-c", os.path.join(HERE, "mermaid.json")],
                       check=True, env=env, cwd=OUT)


def export_pdf(docx, pdf):
    # Word refreshes the table-of-contents field and prints the PDF
    script = (
        "$w = New-Object -ComObject Word.Application; $w.Visible = $false; "
        f"try {{ $d = $w.Documents.Open('{docx}'); "
        "foreach ($t in $d.TablesOfContents) { $t.Update() }; $d.Save(); "
        f"$d.SaveAs2('{pdf}', 17); 'pages: ' + $d.ComputeStatistics(2); $d.Close() }} "
        "finally { $w.Quit() }"
    )
    out = subprocess.run(["powershell", "-NoProfile", "-Command", script],
                         check=True, capture_output=True, text=True)
    print(out.stdout.strip())


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    assemble.main(PROPOSAL, OUT)
    render_figures()
    docx = os.path.join(OUT, "proposal.docx")
    make_docx.main(OUT, docx)
    pdf = os.path.join(OUT, "proposal.pdf")
    export_pdf(docx, pdf)

    figdir = os.path.join(PROPOSAL, "figures")
    os.makedirs(figdir, exist_ok=True)
    for f in os.listdir(OUT):
        if f.startswith("fig") and (f.endswith(".png") or f.endswith(".mmd")):
            shutil.copy2(os.path.join(OUT, f), figdir)
    shutil.copy2(docx, os.path.join(PROPOSAL, "proposal.docx"))
    shutil.copy2(pdf, os.path.join(PROPOSAL, "proposal.pdf"))
    print("updated", PROPOSAL)


if __name__ == "__main__":
    main()
