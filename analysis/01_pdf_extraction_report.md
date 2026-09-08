# Rapport d'extraction PDF

Extraction déterministe réalisée avec PyMuPDF (`pymupdf`) depuis `Reflections_PierreCampergue.pdf`.

- Pages PDF: 562
- Fichier paginé: `corpus/extracted/Reflections_PierreCampergue.pages.jsonl`
- Texte brut: `corpus/raw/Reflections_PierreCampergue.txt`
- Provenance: chaque ligne JSON contient document, page_pdf et texte original extrait.
- OCR: non utilisé.

Limites à vérifier ultérieurement: formules et tableaux peuvent perdre leur mise en page; une inspection ciblée des pages courtes et des figures reste nécessaire.
