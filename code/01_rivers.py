"""Step 1: from OpenStreetMap waterway ways to named rivers. Normalise each name, split it into the generic word (River,
Afon, Allt, Burn, Beck, Brook...) and the specific name (Avon, Esk, Derwent...), and join ways of the same name into one
watercourse when their start points chain within a set distance (15 km for rivers, 4 km for streams).
Output: WORK/ways.csv.gz (one row per way), WORK/rivers.csv.gz (one row per watercourse)."""
import unicodedata, warnings
warnings.filterwarnings("ignore")
import pandas as pd, numpy as np
import geopandas as gpd
from scipy.spatial import cKDTree
import pyproj
from common import *
from generics import split_name

rows = []
for r in read_tsv(RIVERS):
    m = re.search(r"\(+\s*([-\d.]+)\s+([-\d.]+)", r["p"])
    if not m:
        continue
    rows.append(dict(osm=r["x"].split("openstreetmap.org/")[-1], ww=r["ww"], name=r["name"].strip(), name_cy=r["namecy"].strip(),
                     name_gd=r["namegd"].strip(), lon=float(m.group(1)), lat=float(m.group(2))))
w = pd.DataFrame(rows)
n_raw = len(w)
w = w[(w.name != "") & w.osm.str.startswith("way/")].drop_duplicates("osm")
print("ways", n_raw, "kept", len(w), w.ww.value_counts().to_dict())
sp = w.name.map(split_name)
w["generic"], w["specific"], w["key"] = [s[0] for s in sp], [s[1] for s in sp], [s[2] for s in sp]
tr = pyproj.Transformer.from_crs(4326, 27700, always_xy=True)
w["E"], w["N"] = tr.transform(w.lon.values, w.lat.values)

# join ways into watercourses: same normalised full name and type class, start points chained
w["cls"] = np.where(w.ww == "canal", "canal", np.where(w.ww == "river", "river", "stream"))
w["wid"] = -1
nid = 0
for (nm, cls), grp in w.groupby(["key", "cls"]):
    d = 15000 if cls == "river" else (8000 if cls == "canal" else 4000)
    xy = grp[["E", "N"]].values
    par = np.arange(len(grp))
    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]; i = par[i]
        return i
    for i, j in cKDTree(xy).query_pairs(d):
        a, b = f(i), f(j)
        if a != b: par[a] = b
    roots = np.array([f(i) for i in range(len(grp))])
    _, lab = np.unique(roots, return_inverse=True)
    w.loc[grp.index, "wid"] = lab + nid
    nid += lab.max() + 1
print("watercourses", nid)

# a river and a stream of the same name that touch are one watercourse (OSM often tags the upper part a stream)
g = w.groupby("wid").agg(name=("name", lambda s: s.value_counts().index[0]), key=("key", "first"), generic=("generic", "first"),
                         specific=("specific", "first"), cls=("cls", "first"), ways=("osm", "size"),
                         name_cy=("name_cy", lambda s: next((x for x in s if x), "")), name_gd=("name_gd", lambda s: next((x for x in s if x), "")),
                         lon=("lon", "median"), lat=("lat", "median"), E0=("E", "min"), E1=("E", "max"), N0=("N", "min"), N1=("N", "max"),
                         osm=("osm", "first"))
g["extent_km"] = np.hypot(g.E1 - g.E0, g.N1 - g.N0) / 1000
# county and nation at the median start point
cty = gpd.read_file(f"{GEO}/counties_uk.geojson").to_crs(4326)
pts = gpd.GeoDataFrame(g, geometry=gpd.points_from_xy(g.lon, g.lat), crs=4326)
j = gpd.sjoin(pts, cty[["county", "nation", "geometry"]], how="left", predicate="within")
j = j[~j.index.duplicated()]
g["county"], g["nation"] = j["county"].values, j["nation"].values
miss = g.nation.isna()
if miss.any():
    nn = gpd.sjoin_nearest(pts[miss.values].to_crs(27700), cty.to_crs(27700)[["county", "nation", "geometry"]], how="left", max_distance=5000)
    nn = nn[~nn.index.duplicated()]
    g.loc[nn.index, "county"] = nn["county"].values; g.loc[nn.index, "nation"] = nn["nation"].values
g["nation"] = g.nation.fillna("Other"); g["county"] = g.county.fillna("")
g.reset_index().to_csv(f"{WORK}/rivers.csv.gz", index=False)
w.to_csv(f"{WORK}/ways.csv.gz", index=False)
print(g.cls.value_counts().to_dict(), g.nation.value_counts().to_dict())
print(g[g.cls == "river"].sort_values("extent_km", ascending=False).head(40)[["name", "ways", "extent_km", "county"]].to_string())
