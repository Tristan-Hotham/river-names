"""Step 2: roots for every watercourse, the review list, the generic words, the origins of the largest English rivers, and the
place-name comparison. Output: WORK/classified.csv.gz, WORK/places.csv.gz, WORK/review_roots.txt, WORK/borrowed.csv"""
import warnings
warnings.filterwarnings("ignore")
import pandas as pd, numpy as np
from scipy.spatial import cKDTree
import pyproj
from common import *
from generics import norm, QUAL
from roots import ROOTS, ORIGIN, EXCLUDE_SPEC

g = pd.read_csv(f"{WORK}/rivers.csv.gz", keep_default_na=False)
w = pd.read_csv(f"{WORK}/ways.csv.gz", keep_default_na=False, usecols=["osm", "wid", "E", "N", "lon", "lat"])
g["spec0"] = g.specific.str.replace(r"^(" + QUAL + r") ", "", regex=True).str.replace(r"^(the) ", "", regex=True)
# Welsh and Gaelic specific names: also try the Welsh or Gaelic tag (Afon Wysg for the Usk)
from generics import split_name
g["spec_cy"] = g.name_cy.map(lambda s: split_name(s)[1] if s else "")
g["root"], g["root_cert"] = "", ""
for key, lab, rx, meaning, cert, note in ROOTS:
    m = (g.spec0.str.match(rx) | g.spec_cy.str.match(rx)) & (g.cls != "canal")
    g.loc[m & (g.root == ""), "root"] = key
    g.loc[m & (g.root_cert == ""), "root_cert"] = cert
# Scottish Avons may be Gaelic (Athfhinn, 'bright one'): probable only
g.loc[(g.root == "avon") & (g.nation == "Scotland"), "root_cert"] = "probable"
ov = pd.read_csv(os.path.join(ROOT, "code", "overrides.csv"), keep_default_na=False)
g["review"] = ""
for o in ov.itertuples():
    sel = g.osm == o.osm
    if not sel.any(): print("override not used", o.osm); continue
    if o.action == "drop_root":
        g.loc[sel, ["root", "root_cert"]] = ["", ""]
    elif o.action.startswith("root="):
        g.loc[sel, "root"] = o.action.split("=")[1]
    elif o.action == "probable":
        g.loc[sel, "root_cert"] = "probable"
    g.loc[sel, "review"] = o.reason
pd.set_option("display.width", 220)
with open(f"{WORK}/review_roots.txt", "w") as f:
    for key, *_ in ROOTS:
        s = g[g.root == key].sort_values(["nation", "name"])
        f.write(f"===== {key} {len(s)}\n" + s[["osm", "name", "name_cy", "cls", "ways", "extent_km", "county", "root_cert", "review"]].to_string(index=False) + "\n")
g.to_csv(f"{WORK}/classified.csv.gz", index=False)

# ---------- places (for the comparison)
P = []
for r in read_tsv(PL_UK):
    lon, lat = point(r["wkt"])
    if lon is None or r["place"] not in ("city", "town", "village", "hamlet"):
        continue
    P.append(dict(osm=r["x"].split("openstreetmap.org/")[-1], kind=r["place"], name=r["name"], lon=lon, lat=lat))
P = pd.DataFrame(P)
tr = pyproj.Transformer.from_crs(4326, 27700, always_xy=True)
P["E"], P["N"] = tr.transform(P.lon.values, P.lat.values)
import geopandas as gpd
cty = gpd.read_file(f"{GEO}/counties_uk.geojson").to_crs(4326)
j = gpd.sjoin(gpd.GeoDataFrame(P, geometry=gpd.points_from_xy(P.lon, P.lat), crs=4326), cty[["county", "nation", "geometry"]], how="left", predicate="within")
j = j[~j.index.duplicated()]
P["county"], P["nation"] = j.county.values, j.nation.values
P["first"] = P.name.map(lambda s: next((t for t in re.split(r"[\s\-]+", norm(s)) if not re.fullmatch(QUAL + "|st|saint|the|king's|kings|market|chipping|long|high|great|little", t)), ""))
EN = (r"(ton|tone|ham|hampton|ley|leigh|lee|bury|borough|burgh|brough|ford|field|worth|worthy|wardine|wick|wich|stead|sted|den|don|hurst|hirst|"
      r"well|wells|bridge|stow|stowe|minster|cester|caster|chester|by|thorpe|thorp|thwaite|toft|holme|beck|dale|kirk|hall|wood|ing|ings|mouth|"
      r"port|hithe|ey|sey|bourne|burn|brook|cote|cott|cot|combe|comb|cliffe|cliff|church|castle|haven|marsh|moor|mere|over|hope|ridge|shaw|"
      r"low|ness|ay|head|side|gate|stone|ham|hay|land|sall|sett|all|wold|age|ock)$")
P["english_end"] = P["first"].str.contains(EN, regex=True)
P.to_csv(f"{WORK}/places.csv.gz", index=False)

# ---------- settlements that borrow a river's name: within 6 km of the river's mapped start points, first word starting with it
COMMON = {"black", "white", "red", "mill", "new", "old", "south", "north", "east", "west", "little", "great", "river", "brook", "hall", "green",
          "lower", "upper", "dean", "nant", "allt", "the", "wood", "moor", "park", "lake", "bridge", "beck", "burn", "town", "low", "high"}
tree = cKDTree(P[["E", "N"]].values)
rows = []
R = g[(g.cls == "river") & (g.spec0.str.len() >= 3) & ~g.spec0.str.contains(" ") & ~g.spec0.isin(COMMON)]
ws = w.groupby("wid")
for r in R.itertuples():
    pts = ws.get_group(r.wid)[["E", "N"]].values
    near = set()
    for lst in tree.query_ball_point(pts, 6000):
        near.update(lst)
    for k in near:
        p = P.iloc[k]
        if p["first"].startswith(r.spec0) and len(p["first"]) >= len(r.spec0):
            rows.append(dict(river=r.name, spec=r.spec0, root=r.root, place=p["name"], kind=p.kind, county=p.county, nation=p.nation, osm=p.osm))
B = pd.DataFrame(rows).drop_duplicates(["river", "place", "county"])
B.to_csv(f"{WORK}/borrowed.csv", index=False)
print("roots", g[g.root != ""].root.value_counts().to_dict())
print("borrowed", len(B), B.groupby("spec").place.apply(lambda s: ", ".join(sorted(set(s))[:8])).sort_index().head(80).to_string())
