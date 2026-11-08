"""Generic words for a watercourse, and how a name splits into generic + specific.

GENERICS: (key, label, language, meaning, regexes). Before the specific: River, Afon, Allt, Abhainn, Nant, Water of, Burn of.
After it: Brook, Beck, Burn, Bourne, Water, Gill, Sike, Dyke, Rhyne, Lode, Fleet, River, Stream. One-word names ending in a
generic (Holbeck, Tyburn, Westbourne, Cottesbrook) count for that generic.
Meanings are the ordinary senses given in the place-name literature (Gelling and Cole 2000; Mills 2011; Owen and Morgan 2007),
listed in NOTES.md for checking."""
import re, unicodedata

GENERICS = [
    ("brook", "brook", "Old English", "brōc, a stream"),
    ("beck", "beck", "Old Norse", "bekkr, a stream"),
    ("burn", "burn", "Old English and Scots", "burna, a stream (Scots burn)"),
    ("bourne", "bourne", "Old English", "burna, a stream, in the south often an intermittent chalk stream"),
    ("water", "water", "English and Scots", "a river or large stream (Scotland, Cumbria, Northern Ireland)"),
    ("gill", "gill or ghyll", "Old Norse", "gil, a ravine with a stream"),
    ("sike", "sike or syke", "Old English and Norse", "sīc, sík, a small stream or ditch"),
    ("dyke", "dyke or dike", "Old English and Norse", "dīc, dík, a ditch or drain"),
    ("rhyne", "rhyne or rhine", "Old English", "ryne, a drainage channel (Somerset Levels)"),
    ("lode", "lode", "Old English", "lād, a watercourse or channel (Fens)"),
    ("fleet", "fleet", "Old English", "flēot, a creek or inlet"),
    ("allt", "allt", "Scottish Gaelic", "allt, a stream (also a steep slope)"),
    ("abhainn", "abhainn", "Scottish Gaelic", "abhainn, a river"),
    ("nant", "nant", "Welsh", "nant, a stream (also a valley)"),
    ("afon", "afon", "Welsh", "afon, a river"),
    ("river", "river", "English", "river"),
    ("other", "other or none", "", ""),
]
GLAB = {g[0]: g[1] for g in GENERICS}
QUAL = r"(?:great|little|upper|lower|east|west|north|south|old|new|middle|black|white|red|nether|over|mill|long)"


def norm(s):
    s = unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode().lower()
    s = s.replace("’", "'").replace("&", "and")
    return re.sub(r"\s+", " ", re.sub(r"[\(\)\[\],.]", " ", s)).strip()


PRE = [("river", r"^(?:the )?river (?:of )?"), ("afon", r"^afon "), ("allt", r"^(?:allt|alltan|ault) "), ("abhainn", r"^(?:abhainn|amhainn|avon an?) "),
       ("nant", r"^nant "), ("water", r"^water of "), ("burn", r"^burn of "), ("gill", r"^(?:gill|ghyll) of ")]
POST = [("brook", r" brook$"), ("beck", r" beck$"), ("burn", r" burn$"), ("bourne", r" bourne?$"), ("water", r" water$"), ("gill", r" (?:gill|ghyll)$"),
        ("sike", r" (?:sike|syke)$"), ("dyke", r" (?:dyke|dike)$"), ("rhyne", r" (?:rhyne|rhine)$"), ("lode", r" lode$"), ("fleet", r" fleet$"),
        ("river", r" river$"), ("other", r" (?:stream|drain|cut|canal|navigation|leat|race|sewer|ditch|channel|lake)$")]
ONEWORD = [("brook", r"brook$"), ("beck", r"beck$"), ("burn", r"burn$"), ("bourne", r"bourne?$"), ("gill", r"(?:gill|ghyll)$"), ("sike", r"(?:sike|syke)$"),
           ("dyke", r"(?:dyke|dike)$"), ("lode", r"lode$"), ("fleet", r"fleet$")]


def split_name(name):
    """-> (generic, specific, key). key is the normalised full name used to join ways."""
    n = norm(name)
    key = n
    for g, rx in PRE:
        m = re.match(rx, n)
        if m and len(n) > m.end():
            spec = n[m.end():]
            # 'River Avon' with an English suffix as well ('River Leen Brook' is rare): keep the prefix generic
            return g, spec, key
    for g, rx in POST:
        m = re.search(rx, n)
        if m and m.start() > 0:
            return g, n[:m.start()].strip(), key
    if " " not in n:
        for g, rx in ONEWORD:
            m = re.search(rx, n)
            if m and m.start() >= 2:
                return g, n, key
    return "other", n, key
