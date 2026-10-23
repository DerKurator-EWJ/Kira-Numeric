# KIRA EFFICIENT CORE 0.1 — selektive Spezialisierung

**Ziel:** Allgemeine Identität/Persistenz nur dort teilen, wo es sich lohnt; spezialisierte Algorithmen nicht aus Prinzip ersetzen.

## Umsetzung
- Ein SQLite-Dateipfad, eine DB-Verbindung pro Core-Instanz; RRM-Binärrecords und FOUNDATIONs unveränderter `TransitionPredictor` verwenden diese Verbindung.
- Typgesteuertes, konstantes Routing: Integer-Token -> FOUNDATION-Übergangsindex; Graph `{nodes,edges}` -> RRM-Binärlernoperator. Keine lernende Kostenbewertung, kein neuer allgemeiner Lernoperator.
- Streams nach Modalität getrennt; Token-Verlauf als begrenzter RAM-Tail mit Wiederherstellung aus dem persistenten Protokoll; Transaktionen und Neustart geprüft.
- Kein Bridge-Doppel-Snapshot, keine separate SQLite-Datei pro Subsystem.
- Für einen reproduzierbaren, kleinen Prototyp nur benötigte Teile von FOUNDATION (prediction.py) und RRM CORE übernommen. Keine Behauptung, dass sämtliche FOUNDATION-Fähigkeiten migriert sind.

## Testen (Python 3, Standardbibliothek)
Windows: `set PYTHONPATH=.;RRM_UNIFIED_0_1` dann `python -m unittest -v test_efficient` und `python benchmark.py`.
Linux: `PYTHONPATH=.:RRM_UNIFIED_0_1 python -m unittest -v test_efficient`.

## Messung
`results.json`: fünf lokale Wiederholungen, 80 Ereignisse, SQLite, winzige synthetische Aufgaben. **Nicht streng gleichwertige Commit-Strategien:** spezialisierte Baseline schreibt im Batch; `EfficientCore.observe` committet jedes Token für garantierte Persistenz. Startup, Schema und Transaktionskosten dominieren. Deshalb sind die absoluten Trainingszeiten **kein fairer Geschwindigkeitsvergleich**. Graph-Baseline und gerouteter Graph verwenden denselben RRM-Lernalgorithmus. Der zusätzliche Routingaufwand ist klein, aber nicht null.

## Grenzen
- Nur Token als Integer, Graphen mit bereits ausgerichteten Kanten; keine universelle Sprach-, Audio- oder Videoverarbeitung.
- `TransitionPredictor` benötigt ein SQL-JSON-Kontextfeld; vollständig binäres Wissen ist nicht erzwungen, da der Spezialpfad sonst schlechter würde.
- SQLite-Persistenz ist kein Nachweis der Effizienz bei großen Datenmengen; Memory/RSS und komplexe Generalisierung fehlen.
- Gemischte Beobachtungen über Token- und Graphroute werden nicht automatisch miteinander verknüpft. Keine selbstlernende Pfadwahl.
