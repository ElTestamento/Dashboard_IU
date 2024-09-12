# logic.py

from entities import Student, Modul, AVAILABLE_MODULES


class StudiumManager:
    def __init__(self):
        self.studenten = [] # Liste von Studenten die zu managen sind. Geladen aus der JSON. Gespeichert in der JSON
        self.current_student = None

    def add_student(self, vorname, nachname, matrikelnummer):
#Fügt einen neuen Studenten hinzu
        student = Student(vorname, nachname, matrikelnummer)
        self.studenten.append(student)
        self.current_student = student
        return student

    def select_student(self, matrikelnummer):
#Wählt einen Studenten anhand der Matrikelnummer aus
        for student in self.studenten:
            if student.matrikelnummer == matrikelnummer:
                self.current_student = student
                return student
        return None

    def add_module(self, semester_num, modul_name):
#Fügt ein Modul zu einem bestimmten Semester hinzu
        if self.current_student and modul_name in AVAILABLE_MODULES:
            # Prüfen, ob das Modul bereits in irgendeinem Semester existiert
            for semester in self.current_student.semester:
                if any(m.name == modul_name for m in semester.module):
                    return False

            modul = Modul(modul_name)
            self.current_student.semester[semester_num - 1].module.append(modul)
            return True
        return False

    def complete_module(self, semester_num, modul_index, note):
#Schließt ein Modul ab und setzt die Note
        if self.current_student:
            modul = self.current_student.semester[semester_num - 1].module[modul_index]
            modul.note = note
            if 1.0 <= note <= 4.0:
                modul.status = "bestanden"
            else:
                modul.status = "durchgefallen"
            return True
        return False

    def calculate_average_grade(self):
#Berechnet die Durchschnittsnote über alle Semester
        if not self.current_student:
            return None

        total_grade = 0
        total_ects = 0
        for semester in self.current_student.semester:
            for modul in semester.module:
                if modul.status == "bestanden":
                    total_grade += modul.note * modul.ects
                    total_ects += modul.ects

        if total_ects > 0:
            return total_grade / total_ects
        return None

    def calculate_total_ects(self):
#Berechnet die Gesamtanzahl der ECTS-Punkte
        if not self.current_student:
            return 0

        total_ects = 0
        for semester in self.current_student.semester:
            for modul in semester.module:
                if modul.status == "bestanden":
                    total_ects += modul.ects
        return total_ects

    def get_semester_ects(self, semester_num):
#Berechnet die verbrauchten und verbleibenden ECTS-Punkte für ein Semester
        if not self.current_student:
            return 0, 30

        semester = self.current_student.semester[semester_num - 1]
        used_ects = sum(modul.ects for modul in semester.module if modul.status == "bestanden")
        remaining_ects = 30 - used_ects
        return used_ects, remaining_ects

    def get_study_status(self):
#Ermittelt den Studienstatus basierend auf der Durchschnittsnote
        avg_grade = self.calculate_average_grade()
        if avg_grade is None:
            return "gelb"
        elif avg_grade <= 3.0:
            return "grün"
        elif avg_grade <= 4.0:
            return "gelb"
        else:
            return "rot"