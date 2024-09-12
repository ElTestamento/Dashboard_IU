# entities.py

class Student:
    def __init__(self, vorname, nachname, matrikelnummer):
        self.vorname = vorname
        self.nachname = nachname
        self.matrikelnummer = matrikelnummer
        self.semester = [Semester(i) for i in range(1, 7)]

    def to_dict(self):
        return {
            'vorname': self.vorname,
            'nachname': self.nachname,
            'matrikelnummer': self.matrikelnummer,
            'semester': [semester.to_dict() for semester in self.semester]
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data['vorname'], data['nachname'], data['matrikelnummer'])
        student.semester = [Semester.from_dict(sem_data) for sem_data in data['semester']]
        return student

class Modul:
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

# Liste der verfügbaren Module
AVAILABLE_MODULES = ["Mathe 1", "Mathe 2", "Intro AI", "Mathe 3", "Mathe 4", "Ethik", "OOP", "Cloud 1", "Cloud 2"]