# river-names: working notes

Brief: /home/claude/work/new9/BRIEFS.md (study 6) + shared rules in /home/claude/work/new8/BRIEFS.md and /home/claude/newdata/BRIEF.md.
Format refs: studies/church-orientation, studies/sunless-valleys; page engine and code layout copied from studies/animal-place-names (same batch).
Work files: /home/claude/scratch/river-names (delete at the end).

## Pipeline
01_rivers.py (OSM ways -> watercourses: same normalised name + type, start points chained within 15/8/4 km)
-> 02_classify.py (generics.py split, roots.py root regexes, overrides.csv, places, names borrowed from rivers)
-> 03_analysis.py (root_rivers_by_hand.csv, results.json, data files) -> 04_export.py -> 05_figures.py -> 06_build_site.py
-> 07_paper.py -> reddit/collage.py -> 09_readme.py -> 08_release.py -> qa.js

## Data checks (whole set)
- Every root match (243 watercourses) read by eye (WORK/review_roots.txt, with coordinates). 22 false friends removed in
  overrides.csv (Kent Water/Ditch/Brook named after the county; minor Allen/Ouse/Wey streams; Nant Thames; Trent Brook Dorset).
- OSM splits rivers into pieces (gaps, stream-tagged upper course, Welsh names Hafren/Dyfrdwy/Wysg) and automatic joining
  either fragmented (6 km) or wrongly merged (15 km joined the Salisbury Avon into the Bristol Avon). So every one of the 243
  root pieces was assigned to its river by hand from its position: code/root_rivers_by_hand.csv (116 rivers). Notable: the
  Dart near Tiverton is a separate river from the Devon Dart; Afon Hafren (Carmarthenshire) and Nant Hafren (Ceredigion) are
  not the Severn; Avon Water (Lymington) is separate from the Hampshire Avon.
- Generic split checked on the commonest names; 'other' (no generic) = 5,474 watercourses.
- Borrowed names: only rivers with a root or ORIGIN 'pre'; travellers' sites, farms, halls, junctions removed. Direction can
  run the other way (Penk from Penkridge): stated as a caveat; text quotes only Exeter, Dartmouth, Dartington, Alnwick,
  Tynemouth, Doncaster, Thame, Frome, Usk (asserted in 06_build_site.py).

## References and claims to verify (cited from memory)
- Ekwall, E. (1928) English River-Names. Oxford: Clarendon Press.
- Watts, V. (ed.) (2004) The Cambridge Dictionary of English Place-Names. CUP.
- Mills, A. D. (2011) A Dictionary of British Place-Names, rev. edn. OUP.
- Gelling, M. and Cole, A. (2000) The Landscape of Place-Names. Shaun Tyas.
- Owen, H. W. and Morgan, R. (2007) Dictionary of the Place-Names of Wales. Gomer.
- Watson, W. J. (1926) The History of the Celtic Place-Names of Scotland. Blackwood.
- Bast, H. and Buchhold, B. (2017) QLever: a query engine for efficient SPARQL+Text search. CIKM 2017, 647 to 656.
- The ORIGIN classes in code/roots.py (60 largest English rivers: 37 pre-English, 10 English, 13 uncertain) are from memory of
  Ekwall/Watts and need a spot check, especially: Ure, Yare, Lea, Soar, Dove, Brue, Aire, Nene (pre); Welland, Wharfe, Ribble,
  Stour, Witham, Parrett, Test, Swale, Bure (uncertain); back-formations Arun (Arundel), Rother (Rotherbridge), Mole (Molesey),
  Lark (Lackford), Roding (Roding villages); Mersey 'boundary river'; Otter (OE otor).
- Root meanings (roots.py): Avon 'river'; isca 'water' (Esk, Exe, Axe, Usk); Derwent 'oak'; Dee 'goddess'; Calder 'hard water';
  Leven 'smooth'; Frome 'fair, brisk'; Tam- 'dark' (marked debated); Scottish Avons possibly Gaelic Athfhinn (marked probable).
- 'Danelaw' wording: Derbyshire, Nottinghamshire, Leicestershire, Lincolnshire = Five Boroughs territory; check phrasing.

## Log
- All steps done. Headline: 37/60 big English rivers pre-English vs 73% of towns English/Norse; 10 Avons, 10 Esks, 15 Calders;
  beck majority north of 53.75N; east Midlands 26% beck vs west 0% (0 of 755).

## Independent review (2026)
- Pipeline reran from raw: outputs identical before changes.
- Fixed: beck comparison pooled Derbyshire/Leicestershire (0 and 2 becks) into the "east" 26%, contradicting the text's own
  point; east is now Lincolnshire + Nottinghamshire (115 becks to 26 brooks, 82%), Derbyshire + Leicestershire reported
  separately (2 to 300), west 0 of 755 (no beck way at all in the raw data for the western counties or Derbyshire).
- Fixed: the ranked Rother is the eastern (East Sussex) Rother, a back-formation from Rotherfield, not Rotherbridge.
- Fixed: origin_major in watercourses.csv / popups now only on the ranked watercourse (the Derbyshire Rother was labelled English).
- Fixed wording: "every stream is a burn or a water" (Borders/D&G also have sikes, gills); Wales and Highland shares are of
  the named generics, not all streams; *isca "usually read as" water; Cherwell first element uncertain; 60 largest is "in the
  data" with the Eden (Cumbria) noted as missing because OSM maps it in few long ways.
