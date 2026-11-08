"""Step 6: index.html from code/page_template.html, filled from data/results.json, with the facts stated in words checked.
10.5281/zenodo.24063209, https://doi.org/10.5281/zenodo.24063209 and https://blog.tristanhotham.com/2026/10/31/river-names/ stay as placeholders for the publisher."""
import time
import pandas as pd
from common import *
from generics import GENERICS
from roots import ROOTS

R = jload(f"{DATA}/results.json")
B = pd.read_csv(f"{DATA}/borrowed_names.csv")
for spec, place in [("exe", "Exeter"), ("dart", "Dartmouth"), ("dart", "Dartington"), ("aln", "Alnwick"), ("tyne", "Tynemouth"), ("don", "Doncaster"),
                    ("thame", "Thame"), ("frome", "Frome"), ("usk", "Usk")]:
    assert ((B.spec == spec) & (B.place == place)).any(), (spec, place)
M = R["major"]
assert {"Arun", "Rother", "Mole", "Lark", "Mersey", "Waveney", "Cherwell"} <= set(M["english_list"])
assert {"Thames", "Trent", "Severn", "Avon", "Derwent", "Exe", "Tamar", "Tees", "Tyne"} <= {r.title() for r in pd.read_csv(f"{DATA}/major_rivers_england.csv").query("origin == 'pre'").river} | {"Ouse"}
assert M["pre"] > 30 and M["pre"] > 3 * M["english"]
assert R["scotland"]["gaelic_pc_Scottish_Borders"] == 0 and R["scotland"]["gaelic_pc_Dumfries_and_Galloway"] == 0       # "none at all"
assert R["beck_county"]["Cheshire"] == 0 and R["danelaw"]["mid"]["beck_pc"] < 2 and R["danelaw"]["east"]["beck_pc"] > 50  # "brook country"
assert R["danelaw"]["west"]["beck_pc"] == 0 and abs(R["danelaw"]["east_lat"] - R["danelaw"]["west_lat"]) < 0.4             # "much the same latitude"
assert R["southern"]["lode"] > 0 and R["southern"]["rhyne_somerset"] > 10
avl = " ".join(R["roots"]["avon"]["list"])
for nm in ("Warwickshire", "Bristol", "Salisbury", "Devon", "Speyside", "Falkirk"):
    assert nm in avl, nm
assert any("Cumbria" in x for x in R["roots"]["isca"]["list"]) and any("North Esk (Angus)" in x for x in R["roots"]["isca"]["list"])
CW = '<button class="chip" data-g="all" aria-pressed="true">All</button>' + "".join(
    f'<button class="chip" data-g="{k}" aria-pressed="false">{l}</button>' for k, l, *_ in GENERICS if k not in ("other", "river", "fleet"))
CR = '<button class="chip" data-r="all" aria-pressed="true">All</button>' + "".join(
    f'<button class="chip" data-r="{k}" aria-pressed="false">{l.split(", ")[0]}</button>' for k, l, *_ in ROOTS)
t = open(os.path.join(ROOT, "code", "page_template.html"), encoding="utf-8").read()
css = open(os.path.join(ROOT, "code", "page.css"), encoding="utf-8").read()
fs = open(os.path.join(ROOT, "code", "fullscreen_snippet.html"), encoding="utf-8").read()
t = t.replace("{{CSS}}", css).replace("{{CHIPS_WORDS}}", CW).replace("{{CHIPS_ROOTS}}", CR).replace("{{FULLSCREEN}}", fs)
t = t.replace("{{BYLINE}}", BYLINE).replace("{{AI}}", AI).replace("{{VERSION}}", time.strftime("%Y%m%d"))
t = fill(t, R)
assert set(re.findall(r"\{\{([^}]+)\}\}", t)) <= {"DOI", "DOI_URL", "BLOG_URL"}, set(re.findall(r"\{\{([^}]+)\}\}", t))
vis = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", "", t, flags=re.S)
for bad in ("—", "–", "--", "DSIT", "DCMS", "civil serv"):
    assert bad not in vis, bad
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(t)
js = open(os.path.join(ROOT, "js", "page.js"), encoding="utf-8").read()
assert "—" not in js and "–" not in js
print("index.html", len(t) // 1024, "KB")
