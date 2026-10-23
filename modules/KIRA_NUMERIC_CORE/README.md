# KIRA NUMERIC CORE 0.1 — inkrementelle Korrektur

## Grundsatz
Der fundamentale numerische Kern kennt **keine Knoten, Kanten, Geometrie oder Topologie**. Ein Eintrag besitzt eine opaque, dauerhafte Identität und einen exakten rationalen Wert. Die Differenz zweier Identifikatoren hat **keine** semantische Bedeutung. Numerische Nähe ist nur für explizite Werte definiert, nicht für Hashes oder IDs.

## Neu implementiert
- `numeric_core.py`: `Fraction`-basierte exakte rationale Werte, numerische Bereichssuche, unveränderliche IDs, persistente Evidenz mit Quellen, keine automatische Überschreibung bei Widerspruch.
- `efficient_core.py`: optionale numerische Schnittstelle `observe_numeric`/`query_numeric` in derselben SQLite-Datei; bisheriger Token- und Graphpfad bleibt vorerst aus Kompatibilitätsgründen erhalten.
- Sieben Tests (sechs Numerik, einer Integration). Die Integration deckte einen realen Tabellen-Namenskonflikt mit der Alt-Runtime auf, der durch `numeric_*`-Namensräume behoben wurde.

## Wichtige Grenzen / nächste Migration
- **Noch kein Ersatz des graphbasierten `binary_learning.py`.** Der bisherige Graphpfad bleibt eine Legacy-Spezialisierung und darf nicht als fundamentales RRM-Modell interpretiert werden.
- Die numerische Bereichssuche ist `O(log n + k)` im RAM (sortierte Liste); das **Einfügen ist O(n)** durch Verschieben in der Python-Liste. Damit ist die Forderung nach durchgängig subquadratischem inkrementellem Lernen noch NICHT erfüllt. Ein B-Baum/SQLite-Bereichsindex oder segmentierte geordnete Struktur ist nötig.
- Alle numerischen Einträge werden derzeit für den Bereichsindex in den RAM geladen; kein Out-of-Core-Benchmark.
- Kein Modell, das aus bloßer numerischer Nähe automatisch semantisch richtige Relationen lernt. Das muss empirisch validiert werden.
- Für IDs bleiben alte RRM-Records und ihre Hash-/Referenzsemantik unverändert; sie sind keine numerischen Ähnlichkeitskoordinaten.
- Noch keine Migration bestehender Graph-Evidenz auf ein mathematisch definiertes rein numerisches Lernverfahren. Das wäre ohne konkrete Abbildungsregel ein unzulässiger Bedeutungswechsel.
- Die zwei SQLite-Verbindungen teilen eine Datei, aber nicht eine atomare Transaktion über beide Teilpfade.

## Test
`PYTHONPATH=.:RRM_UNIFIED_0_1 python -m unittest -v test_numeric_core test_integration`

Das Paket ist ein **erster integrierter Migrationsschritt**, keine fertige rein numerische Kira.
