"""River-name roots (Brittonic or older) and the origins of the largest English rivers.

Authorities (full references in the paper and NOTES.md, all to be checked by the reviewer):
  EKWALL28  Ekwall, E. (1928) English River-Names. Oxford: Clarendon Press.
  WATTS     Watts, V. (2004) The Cambridge Dictionary of English Place-Names.
  MILLS     Mills, A. D. (2011) A Dictionary of British Place-Names.
  OWEN      Owen, H. W. and Morgan, R. (2007) Dictionary of the Place-Names of Wales.
  WATSON    Watson, W. J. (1926) The History of the Celtic Place-Names of Scotland.
Each meaning is the one these works give, from memory; several are debated, which the 'note' says.
ROOTS: (key, label, regex on the specific name with any qualifier removed, meaning, certainty, note)."""

ROOTS = [
    ("avon", "Avon", r"^(avon|afon)$", "Brittonic *abona, 'river' (Welsh afon)", "certain",
     "Literally 'river'. Some Scottish Avons may instead be Gaelic: those are marked probable."),
    ("isca", "Esk, Exe, Axe, Usk", r"^(esk|exe|axe|usk|wysg)$", "Brittonic *isca, usually read as 'water'", "probable",
     "Ekwall derives Esk, Exe, Axe and Usk from one root for water; the Esks of Scotland and Cumbria are counted with them."),
    ("ouse", "Ouse", r"^(ouse|great ouse|little ouse)$", "a Brittonic or older word for 'water'", "probable",
     "Pre-English; the meaning 'water' is a common but not certain reading."),
    ("derwent", "Derwent, Darwen, Darent, Dart", r"^(derwent|darwen|darent|dart)$", "Brittonic *derwā, 'oak': 'river where oaks grow'", "certain",
     "Dart is a shorter form of the same root."),
    ("dee", "Dee", r"^(dee|dyfrdwy)$", "Brittonic *dēwā, 'goddess, holy one'", "probable",
     "The Welsh name Dyfrdwy is 'water of the goddess'."),
    ("don", "Don", r"^don$", "perhaps the goddess Dānu, or a word for water", "probable", "Pre-English; meaning debated."),
    ("tam", "Thames, Tame, Thame, Teme, Tamar, Team", r"^(thames|tame|thame|teme|tamar|team)$", "a pre-English root *tam-, often read as 'dark'", "probable",
     "The grouping is Ekwall's; the meaning 'dark' is debated."),
    ("calder", "Calder", r"^(calder|callater)$", "Brittonic *caleto-dubron, 'hard (rocky) water'", "certain", ""),
    ("leven", "Leven", r"^leven$", "Brittonic *lēβn-, 'smooth'", "probable", ""),
    ("alaun", "Aln, Alne, Allen, Ellen, Alun", r"^(aln|alne|allen|ellen|alun|alyn|allan)$", "a pre-English root *alaun-, meaning uncertain", "probable",
     "Grouped by Ekwall; meaning unknown, perhaps 'wandering' or a divine name."),
    ("frome", "Frome", r"^(frome|ffraw)$", "Brittonic *frām, 'fair, fine, brisk'", "probable", ""),
    ("kennet", "Kennet, Kent", r"^(kennet|kent)$", "a pre-English root of uncertain meaning (Roman Cunetio)", "probable", ""),
    ("colne", "Colne, Clun", r"^(colne|clun)$", "pre-English, meaning unknown", "probable", ""),
    ("wye", "Wye, Wey", r"^(wye|wey|gwy)$", "pre-English, meaning unknown", "probable", ""),
    ("trent", "Trent", r"^trent$", "Brittonic, often read as 'the trespasser', the river that floods", "probable", ""),
    ("severn", "Severn", r"^(severn|hafren)$", "pre-English (Latin Sabrina, Welsh Hafren), meaning unknown", "certain", ""),
]

# Origin of the 60 largest English rivers in the data (by the spread of their mapped course), after Ekwall (1928) and Watts (2004).
# pre: Brittonic or older; english: Old English, or a later English back-formation from a place name; uncertain: debated or unknown.
ORIGIN = {
    "thames": "pre", "trent": "pre", "nene": "pre", "great ouse": "pre", "avon": "pre", "severn": "pre", "derwent": "pre", "ure": "pre",
    "teme": "pre", "wye": "pre", "calder": "pre", "kennet": "pre", "tamar": "pre", "exe": "pre", "taw": "pre", "aire": "pre", "yare": "pre",
    "lune": "pre", "don": "pre", "medway": "pre", "wey": "pre", "lea": "pre", "tees": "pre", "ouse": "pre", "lugg": "pre", "dove": "pre",
    "little ouse": "pre", "brue": "pre", "soar": "pre", "colne": "pre", "thame": "pre", "frome": "pre", "tweed": "pre", "tame": "pre",
    "tyne": "pre", "wear": "pre", "windrush": "pre", "eden": "pre", "esk": "pre", "axe": "pre", "dart": "pre", "teign": "pre", "fowey": "pre", "tone": "pre", "kent": "pre", "nidd": "pre", "rye": "uncertain", "skerne": "uncertain", "hodder": "pre", "leen": "uncertain", "idle": "english", "ivel": "uncertain", "ouzel": "english", "stort": "english", "beane": "uncertain", "glen": "pre", "isle": "uncertain", "ock": "pre", "loddon": "pre", "blackwater": "english", "culm": "pre", "yeo": "english", "tavy": "pre", "camel": "pre", "fal": "uncertain", "erewash": "english", "rea": "english", "sow": "uncertain", "penk": "pre", "anker": "uncertain", "leam": "pre", "arrow": "pre", "stour": "uncertain", "great stour": "uncertain", "trym": "uncertain", "cuckmere": "english", "ouse": "pre", "adur": "english", "lymington": "english", "wandle": "english", "brent": "pre", "chess": "english", "gade": "uncertain", "ver": "pre", "lee": "pre", "mimram": "uncertain", "rib": "uncertain", "ash": "english", "pant": "pre", "blyth": "english", "chelt": "english", "evenlode": "english", "glyme": "uncertain", "bain": "uncertain", "ancholme": "uncertain", "hull": "uncertain", "foulness": "english", "derwent": "pre", "rye ": "uncertain", "seven": "uncertain", "esk": "pre", "greta": "norse", "eamont": "english", "lowther": "uncertain", "irthing": "uncertain", "gelt": "norse", "petteril": "uncertain", "caldew": "pre", "south tyne": "pre", "north tyne": "pre", "rede": "uncertain", "coquet": "uncertain", "wansbeck": "uncertain", "blyth": "english", "till": "uncertain", "glen": "pre", "breamish": "uncertain", "browney": "uncertain", "gaunless": "norse", "leven": "pre", "kent": "pre", "bela": "norse", "keer": "uncertain", "wyre": "uncertain", "brock": "english", "douglas": "pre", "yarrow": "pre", "tame": "pre", "goyt": "uncertain", "etherow": "uncertain", "medlock": "english", "roch": "english", "irk": "uncertain", "bollin": "uncertain", "dane": "uncertain", "wheelock": "pre", "gowy": "pre", "tern": "uncertain", "roden": "uncertain", "perry": "english", "onny": "uncertain", "corve": "uncertain", "rea brook": "english", "worfe": "uncertain", "stour ": "uncertain",
    "mersey": "english", "waveney": "english", "cherwell": "english", "weaver": "english", "lark": "english", "rother": "english",
    "arun": "english", "roding": "english", "irwell": "english", "wensum": "english", "cam": "english", "mole": "english", "evenlode": "english",
    "otter": "english", "chelmer": "english",
    "welland": "uncertain", "wharfe": "uncertain", "ribble": "uncertain", "stour": "uncertain", "witham": "uncertain", "parrett": "uncertain",
    "test": "uncertain", "swale": "uncertain", "bure": "uncertain", "wissey": "uncertain", "great stour": "uncertain", "tern": "uncertain",
    "torridge": "uncertain", "dane": "uncertain", "itchen": "uncertain", "hull": "uncertain", "coquet": "uncertain", "wyre": "uncertain",
}
ORIGIN_NOTE = {
    "mersey": "Old English, the boundary river", "waveney": "Old English, river by a quaking fen", "cherwell": "Old English wella, stream; first element uncertain",
    "weaver": "Old English, winding river", "lark": "back-formation from Lackford", "rother": "back-formation from Rotherfield (the eastern Rother; the western Rother is from Rotherbridge)",
    "arun": "back-formation from Arundel", "roding": "from the Roding villages, Old English folk name", "irwell": "Old English, winding stream",
    "wensum": "Old English, winding", "cam": "back-formation from Cambridge (earlier Granta)", "mole": "back-formation from Molesey",
    "evenlode": "back-formation from the village of Evenlode", "otter": "Old English otor, otter", "chelmer": "back-formation from Chelmsford",
}
EXCLUDE_SPEC = {"bedford", "nene old course", "old bedford", "new bedford", "hundred foot", "forty foot", "sixteen foot", "twenty foot"}   # artificial cuts in the Fens
