"""Step 3: every number quoted anywhere goes into data/results.json. Also writes the derived data files:
data/watercourses.csv (every named watercourse with generic, root and origin), data/root_rivers.csv (each river in a root group),
data/major_rivers_england.csv, data/generic_by_county.csv, data/borrowed_names.csv, data/generic_grid.csv."""
import warnings
warnings.filterwarnings("ignore")
import pandas as pd, numpy as np
from scipy.spatial import cKDTree
from common import *
from generics import GENERICS, GLAB
from roots import ROOTS, ORIGIN, ORIGIN_NOTE, EXCLUDE_SPEC

g = pd.read_csv(f"{WORK}/classified.csv.gz", keep_default_na=False)
w = pd.read_csv(f"{WORK}/ways.csv.gz", keep_default_na=False, usecols=["wid", "E", "N"])
P = pd.read_csv(f"{WORK}/places.csv.gz", keep_default_na=False)
P["english_end"] = P.english_end.astype(str) == "True"
B = pd.read_csv(f"{WORK}/borrowed.csv", keep_default_na=False)
R = {}
R["n_overrides"] = int(len(pd.read_csv(os.path.join(ROOT, "code", "overrides.csv"))))
R["n"] = {"ways": int(len(w)), "watercourses": len(g), "rivers": int((g.cls == "river").sum()), "streams": int((g.cls == "stream").sum()),
          "canals": int((g.cls == "canal").sum()), "roots": len(ROOTS)}

# ---------- distinct rivers: OSM splits one river into pieces (gaps, a different tag for the upper course, Welsh names). For the
# root groups every piece was assigned to a river by hand, from its position (code/root_rivers_by_hand.csv).
HB = pd.read_csv(os.path.join(ROOT, "code", "root_rivers_by_hand.csv"))
g = g.merge(HB, on="wid", how="left")
g["river"] = g.river.fillna("")
assert set(g[g.root != ""].wid) == set(HB.wid), set(g[g.root != ""].wid) ^ set(HB.wid)
g["rid"] = g.river

# ---------- roots: distinct rivers per root
RR = []
for key, lab, rx, meaning, cert, note in ROOTS:
    s = g[g.root == key]
    grp = s.groupby("rid").agg(name=("river", "first"), spec=("spec0", "first"), ways=("ways", "sum"),
                               county=("county", lambda x: x.loc[s.loc[x.index, "ways"].idxmax()]), nation=("nation", lambda x: x.loc[s.loc[x.index, "ways"].idxmax()]),
                               cert=("root_cert", lambda x: "certain" if (x == "certain").all() else "probable"),
                               lon=("lon", "median"), lat=("lat", "median"))
    for r in grp.itertuples():
        RR.append(dict(root=key, root_label=lab, rid=r.Index, name=r.name, spec=r.spec, county=r.county, nation=r.nation, ways=r.ways, certainty=r.cert,
                       lon=r.lon, lat=r.lat, meaning=meaning))
RR = pd.DataFrame(RR).sort_values(["root", "ways"], ascending=[True, False])
RR.to_csv(f"{DATA}/root_rivers.csv", index=False)
R["roots"] = {}
for key, lab, rx, meaning, cert, note in ROOTS:
    s = RR[RR.root == key]
    R["roots"][key] = {"label": lab, "meaning": meaning, "certainty": cert, "note": note, "rivers": len(s),
                       "by_nation": s.nation.value_counts().to_dict(), "names": sorted(set(s.spec)),
                       "list": [f"{r.name} ({r.county})" for r in s.itertuples()]}
R["root_rivers"] = len(RR)
R["avon_rivers"] = R["roots"]["avon"]["rivers"]
R["avon_england"] = int(((RR.root == "avon") & (RR.nation == "England")).sum())
R["avon_scotland"] = int(((RR.root == "avon") & (RR.nation == "Scotland")).sum())
R["esk_rivers"] = int(((RR.root == "isca") & (RR.spec.str.endswith("esk"))).sum())
R["derwent_rivers"] = int(((RR.root == "derwent") & RR.spec.isin(["derwent", "darwen", "darent"])).sum())
R["calder_rivers"] = R["roots"]["calder"]["rivers"]

# ---------- generic words
G = g[g.cls != "canal"]
R["generic_counts"] = {k: int((G.generic == k).sum()) for k, *_ in GENERICS}
R["generic_by_nation"] = {nat: {k: int(((G.nation == nat) & (G.generic == k)).sum()) for k, *_ in GENERICS} for nat in ("England", "Scotland", "Wales", "Northern Ireland")}
SM = ["brook", "beck", "burn", "bourne", "water", "gill", "sike", "dyke", "rhyne", "lode", "allt", "abhainn", "nant", "afon"]
by_c = G[G.generic.isin(SM)].groupby(["county", "generic"]).size().unstack(fill_value=0)
by_c["total"] = by_c.sum(axis=1)
by_c.to_csv(f"{DATA}/generic_by_county.csv")
def share(c, a, b=("brook", "beck")):
    r = by_c.loc[c] if c in by_c.index else None
    if r is None: return None
    tot = sum(r.get(x, 0) for x in b)
    return float(100 * r.get(a, 0) / tot) if tot else None
# east: the two counties of the east Midlands and Lincolnshire where becks are common; mid: Derbyshire and Leicestershire, also
# inside the Danelaw (Five Boroughs) but with almost no becks, reported separately so the pooled share is not misleading
DANE = ["Lincolnshire", "Nottinghamshire"]
MID = ["Derbyshire", "Leicestershire"]
WEST = ["Cheshire", "Staffordshire", "Shropshire", "Greater Manchester"]
def grp_share(cs):
    be = sum(by_c.loc[c].get("beck", 0) for c in cs if c in by_c.index); br = sum(by_c.loc[c].get("brook", 0) for c in cs if c in by_c.index)
    return {"beck": int(be), "brook": int(br), "beck_pc": float(100 * be / (be + br))}
R["danelaw"] = {"east": grp_share(DANE), "mid": grp_share(MID), "west": grp_share(WEST), "east_counties": DANE, "mid_counties": MID, "west_counties": WEST,
                "east_lat": float(P[P.county.isin(DANE)].lat.median()), "west_lat": float(P[P.county.isin(WEST)].lat.median())}
R["beck_county"] = {c: share(c, "beck") for c in ("Cumbria", "North Yorkshire", "West Yorkshire", "Lincolnshire", "Nottinghamshire", "Derbyshire",
                                                 "Cheshire", "Staffordshire", "Norfolk", "Lancashire", "Leicestershire")}
# beck against brook by latitude in England
E = G[(G.nation == "England") & G.generic.isin(["beck", "brook"])].copy()
E["band"] = (E.lat * 4).round() / 4
lb = E.groupby("band").apply(lambda s: pd.Series({"beck": int((s.generic == "beck").sum()), "brook": int((s.generic == "brook").sum())}))
lb["beck_pc"] = 100 * lb.beck / (lb.beck + lb.brook)
lb = lb[(lb.beck + lb.brook) >= 30]
R["beck_bands"] = [{"lat": float(b), "beck": int(r.beck), "brook": int(r.brook), "beck_pc": float(r.beck_pc)} for b, r in lb.iterrows()]
cross = [b for b, r in lb.iterrows() if r.beck_pc >= 50]
R["beck_majority_from"] = float(min(cross)) if cross else None
R["beck_south5"] = float(np.percentile(G[(G.generic == "beck") & (G.nation == "England")].lat, 5))
R["brook_north95"] = float(np.percentile(G[(G.generic == "brook") & (G.nation == "England")].lat, 95))
# Scotland: Gaelic allt and abhainn against Scots burn and water
S = G[G.nation == "Scotland"]
R["scotland"] = {"allt": int((S.generic == "allt").sum()), "abhainn": int((S.generic == "abhainn").sum()), "burn": int((S.generic == "burn").sum()),
                 "water": int((S.generic == "water").sum())}
R["scotland"]["gaelic_pc"] = 100 * (R["scotland"]["allt"] + R["scotland"]["abhainn"]) / sum(R["scotland"].values())
for c in ("Highland", "Na h-Eileanan Siar", "Argyll and Bute", "Scottish Borders", "Dumfries and Galloway", "Aberdeenshire"):
    r = by_c.loc[c]
    tot = r.get("allt", 0) + r.get("abhainn", 0) + r.get("burn", 0) + r.get("water", 0)
    R["scotland"]["gaelic_pc_" + c.replace(" ", "_")] = float(100 * (r.get("allt", 0) + r.get("abhainn", 0)) / tot)
Wl = G[G.nation == "Wales"]
R["wales"] = {"nant": int((Wl.generic == "nant").sum()), "afon": int((Wl.generic == "afon").sum()), "brook": int((Wl.generic == "brook").sum()),
              "river": int((Wl.generic == "river").sum()), "n": len(Wl)}
R["wales"]["welsh_pc"] = 100 * (R["wales"]["nant"] + R["wales"]["afon"]) / (R["wales"]["nant"] + R["wales"]["afon"] + R["wales"]["brook"] + R["wales"]["river"])
R["southern"] = {"bourne": R["generic_counts"]["bourne"], "rhyne": R["generic_counts"]["rhyne"], "lode": R["generic_counts"]["lode"],
                 "rhyne_somerset": int(by_c.loc["Somerset"].get("rhyne", 0)), "lode_cambs": int(by_c.loc["Cambridgeshire"].get("lode", 0))}
# dominant generic per 25 km square (for the map)
G2 = G[G.generic.isin(SM)].copy()
import pyproj
tr = pyproj.Transformer.from_crs(4326, 27700, always_xy=True)
G2["E"], G2["N"] = tr.transform(G2.lon.values, G2.lat.values)
G2["sq"] = (G2.E // 25000).astype(int).astype(str) + "_" + (G2.N // 25000).astype(int).astype(str)
grid = G2.groupby("sq").agg(n=("generic", "size"), top=("generic", lambda s: s.value_counts().index[0]),
                            top_n=("generic", lambda s: s.value_counts().iloc[0]), E=("E", "mean"), N=("N", "mean"))
grid["E0"] = grid.index.str.split("_").str[0].astype(int) * 25000; grid["N0"] = grid.index.str.split("_").str[1].astype(int) * 25000
grid = grid[grid.n >= 5]
grid.to_csv(f"{DATA}/generic_grid.csv")
R["grid"] = {"squares": len(grid), "top_counts": grid.top.value_counts().to_dict()}

# ---------- the largest English rivers: origin of the name
Eng = g[(g.cls == "river") & (g.nation == "England") & ~g.spec0.isin(EXCLUDE_SPEC)]
size = Eng.groupby("spec0").extent_km.max().sort_values(ascending=False)
top = list(size.index[:60])
missing = [s for s in top if s not in ORIGIN]
assert not missing, missing
MR = pd.DataFrame([{"rank": i + 1, "river": s, "extent_km": float(size[s]), "origin": ORIGIN[s], "note": ORIGIN_NOTE.get(s, "")} for i, s in enumerate(top)])
MR.to_csv(f"{DATA}/major_rivers_england.csv", index=False)
R["major"] = {"n": len(MR), "pre": int((MR.origin == "pre").sum()), "english": int((MR.origin == "english").sum()), "uncertain": int((MR.origin == "uncertain").sum())}
for k in ("pre", "english", "uncertain"):
    R["major"][k + "_pc"] = 100 * R["major"][k] / len(MR)
top20 = MR.head(20)
R["major"]["top20_pre"] = int((top20.origin == "pre").sum())
R["major"]["english_list"] = [f"{r.river.title()}" for r in MR[MR.origin == "english"].itertuples()]
R["major"]["top10"] = [r.river.title() for r in MR.head(10).itertuples()]
R["major"]["top10_pre"] = int((MR.head(10).origin == "pre").sum())

# ---------- towns: English or Norse names
T = P[(P.nation == "England") & P.kind.isin(["city", "town"])]
R["towns"] = {"n": len(T), "english_end": int(T.english_end.sum()), "english_pc": float(100 * T.english_end.mean())}
V = P[(P.nation == "England") & (P.kind == "village")]
R["villages"] = {"n": len(V), "english_end": int(V.english_end.sum()), "english_pc": float(100 * V.english_end.mean())}

# ---------- settlements named from a pre-English river
pre_specs = set(RR.spec) | {s for s, o in ORIGIN.items() if o == "pre"}
BB = B[B.spec.isin(pre_specs) & (B.kind.isin(["city", "town", "village", "hamlet"]))].copy()
BB = BB[(BB.place.str.lower() != BB.river.str.lower()) & ~BB.place.str.contains("Travellers|Junction|Farm|Hall$|Park$", regex=True)]
BB.to_csv(f"{DATA}/borrowed_names.csv", index=False)
R["borrowed"] = {"n": len(BB), "rivers": int(BB.spec.nunique()),
                 "examples": {s: sorted(set(BB[BB.spec == s].place))[:6] for s in ("exe", "axe", "avon", "tamar", "aln", "esk", "colne", "calder", "derwent", "trent", "severn", "kennet", "dart", "wear", "tyne", "tees", "eden", "lune", "ure", "nene", "frome") if (BB.spec == s).any()}}

# ---------- facts quoted in words
def has(spec, place):
    return bool(((BB.spec == spec) & (BB.place == place)).any())
R["checks"] = {"exeter": has("exe", "Exeter"), "exmouth": has("exe", "Exmouth"), "alnwick": has("aln", "Alnwick"), "axminster": has("axe", "Axminster"),
               "lancaster": has("lune", "Lancaster")}
jsave(R, f"{DATA}/results.json", indent=1)

# ---------- the data file of every watercourse
out = g[["wid", "rid", "osm", "name", "name_cy", "name_gd", "cls", "generic", "specific", "spec0", "root", "root_cert", "ways", "extent_km", "county", "nation", "lon", "lat", "review"]].copy()
out["generic_label"] = out.generic.map(GLAB)
# the origin class belongs to the one watercourse ranked in the 60 (other rivers of the same name, such as the Derbyshire Rother,
# can have a different origin)
top_wid = {Eng[Eng.spec0 == s].sort_values("extent_km", ascending=False).wid.iloc[0]: s for s in top}
out["origin_major"] = out.wid.map(lambda w_: ORIGIN[top_wid[w_]] if w_ in top_wid else "")
out.to_csv(f"{DATA}/watercourses.csv", index=False)
print(json.dumps({k: R[k] for k in ("n", "avon_rivers", "avon_england", "avon_scotland", "esk_rivers", "derwent_rivers", "calder_rivers", "root_rivers",
                                     "danelaw", "beck_county", "beck_majority_from", "beck_south5", "brook_north95", "scotland", "wales", "southern",
                                     "major", "towns", "villages", "checks", "grid")}, indent=1, ensure_ascii=False))
print({k: (v["rivers"], v["by_nation"]) for k, v in R["roots"].items()})
print(R["borrowed"])
