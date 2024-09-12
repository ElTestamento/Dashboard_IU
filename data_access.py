# data_access.py
# In dieser Datei ist das Objekte "DataAccess" zur Datenverwaltung gekapselt.

import json
from entities import Student

class DataAccess:
# Die save_data-Methode konvertiert jedes Studenten-Objekt in ein Dictionary und speichert die resultierende Liste in einer JSON-Datei.
# Vorhersehbare Fehler werden in einem Try and Catch Block abgefangen.
# Die load_data-Methode liest Daten aus einer JSON-Datei, konvertiert sie zurück in Studenten-Objekte
# Beide Methoden sind als statische Methoden implementiert.
    @staticmethod
    def save_data(studenten, filename='studenten_data.json'):
        """Speichert die Studentendaten in einer JSON-Datei."""
        data = [student.to_dict() for student in studenten]
        try:
            with open(filename, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Fehler beim Speichern der Daten: {str(e)}")

    @staticmethod
    def load_data(filename='studenten_data.json'):
        """Lädt die Studentendaten aus einer JSON-Datei."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            return [Student.from_dict(student_data) for student_data in data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Die Datei konnte nicht gelesen werden. Sie könnte beschädigt sein.")
            return []
        except Exception as e:
            print(f"Fehler beim Laden der Daten: {str(e)}")
            return []