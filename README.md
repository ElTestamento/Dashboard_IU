# Dashboard_IU

Studium Monitor – Dashboard
Desktop-Anwendung zur Verwaltung und Visualisierung des Studienverlaufs. Entwickelt mit Python und PyQt6.
Features

Mehrere Studenten verwaltbar mit Matrikelnummer
6 Semester-Tabs mit Modulverwaltung und ECTS-Tracking (max. 30 ECTS/Semester, 180 gesamt)
Notenerfassung mit gewichtetem Notendurchschnitt (ECTS-gewichtet)
Studienstatus als Ampelindikator (grün / gelb / rot)
Fortschrittsbalken über alle 36 abschließbaren Module
Persistenz via JSON (automatisches Speichern beim Beenden)

Projektstruktur
├── main.py          # Einstiegspunkt – initialisiert App, lädt Daten
├── logic.py         # StudiumManager – Anwendungslogik
├── gui.py           # Dashboard, SemesterTab, Dialoge (PyQt6)
├── entities.py      # Datenmodelle: Student, Modul, AVAILABLE_MODULES
└── data_access.py   # JSON-Persistenz (laden/speichern)
Installation
bashpip install PyQt6
python main.py
