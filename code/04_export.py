"""Step 4: page data. data/rivers.json (every named watercourse: one point, generic, root) and data/rootpts.json (the start point
of every mapped way of the rivers in a root group, which traces their courses), and data/places.json (towns for the search)."""
import pandas as pd
from common import *
from generics import GENERICS
from roots import ROOTS, ORIGIN

R = jload(f"{DATA}/results.json")
g = pd.read_csv(f"{DATA}/watercourses.csv", keep_default_na=False)
g = g[g.cls != "canal"]
GK = [x[0] for x in GENERICS]
RK = [x[0] for x in ROOTS]
OK = {"pre": 1, "english": 2, "uncertain": 3}
rows = [[round(float(r.lon), 4), round(float(r.lat), 4), r.name, GK.index(r.generic), RK.index(r.root) if r.root else -1, 1 if r.cls == "river" else 0,
         r.county or r.nation, OK.get(r.origin_major, 0) if r.cls == "river" and r.nation == "England" else 0, r.osm, r.name_cy or r.name_gd] for r in g.itertuples()]
jsave({"generics": [list(x) for x in GENERICS], "roots": [[k, l, m, c, n] for k, l, rx, m, c, n in ROOTS],
       "cols": ["lon", "lat", "name", "generic", "root", "river", "county", "origin", "osm", "alt"], "rows": rows}, f"{DATA}/rivers.json")
w = pd.read_csv(f"{WORK}/ways.csv.gz", keep_default_na=False, usecols=["osm", "wid", "lon", "lat"])
HB = pd.read_csv(os.path.join(ROOT, "code", "root_rivers_by_hand.csv"))
c = pd.read_csv(f"{WORK}/classified.csv.gz", keep_default_na=False, usecols=["wid", "root", "root_cert"])
w = w.merge(HB, on="wid").merge(c, on="wid")
RIV = sorted(w.river.unique())
pts = [[round(float(r.lon), 4), round(float(r.lat), 4), RK.index(r.root), RIV.index(r.river)] for r in w.itertuples()]
jsave({"rivers": RIV, "pts": pts}, f"{DATA}/rootpts.json")
P = pd.read_csv(f"{WORK}/places.csv.gz", keep_default_na=False)
P = P[P.kind.isin(["city", "town", "village"])]
pri = {"city": 0, "town": 1, "village": 2}
P = P.assign(p=P.kind.map(pri)).sort_values(["p", "name"])
jsave({"places": [[r.name, round(float(r.lon), 4), round(float(r.lat), 4), r.p, r.county if isinstance(r.county, str) and r.county else (r.nation or "")] for r in P.itertuples()]}, f"{DATA}/places.json")
for f in ("rivers.json", "rootpts.json", "places.json"):
    print(f, os.path.getsize(f"{DATA}/{f}") // 1024, "KB")
