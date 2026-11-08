"""Reddit collage (r/dataisbeautiful style) and the 1200 x 630 header card.
Light parchment background; labels on the sea; full legend; source footer.
Output: reddit/river_names_collage.png (3000 x 2100 px) and header.png. Run after code/05_figures.py."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code"))
import pandas as pd
import matplotlib.patheffects as pe
from figstyle import *
from generics import GENERICS, GLAB

R = jload(f"{DATA}/results.json")
GR = pd.read_csv(f"{DATA}/generic_grid.csv")
MR = pd.read_csv(f"{DATA}/major_rivers_england.csv")
GCOL = {"brook": "#A3261B", "beck": "#1F5F8B", "burn": "#5E8F2E", "bourne": "#D07A2A", "water": "#6FA7C9", "gill": "#6B3E8E", "sike": "#8E8E3A",
        "dyke": "#7A6A52", "rhyne": "#C2577A", "lode": "#B8862B", "allt": "#2E9C9A", "abhainn": "#164B57", "nant": "#C94F3A", "afon": "#7A1F14"}
LANG = {g[0]: g[2] for g in GENERICS}
OC = {"pre": "#2F7F4A", "english": "#A3261B", "uncertain": "#B9AC8E"}
HALO = [pe.withStroke(linewidth=3, foreground=PAPER)]
OUT = os.path.join(ROOT, "reddit", "river_names_collage.png")
M, D = R["major"], R["danelaw"]


def gridmap(ax, ext_ll=(-8.4, 1.9, 49.85, 59.0)):
    ext, f = ink_base(ax, 27700, ext_ll, coast_lw=0.5, ripple_m=(6e3, 15e3), countries=False, min_area=2e7)
    for r in GR.itertuples():
        ax.add_patch(plt.Rectangle((r.E0, r.N0), 25000, 25000, fc=GCOL[r.top], ec=PAPER, lw=0.3, alpha=0.35 + 0.6 * min(1, r.top_n / r.n), zorder=3.5))
    ax.set_xlim(ext[0] + 0.6e5, ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_facecolor("none")
    return ext, f


fig = plt.figure(figsize=(10, 7), dpi=300); parchment(fig, seed=8)
fig.text(0.035, 0.955, "Avon means river", fontproperties=HAND, fontsize=31, color=RED, va="center")
fig.text(0.035, 0.912, f"{R['n']['watercourses']:,} named rivers and streams in the UK, by the words in their names", fontproperties=FELL, fontsize=12, color=INKC, va="center")
fig.text(0.035, 0.885, "Avon is Brittonic for 'river' (Welsh afon): Stratford-upon-Avon stands on the River River.", fontproperties=FELL, fontsize=10, color=MUT, va="center")
ax = fig.add_axes([0.0, 0.05, 0.47, 0.81])
ext, f = gridmap(ax)
for txt, lon, lat in [("allt: Gaelic", -8.3, 58.75), ("burn", -0.6, 56.9), ("beck: Old Norse", 0.6, 54.75), ("brook", 1.85, 52.35), ("nant: Welsh", -6.4, 52.55)]:
    x, y = f(lon, lat)
    ax.text(x, y, txt, fontproperties=FELLIT, fontsize=10.5, color=INKC, path_effects=HALO, zorder=9)
lx = fig.add_axes([0.46, 0.25, 0.15, 0.61]); lx.axis("off")
lx.text(0, 1.0, "Commonest stream word,\nper 25 km square", fontproperties=FELLSC, fontsize=10, color=RED, va="top")
order = ["allt", "abhainn", "burn", "water", "beck", "gill", "sike", "dyke", "brook", "lode", "rhyne", "nant", "afon"]
for i, k in enumerate(order):
    y = 0.90 - i * 0.068
    lx.add_patch(plt.Rectangle((0, y - 0.02), 0.1, 0.036, fc=GCOL[k], ec=INKC, lw=0.4, transform=lx.transAxes))
    lx.text(0.14, y + 0.008, f"{GLAB[k]}", fontproperties=FELL, fontsize=9, color=INKC, va="center", transform=lx.transAxes)
    lx.text(0.14, y - 0.024, LANG[k], fontproperties=FELLIT, fontsize=6.6, color=MUT, va="center", transform=lx.transAxes)

# ---- 60 biggest rivers
fig.text(0.64, 0.86, "England's 60 biggest mapped rivers", fontproperties=FELLSC, fontsize=12, color=RED)
fig.text(0.64, 0.84, f"{M['pre']} kept names older than English; only {M['english']} are English", fontproperties=FELL, fontsize=9, color=MUT)
wx = fig.add_axes([0.64, 0.47, 0.33, 0.36]); wx.axis("off"); wx.set_xlim(0, 6); wx.set_ylim(0, 10.6)
for i, r in MR.iterrows():
    c, rr = i % 6, i // 6
    wx.add_patch(plt.Rectangle((c + 0.04, 9.6 - rr), 0.92, 0.86, fc=OC[r.origin], ec=INKC, lw=0.3))
    wx.text(c + 0.5, 10.03 - rr, r.river.title(), ha="center", va="center", fontproperties=FELL, fontsize=6.6, color=PAPER if r.origin != "uncertain" else INKC)
for i, (k, l) in enumerate([("pre", "Brittonic or older"), ("english", "English"), ("uncertain", "debated")]):
    fig.patches.append(plt.Rectangle((0.64 + i * 0.11, 0.445), 0.014, 0.014, fc=OC[k], ec=INKC, lw=0.3, transform=fig.transFigure, figure=fig))
    fig.text(0.658 + i * 0.11, 0.452, l, fontproperties=FELL, fontsize=8.5, color=INKC, va="center")
fig.text(0.64, 0.415, f"Meanwhile {R['towns']['english_pc']:.0f}% of England's towns end in an English or Norse word", fontproperties=FELL, fontsize=8.6, color=INKC)

# ---- the beck line
bx = fig.add_axes([0.645, 0.10, 0.15, 0.22])
vals = [D["east"]["beck_pc"], D["mid"]["beck_pc"], D["west"]["beck_pc"]]
bx.bar([0, 1, 2], vals, color=[GCOL["beck"], GCOL["brook"], GCOL["brook"]], edgecolor=INKC, lw=0.4, width=0.6)
for i, v in enumerate(vals):
    bx.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontproperties=FELL, fontsize=10, color=INKC)
bx.set_xticks([0, 1, 2]); bx.set_xticklabels(["A", "B", "C"], fontproperties=FELL, fontsize=9)
bx.set_yticks([]); bx.set_ylim(0, max(vals) + 10)
for s in ("top", "right", "left"): bx.spines[s].set_visible(False)
fig.text(0.64, 0.37, "The beck line", fontproperties=FELLSC, fontsize=12, color=RED)
fig.text(0.64, 0.35, "Becks among beck and brook names at similar latitudes:", fontproperties=FELL, fontsize=8.8, color=MUT)
fig.text(0.81, 0.29, f"A: Lincolnshire, Nottinghamshire\n({D['east']['beck']} becks, {D['east']['brook']} brooks)", fontproperties=FELL, fontsize=8.5, color=INKC, va="top")
fig.text(0.81, 0.225, f"B: Derbyshire, Leicestershire, also\nold Danelaw ({D['mid']['beck']} becks, {D['mid']['brook']} brooks)", fontproperties=FELL, fontsize=8.5, color=INKC, va="top")
fig.text(0.81, 0.16, f"C: Cheshire, Staffs, Shropshire,\nGreater Manchester: not one\nbeck in {D['west']['brook']} brooks", fontproperties=FELL, fontsize=8.5, color=INKC, va="top")
fig.text(0.035, 0.034, "Data: OpenStreetMap contributors (ODbL), via QLever. Etymologies: Ekwall, English River-Names (1928); Watts (2004); Mills (2011).", fontproperties=FELL, fontsize=7.4, color=MUT)
fig.text(0.035, 0.014, f"Avons: {R['avon_rivers']}. Esks: {R['esk_rivers']}. Calders: {R['calder_rivers']}. Rivers ranked by the spread of their mapped course.", fontproperties=FELL, fontsize=7.4, color=MUT)
fig.text(0.965, 0.018, "maps.tristanhotham.com/river-names", fontproperties=FELL, fontsize=8, color=RED, ha="right")
fig.savefig(OUT, dpi=300, facecolor=fig.get_facecolor())
plt.close(fig)

fig = plt.figure(figsize=(12, 6.3), dpi=100); parchment(fig, seed=4)
ax = fig.add_axes([0.55, 0.0, 0.45, 1.0])
gridmap(ax)
fig.text(0.05, 0.76, "Avon", fontproperties=HAND, fontsize=60, color=RED, va="center")
fig.text(0.05, 0.60, "means river", fontproperties=FELL, fontsize=44, color=INKC, va="center")
fig.text(0.05, 0.44, f"{M['pre']} of England's 60 biggest rivers", fontproperties=FELL, fontsize=19, color=INKC)
fig.text(0.05, 0.38, "kept names older than English", fontproperties=FELL, fontsize=19, color=INKC)
fig.text(0.05, 0.28, "burn, beck, brook, allt and nant", fontproperties=FELLIT, fontsize=17, color=MUT)
fig.text(0.05, 0.08, "Dr Tristan Hotham · maps.tristanhotham.com", fontproperties=FELL, fontsize=13, color=MUT)
fig.savefig(os.path.join(ROOT, "header.png"), dpi=100, facecolor=fig.get_facecolor())
plt.close(fig)
from PIL import Image
print(Image.open(OUT).size, Image.open(os.path.join(ROOT, "header.png")).size)
