# entities.py
# In dieser Datei werden die tatsächlichen Entity-Klassen gebündelt: Student, Modul und Semester
class Student:
# Die Student-Klasse repräsentiert einen Studenten im System mit grundlegenden Attributen wie Vorname, Nachname und Matrikelnummer.
# Bei der Instanziierung werden automatisch sechs Semester-Objekte erstellt und dem Studenten zugeordnet.
# Die Klasse macht über zwei Metoden dieses Objekt speicherbar (to_dict()) und lesbar (from_dict())
# Durch die Verwendung der @classmethod-Dekoration für from_dict() wird eine alternative Konstruktionsmethode bereitgestellt
# die es ermöglicht, ein Studenten-Objekt direkt aus einem Dictionary zu erstellen.
    def __init__(self, vorname, nachname, matrikelnummer):
# Hier wird die Instanz der Studentenklasse initialisiert
        self.vorname = vorname
        self.nachname = nachname
        self.matrikelnummer = matrikelnummer
        self.semester = [Semester(i) for i in range(1, 7)]

    def to_dict(self):
# Macht aus dem Studenten-Objekt eine Dictionary.
        return {
            'vorname': self.vorname,
            'nachname': self.nachname,
            'matrikelnummer': self.matrikelnummer,
            'semester': [semester.to_dict() for semester in self.semester]
        }

    @classmethod
    def from_dict(cls, data):
# Macht aus dem Dictionary wieder eine Objekt
        student = cls(data['vorname'], data['nachname'], data['matrikelnummer'])
        student.semester = [Semester.from_dict(sem_data) for sem_data in data['semester']]
        return student

class Modul:
# Die Modul-Klasse funktioniert analog zu der Erläuterung der Studenten-Klasse
    def __init__(self, name, ects=5):
        self.name = name
        self.ects = ects
        self.note = None
        self.status = "aktiv"

    def to_dict(self):
        return {
            'name': self.name,
            'ects': self.ects,
            'note': self.note,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        modul = cls(data['name'], data['ects'])
        modul.note = data['note']
        modul.status = data['status']
        return modul

class Semester:
# Die Semester-Klasse funktioniert analog zu der Erläuterung der Studenten-Klasse
    def __init__(self, nummer):
        self.nummer = nummer
        self.module = []

    def to_dict(self):
        return {
            'nummer': self.nummer,
            'module': [modul.to_dict() for modul in self.module]
        }

    @classmethod
    def from_dict(cls, data):
        semester = cls(data['nummer'])
        semester.module = [Modul.from_dict(modul_data) for modul_data in data['module']]
        return semester

# Liste der verfügbaren Module: Dies ist eine Konstante - folgt der Konvention.
# Diese Liste kann in verschiedenen Teilen des Programms wiederverwendet werden, ohne den Code zu duplizieren.
AVAILABLE_MODULES = ["Mathe 1", "Mathe 2", "Intro AI", "Mathe 3", "Mathe 4", "Ethik", "OOP", "Cloud 1", "Cloud 2"]