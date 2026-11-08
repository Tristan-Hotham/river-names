"""Shared paths, constants and helpers for the river-names study ("Avon means river").

Raw inputs (read in place, never modified):
  RIVERS /home/claude/newdata/raw_new9/rivers_uk.tsv.gz
         OpenStreetMap via QLever: waterway=river, stream and canal ways (and a few relations) in the UK with name, name:cy,
         name:gd and the start of the geometry as WKT (?p). One row per way.
  PL_UK  /home/claude/newdata/raw_new9/places_uk.tsv.gz  OpenStreetMap place nodes in the UK (for the place-name comparison).
  TILES  /home/claude/newdata/raw_new8/terrain/tiles/10  AWS Terrain Tiles (not used for results; figures only if needed).
  GEO    /home/claude/newdata/raw/geo/counties_uk.geojson (ONS boundaries, OGL v3) and Natural Earth (public domain).
Intermediates go to WORK (/home/claude/scratch/river-names), outside the repository.
"""
import json, gzip, os, re, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.environ.get("RN_RAW", "/home/claude/newdata/raw_new9")
RIVERS = os.path.join(RAW, "rivers_uk.tsv.gz")
PL_UK = os.path.join(RAW, "places_uk.tsv.gz")
TILES = os.environ.get("RN_TILES", "/home/claude/newdata/raw_new8/terrain/tiles/10")
GEO = os.environ.get("RN_GEO", "/home/claude/newdata/raw/geo")
FONTS = os.environ.get("RN_FONTS", "/home/claude/ref/fonts")
INK = os.environ.get("RN_INK", "/home/claude/studies/ink-map")
INKFONTS = os.path.join(INK, "fonts", "ttf")
DATA = os.path.join(ROOT, "data")
IMG = os.path.join(ROOT, "img")
WORK = os.environ.get("RN_WORK", "/home/claude/scratch/river-names")
for d in (DATA, IMG, WORK):
    os.makedirs(d, exist_ok=True)

SLUG = "river-names"
PAGE = f"https://maps.tristanhotham.com/{SLUG}/"
REPO = f"https://github.com/Tristan-Hotham/{SLUG}"
AI = ("I wrote the text, with drafting and editing assistance from Claude (Anthropic), which also helped "
      "prepare the analysis code. I reviewed and checked all text and results.")
BYLINE = "Dr Tristan Hotham · Independent researcher · 2026"


def jload(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def dash(v):
    """Remove em and en dashes and double hyphens from text (house style)."""
    if isinstance(v, str):
        v = re.sub(r"(\d)\s*[–—]\s*(\d)", r"\1 to \2", v)
        v = v.replace(" — ", ", ").replace("—", ", ").replace(" – ", ", ").replace("–", "-")
        while "--" in v:
            v = v.replace("--", "-")
        return v
    if isinstance(v, list):
        return [dash(x) for x in v]
    if isinstance(v, dict):
        return {k: dash(x) for k, x in v.items()}
    return v


def nonan(v):
    if isinstance(v, float) and (v != v or v in (float("inf"), float("-inf"))):
        return None
    if isinstance(v, (list, tuple)):
        return [nonan(x) for x in v]
    if isinstance(v, dict):
        return {k: nonan(x) for k, x in v.items()}
    if hasattr(v, "item"):
        return nonan(v.item())
    return v


def jsave(obj, path, indent=None):
    obj = nonan(obj)
    if os.path.abspath(path).startswith(DATA):
        obj = dash(obj)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, allow_nan=False, indent=indent, separators=None if indent else (",", ":"))


def get(R, path):
    v = R
    for k in path.split("."):
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def fmt(v, f=None):
    if f is None or f == "raw": return str(v)
    if f == "int": return f"{round(float(v)):,}"
    if f == "pc": return f"{round(float(v))}%"
    if f == "pc1": return f"{float(v):.1f}%"
    if f == "f1": return f"{float(v):.1f}"
    if f == "f2": return f"{float(v):.2f}"
    if f == "x": return f"{float(v):.1f}"
    raise ValueError(f)


def fill(t, R, keep=("DOI", "DOI_URL", "BLOG_URL"), tf=None):
    """replace {{path|fmt}} tokens from results.json; leave the publisher's placeholders and IMG tokens"""
    f = tf or fmt
    return re.sub(r"\{\{(?!IMG\|)([^{}|]+)(\|(\w+))?\}\}", lambda m: m.group(0) if m.group(1) in keep else f(get(R, m.group(1)), m.group(3)), t)


def read_tsv(path):
    """QLever TSV: header line, IRIs in <...>, literals in "..." (possibly @lang or ^^type)."""
    def lit(s):
        s = s.strip()
        if s.startswith("<") and s.endswith(">"):
            return s[1:-1]
        m = re.match(r'^"(.*)"(?:@[\w-]+|\^\^.*)?$', s, re.S)
        if m:
            return m.group(1).replace('\\"', '"').replace("\\\\", "\\")
        return s
    with gzip.open(path, "rt", encoding="utf-8") as f:
        head = [h.lstrip("?") for h in f.readline().rstrip("\n").split("\t")]
        for line in f:
            parts = line.rstrip("\n").split("\t")
            parts += [""] * (len(head) - len(parts))
            yield {h: lit(p) for h, p in zip(head, parts)}


def point(wkt):
    m = re.search(r"POINT\s*\(\s*([-\d.eE]+)\s+([-\d.eE]+)", wkt or "")
    return (float(m.group(1)), float(m.group(2))) if m else (None, None)


def km(lat1, lon1, lat2, lon2):
    import numpy as np
    p1, p2, l1, l2 = map(np.radians, (lat1, lat2, lon1, lon2))
    return 6371.0 * 2 * np.arcsin(np.sqrt(np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin((l2 - l1) / 2) ** 2))


def elevations(lons, lats):
    """ground height (m) from the zoom-10 Terrarium tiles, bilinear; NaN where no tile"""
    import numpy as np
    from PIL import Image
    n = 256 * 2 ** 10
    lons, lats = np.asarray(lons, float), np.asarray(lats, float)
    X = (lons + 180) / 360 * n
    la = np.radians(lats)
    Y = (1 - np.log(np.tan(la) + 1 / np.cos(la)) / np.pi) / 2 * n
    out = np.full(len(lons), np.nan)
    tx, ty = (X // 256).astype(int), (Y // 256).astype(int)
    cache = {}
    for k in set(zip(tx.tolist(), ty.tolist())):
        p = f"{TILES}/{k[0]}/{k[1]}.png"
        if os.path.exists(p):
            a = np.asarray(Image.open(p).convert("RGB")).astype(float)
            cache[k] = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
    for i in range(len(lons)):
        h = cache.get((tx[i], ty[i]))
        if h is None:
            continue
        px, py = X[i] - tx[i] * 256 - 0.5, Y[i] - ty[i] * 256 - 0.5
        x0, y0 = int(min(max(np.floor(px), 0), 254)), int(min(max(np.floor(py), 0), 254))
        fx, fy = min(max(px - x0, 0), 1), min(max(py - y0, 0), 1)
        out[i] = (h[y0, x0] * (1 - fx) * (1 - fy) + h[y0, x0 + 1] * fx * (1 - fy) + h[y0 + 1, x0] * (1 - fx) * fy + h[y0 + 1, x0 + 1] * fx * fy)
    return out
