# Avon means river

The old roots and everyday words of the river names of the United Kingdom. 128,210 named OpenStreetMap waterway stretches joined into 32,068 named rivers, streams and canals; every name split into a generic word (river, afon, allt, burn, beck, brook...) and a specific name; specific names matched against sixteen Brittonic or older root groups after Ekwall's English River-Names (1928), with every piece of the 116 root rivers assigned to its river by hand.

Interactive page: https://maps.tristanhotham.com/river-names/
Paper: https://doi.org/10.5281/zenodo.24063209
Blog post: https://blog.tristanhotham.com/2026/10/31/river-names/
Code and data: https://github.com/Tristan-Hotham/river-names

## Headline results

- Of the 60 largest English rivers in the data, 37 have names traced to Brittonic or older sources, 10 English (several late back-formations from towns: Arun, Rother, Mole, Lark) and 13 uncertain; 9 of the largest ten are pre-English. Meanwhile 73% of England's 1,184 towns and cities have a first word ending in an English or Norse element.
- 10 Avons (6 in England, 4 in Scotland), 10 Esks, 6 Derwents, Darwens and Darents, 15 Calders.
- Generic words follow the old language frontiers: 86% nant or afon in Wales; Gaelic allt or abhainn 86% of allt, abhainn, burn and water names in Highland, 0% in the Borders and Dumfries and Galloway.
- The beck line: becks outnumber brooks in England north of about 53.75°N. At similar latitudes, 82% becks in Lincolnshire and Nottinghamshire against 0% (0 of 755) in Cheshire, Staffordshire, Shropshire and Greater Manchester; Derbyshire and Leicestershire, also in the Danelaw, have 2 becks to 300 brooks.
- 123 towns and villages within 6 km of 45 old-named rivers carry the river's name (Exeter, Dartmouth, Alnwick, Doncaster...).

## Files

| File | What it is |
|---|---|
| `index.html`, `js/page.js` | The interactive page: the Inked World map style (loaded from the ink-map study on the same site), every named river and stream coloured by its generic word, or the courses of the old-root rivers; pickers, search and popups. |
| `header.png` | Social card, 1200 x 630. |
| `data/watercourses.csv` | Every named watercourse (32,068): first OSM way, name, Welsh and Gaelic names, type, generic, specific, root, reading, river (for root rivers), number of ways, spread, county, nation, position. ODbL. |
| `data/root_rivers.csv` | The 116 distinct rivers and streams in the root groups. ODbL. |
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
- Roots: sixteen groups after Ekwall (1928), Watts (2004) and Mills (2011), matched on the specific name or the Welsh name; 22 hand removals; each piece of each root river assigned to its river by hand.
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

Hotham, T. (2026) Avon means river: the old roots and everyday words of British river names. Zenodo. https://doi.org/10.5281/zenodo.24063209

Dr Tristan Hotham, Independent researcher. ORCID 0000-0003-4931-9349.

I wrote the text, with drafting and editing assistance from Claude (Anthropic), which also helped prepare the analysis code. I reviewed and checked all text and results.
