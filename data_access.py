# data_access.py

import json
from entities import Student

class DataAccess:
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