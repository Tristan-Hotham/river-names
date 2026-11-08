"""Step 9: README.md, LICENSE and the Reddit post text (reddit/post.md), filled from data/results.json."""
from common import *

R = jload(f"{DATA}/results.json")
M, D, S, W = R["major"], R["danelaw"], R["scotland"], R["wales"]
readme = f"""# Avon means river

The old roots and everyday words of the river names of the United Kingdom. {R['n']['ways']:,} named OpenStreetMap waterway stretches joined into {R['n']['watercourses']:,} named rivers, streams and canals; every name split into a generic word (river, afon, allt, burn, beck, brook...) and a specific name; specific names matched against sixteen Brittonic or older root groups after Ekwall's English River-Names (1928), with every piece of the {R['root_rivers']} root rivers assigned to its river by hand.

Interactive page: {PAGE}
Paper: {{https://doi.org/10.5281/zenodo.24063209}}
Blog post: {{https://blog.tristanhotham.com/2026/10/31/river-names/}}
Code and data: {REPO}

## Headline results

- Of the 60 largest English rivers in the data, {M['pre']} have names traced to Brittonic or older sources, {M['english']} English (several late back-formations from towns: Arun, Rother, Mole, Lark) and {M['uncertain']} uncertain; {M['top10_pre']} of the largest ten are pre-English. Meanwhile {R['towns']['english_pc']:.0f}% of England's {R['towns']['n']:,} towns and cities have a first word ending in an English or Norse element.
- {R['avon_rivers']} Avons ({R['avon_england']} in England, {R['avon_scotland']} in Scotland), {R['esk_rivers']} Esks, {R['derwent_rivers']} Derwents, Darwens and Darents, {R['calder_rivers']} Calders.
- Generic words follow the old language frontiers: {W['welsh_pc']:.0f}% nant or afon in Wales; Gaelic allt or abhainn {S['gaelic_pc_Highland']:.0f}% of allt, abhainn, burn and water names in Highland, 0% in the Borders and Dumfries and Galloway.
- The beck line: becks outnumber brooks in England north of about {R['beck_majority_from']:.2f}°N. At similar latitudes, {D['east']['beck_pc']:.0f}% becks in Lincolnshire and Nottinghamshire against {D['west']['beck_pc']:.0f}% (0 of {D['west']['brook']}) in Cheshire, Staffordshire, Shropshire and Greater Manchester; Derbyshire and Leicestershire, also in the Danelaw, have {D['mid']['beck']} becks to {D['mid']['brook']} brooks.
- {R['borrowed']['n']} towns and villages within 6 km of {R['borrowed']['rivers']} old-named rivers carry the river's name (Exeter, Dartmouth, Alnwick, Doncaster...).

## Files

| File | What it is |
|---|---|
| `index.html`, `js/page.js` | The interactive page: the Inked World map style (loaded from the ink-map study on the same site), every named river and stream coloured by its generic word, or the courses of the old-root rivers; pickers, search and popups. |
| `header.png` | Social card, 1200 x 630. |
| `data/watercourses.csv` | Every named watercourse ({R['n']['watercourses']:,}): first OSM way, name, Welsh and Gaelic names, type, generic, specific, root, reading, river (for root rivers), number of ways, spread, county, nation, position. ODbL. |
| `data/root_rivers.csv` | The {R['root_rivers']} distinct rivers and streams in the root groups. ODbL. |
| `data/major_rivers_england.csv` | The 60 largest English rivers and the origin of their names. |
| `data/generic_by_county.csv`, `data/generic_grid.csv` | Generic words by county and by 25 km square. |
| `data/borrowed_names.csv` | Settlements near old-named rivers that carry the river's name. ODbL. |
| `data/results.json` | Every number quoted on the page, in the paper, blog, collage and post. |
| `data/rivers.json`, `data/rootpts.json`, `data/places.json` | Page data. |
| `img/` | Figures on the page. |
| `code/` | Numbered scripts, `generics.py` and `roots.py` (the rules and origins), `root_rivers_by_hand.csv` (the hand assignment of river pieces), `overrides.csv` (false friends removed), templates, `qa.js`. |
| `release/` | Paper (`paper/`), blog post and figures (`blog/`), Zenodo files (`zenodo/`). |
| `reddit/` | Collage (`collage.py`, PNG) and post text. |

## Method in brief

- Waterways: OpenStreetMap waterway=river, stream and canal ways with a name in the UK, via QLever; ways of one name joined when their start points chain within 15 km (rivers), 8 km (canals) or 4 km (streams); canals left out of the analysis.
- Generic and specific: prefixes (River, Afon, Allt, Abhainn, Nant, Water of, Burn of) and suffixes (Brook, Beck, Burn, Bourne, Water, Gill, Sike, Dyke, Rhyne, Lode, Fleet, River) and one-word compounds (Holbeck).
- Roots: sixteen groups after Ekwall (1928), Watts (2004) and Mills (2011), matched on the specific name or the Welsh name; {R['n_overrides']} hand removals; each piece of each root river assigned to its river by hand.
- Largest rivers: ranked by the spread of mapped start points (a proxy: a long river mapped in few long ways, such as the Cumbrian Eden, falls outside the 60); origins after Ekwall and Watts. Towns: first word's ending.
- Caveats: etymologies are the standard ones, some debated; OSM naming of small streams is uneven; the size ranking is a proxy; the town test is crude.

## How to rerun

Needs Python 3 with pandas, numpy, scipy, geopandas, pyproj, matplotlib, Pillow; xelatex, pdftotext, pdfinfo; node with Playwright for `code/qa.js`. Raw inputs are listed in `code/common.py`; intermediates go to `RN_WORK`.

```
python3 code/01_rivers.py      # ways to watercourses
python3 code/02_classify.py    # roots, places, names borrowed from rivers
python3 code/03_analysis.py    # results.json and data files
python3 code/04_export.py      # page data
python3 code/05_figures.py     # figures
python3 code/06_build_site.py  # index.html
python3 code/07_paper.py       # paper PDF (DOI=10.5281/zenodo.N to fill the DOI)
python3 reddit/collage.py      # collage and header
python3 code/09_readme.py      # README, LICENSE, Reddit post
python3 code/08_release.py     # blog post, Zenodo files
```

## Sources and licences

- OpenStreetMap (https://www.openstreetmap.org/), © OpenStreetMap contributors, Open Database Licence, queried with QLever (University of Freiburg). The river and place tables are derived databases under the ODbL.
- ONS boundaries (Open Government Licence v3.0).
- River names: Ekwall (1928), Watts (2004), Mills (2011), Gelling and Cole (2000), Owen and Morgan (2007), Watson (1926). Full references in the paper.
- Map style: the Inked World (ink-map study, MIT code). MapLibre GL JS (BSD 3-Clause). Fonts: MedievalSharp, IM Fell, Fraunces, Source Serif 4, IBM Plex Mono (SIL Open Font License).

## Citation

Hotham, T. (2026) Avon means river: the old roots and everyday words of British river names. Zenodo. {{https://doi.org/10.5281/zenodo.24063209}}

Dr Tristan Hotham, Independent researcher. ORCID 0000-0003-4931-9349.

{AI}
"""
for bad in ("—", "–", "--", "DSIT", "DCMS"):
    assert bad not in "\\n".join(l for l in readme.replace("```", "").splitlines() if not l.startswith("|---")), bad
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(readme)
lic = open("/home/claude/studies/animal-place-names/LICENSE", encoding="utf-8").read()
lic = lic.split("Text and figures:")[0] + """Text and figures: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), Tristan Hotham, 2026.
River and place data (data/watercourses.csv, root_rivers.csv, borrowed_names.csv, rivers.json, rootpts.json, places.json): derived from OpenStreetMap, © OpenStreetMap contributors, Open Database Licence 1.0 (https://opendatacommons.org/licenses/odbl/1-0/).
Other derived data (results.json, major_rivers_england.csv, generic_by_county.csv, generic_grid.csv): CC BY 4.0.
The map engine is loaded from the ink-map study (MIT code; credits in its README). Fonts under the SIL Open Font License.
"""
open(os.path.join(ROOT, "LICENSE"), "w", encoding="utf-8").write(lic)
post = f"""**Title:** [OC] Avon means river: {R['towns']['english_pc']:.0f}% of England's towns have English names, but {M['pre']} of its 60 biggest mapped rivers kept names older than English

**Body:**

Avon is the old Brittonic word for river (Welsh afon), so Stratford-upon-Avon is on the River River. When English speakers arrived they renamed nearly every village but kept most big river names. I mapped {R['n']['watercourses']:,} named rivers and streams from OpenStreetMap by the words in their names.

- 60 largest English rivers in the data (ranked by mapped extent): {M['pre']} Brittonic or older (Thames, Trent, Severn, Avon, Exe...), {M['english']} English (several invented later from towns: Arun from Arundel, Mole from Molesey), {M['uncertain']} debated.
- {R['avon_rivers']} Avons, {R['esk_rivers']} Esks, {R['calder_rivers']} Calders.
- The stream word follows the old language borders: allt in the Highlands, burn in the Lowlands, nant in Wales, brook in the Midlands, and the Norse beck in the north.
- At the same latitude, {D['east']['beck_pc']:.0f}% of streams are becks in Lincolnshire and Nottinghamshire, {D['west']['beck_pc']:.0f}% in Cheshire, Staffordshire, Shropshire and Greater Manchester: not one beck in {D['west']['brook']} brooks. Derbyshire and Leicestershire, also Danelaw, are brook country too.

Interactive map (switch between stream words and old roots, tap any river): {PAGE}

**Source comment:**

Data: OpenStreetMap contributors (ODbL) via QLever. Etymologies: Ekwall, English River-Names (1928); Watts, Cambridge Dictionary of English Place-Names (2004); Mills, Dictionary of British Place-Names (2011). Tools: Python (pandas, geopandas, matplotlib), MapLibre. Every rule and hand decision is in the repo: {REPO}
"""
for bad in ("—", "–", "--"):
    assert bad not in post, bad
open(os.path.join(ROOT, "reddit", "post.md"), "w", encoding="utf-8").write(post)
print("README, LICENSE, post written")
