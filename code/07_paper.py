"""Step 7: the paper. Fills code/paper_template.tex from data/results.json, adds tables, compiles with xelatex.
Output: release/paper/Hotham_Avon_Means_River.pdf and .tex beside the f_*.png figures.
The DOI stays a placeholder: the publisher reruns  DOI=10.5281/zenodo.N python3 code/07_paper.py  then 08_release.py."""
import subprocess
from common import *

R = jload(f"{DATA}/results.json")
OUT = os.path.join(ROOT, "release", "paper"); NAME = "Hotham_Avon_Means_River"
tex = lambda s: str(s).replace("\\", "").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#").replace("$", "\\$")


def tfmt(v, f):
    if f == "int": return f"{int(round(float(v))):,}"
    if f == "pc": return f"{round(float(v))}\\%"
    if f == "f1": return f"{float(v):.1f}"
    if f == "f2": return f"{float(v):.2f}"
    return tex(str(v))


import pandas as pd
MR = pd.read_csv(f"{DATA}/major_rivers_england.csv", keep_default_na=False)
OL = {"pre": "Brittonic or older", "english": "English", "uncertain": "uncertain"}
rows = "".join(f"{r['rank']} & {tex(r.river.title())} & {r.extent_km:.0f} & {OL[r.origin]} & {tex(r.note)}\\\\\n" for _, r in MR.iterrows())
TM = ("\\begin{small}\\begin{longtable}{rlrlp{6.6cm}}\\caption{The 60 largest English rivers in the data, by the spread of their mapped course (km, a proxy for size), "
      "and the origin of the name after Ekwall (1928) and Watts (2004).}\\label{tab:major}\\\\\\toprule Rank & River & Spread & Origin & Note\\\\\\midrule\\endhead\n" + rows + "\\bottomrule\\end{longtable}\\end{small}")
rows = "".join(f"{tex(v['label'])} & {tex(v['meaning'])} & {v['certainty']} & {v['rivers']}\\\\\n" for k, v in R["roots"].items())
TR = ("\\begin{table}[tbp]\\centering\\small\\caption{Root groups, the meaning given in the literature, the reading, and the number of distinct rivers and streams "
      "in the UK data.}\\label{tab:roots}\\begin{tabular}{p{4.2cm}p{6.6cm}lr}\\toprule Names & Root and meaning & Reading & Rivers\\\\\\midrule\n" + rows + "\\bottomrule\\end{tabular}\\end{table}")
t = open(os.path.join(ROOT, "code", "paper_template.tex"), encoding="utf-8").read()
t = t.replace("\\begin{document}", "\\newcolumntype{R}[1]{>{\\raggedright\\arraybackslash}p{#1}}\n\\begin{document}").replace("{{AI}}", AI).replace("{{TABLE_MAJOR}}", TM).replace("{{TABLE_ROOTS}}", TR)
t = re.sub(r"\{\{(?!TABLE_|DOI)([^}|]+)(\|(\w+))?\}\}", lambda m: tfmt(get(R, m.group(1)), m.group(3) or "raw"), t)
DOI = os.environ.get("DOI")
t = t.replace("https://doi.org/10.5281/zenodo.24063209", f"\\url{{https://doi.org/{DOI}}}" if DOI else "\\{\\{DOI\\_URL\\}\\}")
assert "{{" not in t and "--" not in t and "—" not in t and "–" not in t
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, NAME + ".tex"), "w", encoding="utf-8").write(t)
for _ in range(2):
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", NAME + ".tex"], cwd=OUT, capture_output=True, text=True)
log = open(os.path.join(OUT, NAME + ".log"), encoding="utf-8", errors="ignore").read()
print([l for l in log.splitlines() if "Missing character" in l or "undefined" in l.lower() or "Overfull" in l][:12])
for ext in (".aux", ".log", ".out", ".bbl", ".blg"):
    q = os.path.join(OUT, NAME + ext)
    if os.path.exists(q): os.remove(q)
txt = subprocess.run(["pdftotext", os.path.join(OUT, NAME + ".pdf"), "-"], capture_output=True, text=True).stdout
pages = subprocess.run(["pdfinfo", os.path.join(OUT, NAME + ".pdf")], capture_output=True, text=True).stdout
print("paper", r.returncode, len(txt.split()), "words;", [l for l in pages.splitlines() if l.startswith("Pages")], "dashes:", txt.count("—") + txt.count("–") + txt.count("--"))
