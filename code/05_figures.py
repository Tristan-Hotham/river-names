"""Step 5: figures for the page (img/*.jpg), the blog (release/blog/b_*.png, 1800 px), the paper (release/paper/f_*.png)."""
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib.patheffects as pe
from PIL import Image
from figstyle import *
from generics import GENERICS, GLAB
from roots import ROOTS

R = jload(f"{DATA}/results.json")
W = pd.read_csv(f"{DATA}/watercourses.csv", keep_default_na=False)
GR = pd.read_csv(f"{DATA}/generic_grid.csv")
RT = jload(f"{DATA}/rootpts.json")
MR = pd.read_csv(f"{DATA}/major_rivers_england.csv")
BLOG, PAPERD = f"{ROOT}/release/blog", f"{ROOT}/release/paper"
for d in (BLOG, PAPERD):
    os.makedirs(d, exist_ok=True)
CRS = 27700
EXT = (-8.4, 1.9, 49.85, 59.0)
HALO = [pe.withStroke(linewidth=3, foreground=PAPER)]
GCOL = {"brook": "#A3261B", "beck": "#1F5F8B", "burn": "#5E8F2E", "bourne": "#D07A2A", "water": "#6FA7C9", "gill": "#6B3E8E", "sike": "#8E8E3A",
        "dyke": "#7A6A52", "rhyne": "#C2577A", "lode": "#B8862B", "allt": "#2E9C9A", "abhainn": "#164B57", "nant": "#C94F3A", "afon": "#7A1F14"}
RCOL = {"avon": "#A3261B", "isca": "#1F5F8B", "ouse": "#6FA7C9", "derwent": "#2F7F4A", "dee": "#6B3E8E", "don": "#8E5E9E", "tam": "#2B2119",
        "calder": "#B8862B", "leven": "#4E9A6E", "alaun": "#D07A2A", "frome": "#C2577A", "kennet": "#7A6A52", "colne": "#8E8E3A",
        "wye": "#3D6E9E", "trent": "#7A1F14", "severn": "#C94F3A"}


def out(fig, name, dpi=200):
    fig.savefig(f"{WORK}/{name}.png", dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    im = Image.open(f"{WORK}/{name}.png").convert("RGB")
    im.resize((1600, round(im.size[1] * 1600 / im.size[0])), Image.LANCZOS).save(f"{IMG}/{name}.jpg", quality=84, optimize=True)
    im.resize((1800, round(im.size[1] * 1800 / im.size[0])), Image.LANCZOS).save(f"{BLOG}/b_{name}.png", optimize=True)
    w = min(2000, im.size[0]); im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS).save(f"{PAPERD}/f_{name}.png", optimize=True)
    os.remove(f"{WORK}/{name}.png")


def base(ax, ext=EXT):
    return ink_base(ax, CRS, ext, ripple_m=(8e3, 20e3), coast_lw=0.6, countries=False, min_area=2e7)


# ---------- 1. the stream words: dominant generic in each 25 km square
fig = plt.figure(figsize=(10.5, 12.5)); parchment(fig)
ax = fig.add_axes([0.0, 0.03, 0.74, 0.87])
ext, f = base(ax)
for r in GR.itertuples():
    share = r.top_n / r.n
    ax.add_patch(plt.Rectangle((r.E0, r.N0), 25000, 25000, fc=GCOL[r.top], ec=PAPER, lw=0.4, alpha=0.35 + 0.6 * min(1, share), zorder=3.5))
ax.set_xlim(ext[0] + 0.6e5, ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_facecolor("none")
lx = fig.add_axes([0.72, 0.30, 0.27, 0.52]); lx.axis("off")
lx.text(0, 1.0, "Commonest word for a stream", fontproperties=FELLSC, fontsize=13, color=RED, va="top")
order = ["allt", "abhainn", "burn", "water", "beck", "gill", "sike", "dyke", "brook", "bourne", "lode", "rhyne", "nant", "afon"]
lang = {g[0]: g[2] for g in GENERICS}
for i, k in enumerate(order):
    y = 0.93 - i * 0.066
    lx.add_patch(plt.Rectangle((0, y - 0.022), 0.09, 0.044, fc=GCOL[k], ec=INKC, lw=0.4, transform=lx.transAxes))
    lx.text(0.13, y, f"{GLAB[k]}", fontproperties=FELL, fontsize=12.5, color=INKC, va="center", transform=lx.transAxes)
    lx.text(0.13, y - 0.027, lang[k], fontproperties=FELLIT, fontsize=9.5, color=MUT, va="center", transform=lx.transAxes)
lx.text(0, -0.03, "Paler squares: the leading word\nhas under half the names.", fontproperties=FELL, fontsize=10.5, color=MUT, va="top", transform=lx.transAxes)
fig.text(0.05, 0.958, "Burn, beck, brook, allt and nant", fontproperties=FELL, fontsize=25, color=INKC, va="center")
fig.text(0.05, 0.925, f"The commonest generic word in the names of {sum(R['generic_counts'][k] for k in order):,} streams and rivers, by 25 km square.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
fig.text(0.05, 0.012, "Names: OpenStreetMap waterways (ODbL). Squares with at least 5 named watercourses. Shetland not shown.", fontproperties=FELL, fontsize=10, color=MUT)
out(fig, "generics")

# ---------- 2. beck against brook: by latitude, and east against west
B = pd.DataFrame(R["beck_bands"])
fig = plt.figure(figsize=(12, 6.8)); parchment(fig)
ax = fig.add_axes([0.07, 0.13, 0.55, 0.68])
ax.fill_betweenx(B.lat, 0, B.beck_pc, color=GCOL["beck"], alpha=0.85, step="mid")
ax.fill_betweenx(B.lat, B.beck_pc, 100, color=GCOL["brook"], alpha=0.75, step="mid")
ax.axvline(50, color=INKC, lw=0.6, ls=(0, (2, 2)))
ax.set_xlim(0, 100); ax.set_ylim(B.lat.min() - 0.12, B.lat.max() + 0.12)
ax.set_xlabel("Share of beck among beck and brook names in England (%)", fontproperties=FELL, fontsize=12)
ax.set_ylabel("Latitude (°N)", fontproperties=FELL, fontsize=12)
ax.text(8, B.lat.max() - 0.2, "beck", fontproperties=FELLSC, fontsize=18, color=PAPER)
ax.text(70, B.lat.min() + 0.25, "brook", fontproperties=FELLSC, fontsize=18, color=PAPER)
for t in ax.get_xticklabels() + ax.get_yticklabels(): t.set_fontproperties(FELL); t.set_fontsize(11)
for s in ("top", "right"): ax.spines[s].set_visible(False)
bx = fig.add_axes([0.70, 0.18, 0.28, 0.55])
D = R["danelaw"]
vals = [D["east"]["beck_pc"], D["mid"]["beck_pc"], D["west"]["beck_pc"]]
bx.bar([0, 1, 2], vals, color=[GCOL["beck"], GCOL["brook"], GCOL["brook"]], edgecolor=INKC, lw=0.5, width=0.62)
for i, (v, k) in enumerate(zip(vals, ("east", "mid", "west"))):
    bx.text(i, v + 1.5, f"{v:.0f}%\n({D[k]['beck']} of {D[k]['beck'] + D[k]['brook']})", ha="center", fontproperties=FELL, fontsize=10.5, color=INKC)
bx.set_xticks([0, 1, 2]); bx.set_xticklabels(["Lincs,\nNotts", "Derbys,\nLeics", "Cheshire, Staffs,\nShrops, Gtr Manc."], fontproperties=FELL, fontsize=9.5)
bx.set_ylim(0, max(vals) + 22); bx.set_yticks([])
for s in ("top", "right", "left"): bx.spines[s].set_visible(False)
fig.text(0.70, 0.82, "At similar latitudes", fontproperties=FELLSC, fontsize=13, color=RED)
fig.text(0.70, 0.80, "beck's share; Lincs, Notts, Derbys\nand Leics were all in the Danelaw", fontproperties=FELL, fontsize=11, color=MUT, va="top")
fig.text(0.03, 0.94, "The beck line", fontproperties=FELL, fontsize=24, color=INKC, va="center")
fig.text(0.03, 0.895, f"Old Norse bekkr against Old English broc: north of about {R['beck_majority_from']:.2f}°N most English streams are becks.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
out(fig, "beck")

# ---------- 3. the old roots: every mapped stretch of the rivers in each root group
pts = pd.DataFrame(RT["pts"], columns=["lon", "lat", "root", "river"])
RK = [r[0] for r in ROOTS]
fig = plt.figure(figsize=(10.5, 12.5)); parchment(fig)
ax = fig.add_axes([0.0, 0.03, 0.74, 0.87])
ext, f = base(ax)
for k in RK[::-1]:
    s = pts[pts.root == RK.index(k)]
    x, y = f(s.lon.values, s.lat.values)
    ax.scatter(x, y, s=7, c=RCOL[k], edgecolors="none", alpha=0.9, zorder=6)
ax.set_xlim(ext[0] + 0.6e5, ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_facecolor("none")
lx = fig.add_axes([0.70, 0.22, 0.29, 0.62]); lx.axis("off")
lx.text(0, 1.0, "Root (rivers)", fontproperties=FELLSC, fontsize=13, color=RED, va="top")
for i, (k, lab, rx, mean, cert, note) in enumerate(ROOTS):
    y = 0.945 - i * 0.058
    lx.scatter([0.03], [y], s=50, c=RCOL[k], edgecolors=INKC, linewidths=0.4, transform=lx.transAxes)
    short = ", ".join(lab.split(", ")[:4]) + (", ..." if len(lab.split(", ")) > 4 else "")
    lx.text(0.09, y, f"{short} ({R['roots'][k]['rivers']})", fontproperties=FELL, fontsize=11.5, color=INKC, va="center", transform=lx.transAxes)
fig.text(0.05, 0.958, "The oldest words in the landscape", fontproperties=FELL, fontsize=25, color=INKC, va="center")
fig.text(0.05, 0.925, f"{R['root_rivers']} rivers and streams whose names share a Brittonic or older root, traced by their mapped stretches.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
fig.text(0.05, 0.012, "Roots after Ekwall (1928), Watts (2004) and Mills (2011). Each dot is the start of a mapped stretch of the river in OpenStreetMap.", fontproperties=FELL, fontsize=10, color=MUT)
out(fig, "roots")

# ---------- 4. the largest English rivers: origin of the name
OC = {"pre": "#2F7F4A", "english": "#A3261B", "uncertain": "#B9AC8E"}
OL = {"pre": "Brittonic or older", "english": "English (incl. back-formations)", "uncertain": "Uncertain or debated"}
fig = plt.figure(figsize=(12, 9.6)); parchment(fig)
ax = fig.add_axes([0.04, 0.08, 0.92, 0.74]); ax.axis("off")
for i, r in MR.iterrows():
    c, rr = i % 4, i // 4
    x, y = c * 0.25, 1 - rr * 0.066
    ax.add_patch(plt.Rectangle((x, y - 0.05), 0.235, 0.055, fc=OC[r.origin], ec=INKC, lw=0.4, alpha=0.9, transform=ax.transAxes))
    ax.text(x + 0.01, y - 0.0225, f"{r['rank']}. {r.river.title()}", fontproperties=FELL, fontsize=12, color=PAPER if r.origin != "uncertain" else INKC,
            va="center", transform=ax.transAxes)
M = R["major"]
fig.text(0.04, 0.95, "England's big rivers kept their old names", fontproperties=FELL, fontsize=24, color=INKC, va="center")
fig.text(0.04, 0.91, f"The 60 largest English rivers in the data, by the spread of their mapped course: {M['pre']} have Brittonic or older names, {M['english']} English ones.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
fig.text(0.04, 0.88, f"Meanwhile {R['towns']['english_pc']:.0f}% of England's towns end in an English or Norse word such as -ton, -ham, -by or -ford.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
for i, k in enumerate(("pre", "english", "uncertain")):
    fig.patches.append(plt.Rectangle((0.04 + i * 0.3, 0.035), 0.025, 0.022, fc=OC[k], ec=INKC, lw=0.4, transform=fig.transFigure, figure=fig))
    fig.text(0.072 + i * 0.3, 0.046, f"{OL[k]} ({M[k]})", fontproperties=FELL, fontsize=12, color=INKC, va="center")
out(fig, "major")

# ---------- 5. Avons, Esks, Derwents and Calders
fig = plt.figure(figsize=(13, 8.6)); parchment(fig)
show = [("avon", "Avon: 'river'"), ("isca", "Esk, Exe, Axe, Usk: 'water'"), ("derwent", "Derwent and Dart: 'oak'"), ("calder", "Calder: 'hard water'")]
for k, (key, title) in enumerate(show):
    ax = fig.add_axes([0.01 + k * 0.247, 0.05, 0.24, 0.76])
    e2, f2 = base(ax)
    s = pts[pts.root == RK.index(key)]
    x, y = f2(s.lon.values, s.lat.values)
    ax.scatter(x, y, s=10, c=RCOL[key], edgecolors="none", zorder=6)
    ax.set_xlim(e2[0] + 1.3e5, e2[1] - 0.1e5); ax.set_ylim(e2[2], e2[3] - 0.3e5); ax.set_facecolor("none")
    fig.text(0.015 + k * 0.247, 0.835, title, fontproperties=FELLSC, fontsize=14, color=RED)
    fig.text(0.015 + k * 0.247, 0.815, f"{R['roots'][key]['rivers']} rivers and streams", fontproperties=FELL, fontsize=11, color=INKC)
fig.text(0.02, 0.95, "How many Avons?", fontproperties=FELL, fontsize=24, color=INKC, va="center")
fig.text(0.02, 0.905, "Four old river words used again and again, from Devon to the Highlands. Each dot starts a mapped stretch of river.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
out(fig, "avons")
print("figures done")
