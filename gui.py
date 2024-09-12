# gui.py

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QLabel, QTabWidget, QDialog, QDialogButtonBox, QFormLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QInputDialog, QMessageBox,
                             QProgressBar, QSizePolicy, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from entities import AVAILABLE_MODULES
from data_access import DataAccess

class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Student hinzufügen")
        self.setFixedSize(300, 200)

        layout = QFormLayout(self)
        self.vorname_input = QLineEdit(self)
        self.nachname_input = QLineEdit(self)
        self.matrikelnummer_input = QLineEdit(self)

        layout.addRow("Vorname:", self.vorname_input)
        layout.addRow("Nachname:", self.nachname_input)
        layout.addRow("Matrikelnummer:", self.matrikelnummer_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_inputs(self):
        return self.vorname_input.text(), self.nachname_input.text(), self.matrikelnummer_input.text()


class ModulDialog(QDialog):
    def __init__(self, available_modules, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modul hinzufügen")
        self.setFixedSize(300, 100)

        layout = QVBoxLayout(self)
        self.modul_combo = QComboBox(self)
        self.modul_combo.addItems(available_modules)

        layout.addWidget(QLabel("Modul:"))
        layout.addWidget(self.modul_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_inputs(self):
        return self.modul_combo.currentText()


class SemesterTab(QWidget):
    def __init__(self, semester_number, available_modules, studium_manager, parent=None):
        super().__init__(parent)
        self.semester_number = semester_number
        self.available_modules = available_modules
        self.studium_manager = studium_manager
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.add_module_button = QPushButton("Modul hinzufügen")
        self.add_module_button.clicked.connect(self.add_module)
        layout.addWidget(self.add_module_button)

        self.module_table = QTableWidget(0, 4)
        self.module_table.setHorizontalHeaderLabels(["Modul", "ECTS", "Note", "Status"])
        self.module_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.module_table)

        self.ects_label = QLabel("Verbrauchte ECTS: 0 / Verbleibende ECTS: 30")
        layout.addWidget(self.ects_label)

    def add_module(self):
        # Filtere die bereits ausgewählten Module
        selected_modules = set(
            modul.name for semester in self.studium_manager.current_student.semester for modul in semester.module)
        available_modules = [m for m in self.available_modules if m not in selected_modules]

        if not available_modules:
            QMessageBox.warning(self, "Fehler", "Alle Module wurden bereits ausgewählt.")
            return

        dialog = ModulDialog(available_modules, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            modul_name = dialog.get_inputs()
            if modul_name and self.studium_manager.add_module(self.semester_number, modul_name):
                self.update_module_table()
                self.update_ects()
                self.window().update_ui()
            else:
                QMessageBox.warning(self, "Fehler", f"Das Modul '{modul_name}' konnte nicht hinzugefügt werden.")

    def complete_module(self, row):
        note, ok = QInputDialog.getDouble(self, "Note eingeben", "Note (1.0 - 5.0):", 1.0, 1.0, 5.0, 1)
        if ok:
            if self.studium_manager.complete_module(self.semester_number, row, note):
                self.update_module_table()
                self.update_ects()
                self.window().update_ui()
            else:
                QMessageBox.warning(self, "Fehler", "Modul konnte nicht abgeschlossen werden.")

    def update_module_table(self):
        self.module_table.setRowCount(0)
        semester = self.studium_manager.current_student.semester[self.semester_number - 1]
        for index, modul in enumerate(semester.module):
            self.module_table.insertRow(index)
            self.module_table.setItem(index, 0, QTableWidgetItem(modul.name))
            self.module_table.setItem(index, 1, QTableWidgetItem(str(modul.ects)))
            self.module_table.setItem(index, 2, QTableWidgetItem(str(modul.note) if modul.note else "-"))
            self.module_table.setItem(index, 3, QTableWidgetItem(modul.status))
            if modul.status == 'aktiv':
                complete_button = QPushButton("Abschließen")
                complete_button.clicked.connect(lambda _, r=index: self.complete_module(r))
                self.module_table.setCellWidget(index, 3, complete_button)

    def update_ects(self):
        used_ects, remaining_ects = self.studium_manager.get_semester_ects(self.semester_number)
        self.ects_label.setText(f"Verbrauchte ECTS: {used_ects} / Verbleibende ECTS: {remaining_ects}")


class Dashboard(QMainWindow):
# Erstellt das Hauptfenster
    def __init__(self, studium_manager):
        super().__init__()
        self.studium_manager = studium_manager
        self.setWindowTitle("Studium Monitor")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #E6F3FF;")
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Oberer Bereich
        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)

        # Linker oberer Bereich
        student_frame = QFrame()
        student_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        student_layout = QVBoxLayout(student_frame)
        top_layout.addWidget(student_frame)

        self.add_student_button = QPushButton("Student hinzufügen")
        self.add_student_button.clicked.connect(self.add_student)
        student_layout.addWidget(self.add_student_button)

        self.select_student_combo = QComboBox()
        self.select_student_combo.currentIndexChanged.connect(self.select_student)
        student_layout.addWidget(self.select_student_combo)

        self.student_info_label = QLabel("Vorname: \nNachname: \nMatrikelnummer: ")
        student_layout.addWidget(self.student_info_label)

        # Rechter oberer Bereich
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        info_layout = QVBoxLayout(info_frame)
        top_layout.addWidget(info_frame)

        self.average_grade_label = QLabel("Durchschnittsnote: -")
        self.average_grade_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        info_layout.addWidget(self.average_grade_label)

        self.total_ects_label = QLabel("Gesamt ECTS: 0 / 180")
        info_layout.addWidget(self.total_ects_label)

        self.study_status_label = QLabel("Status")
        self.study_status_label.setFixedSize(100, 50)
        self.study_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.study_status_label.setStyleSheet("font-weight: bold; color: white; border-radius: 10px;")
        info_layout.addWidget(self.study_status_label)

        # Fortschrittsbalken
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 36)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p% (%v von %m Module abgeschlossen)")
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Semester-Tabs
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        for i in range(1, 7):
            self.tab_widget.addTab(SemesterTab(i, AVAILABLE_MODULES, self.studium_manager), f"Semester {i}")

        self.exit_button = QPushButton("Beenden")
        self.exit_button.clicked.connect(self.close_application)
        layout.addWidget(self.exit_button)

    def add_student(self):
        dialog = AddStudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            vorname, nachname, matrikelnummer = dialog.get_inputs()
            if vorname and nachname and matrikelnummer:
                self.studium_manager.add_student(vorname, nachname, matrikelnummer)
                self.update_student_combo()
                self.update_ui()
            else:
                QMessageBox.warning(self, "Fehler", "Bitte geben Sie alle Informationen ein.")

    def select_student(self, index):
        if index >= 0:
            student = self.studium_manager.studenten[index]
            self.studium_manager.select_student(student.matrikelnummer)
            self.update_ui()

    def update_student_combo(self):
        self.select_student_combo.clear()
        for student in self.studium_manager.studenten:
            self.select_student_combo.addItem(f"{student.vorname} {student.nachname} ({student.matrikelnummer})")

    def update_ui(self):
# Aktualisiere die gesamte Benutzeroberfläche
        if self.studium_manager.current_student:
            student = self.studium_manager.current_student
            self.student_info_label.setText(
                f"Vorname: {student.vorname}\nNachname: {student.nachname}\nMatrikelnummer: {student.matrikelnummer}")

            avg_grade = self.studium_manager.calculate_average_grade()
            self.average_grade_label.setText(
                f"Durchschnittsnote: {avg_grade:.2f}" if avg_grade else "Durchschnittsnote: -")

            total_ects = self.studium_manager.calculate_total_ects()
            self.total_ects_label.setText(f"Gesamt ECTS: {total_ects} / 180")

            status = self.studium_manager.get_study_status()
            self.study_status_label.setText(status.upper())
            if status == "grün":
                self.study_status_label.setStyleSheet(
                    "background-color: #4CAF50; font-weight: bold; color: white; border-radius: 10px;")
            elif status == "gelb":
                self.study_status_label.setStyleSheet(
                    "background-color: #FFEB3B; font-weight: bold; color: black; border-radius: 10px;")
            else:
                self.study_status_label.setStyleSheet(
                    "background-color: #F44336; font-weight: bold; color: white; border-radius: 10px;")

            completed_modules = sum(
                1 for semester in student.semester for modul in semester.module if modul.status == "bestanden")
            self.progress_bar.setValue(completed_modules)

            for i in range(6):
                self.tab_widget.widget(i).update_module_table()
                self.tab_widget.widget(i).update_ects()
        else:
            self.student_info_label.setText("Vorname: \nNachname: \nMatrikelnummer: ")
            self.average_grade_label.setText("Durchschnittsnote: -")
            self.total_ects_label.setText("Gesamt ECTS: 0 / 180")
            self.study_status_label.setText("N/A")
            self.study_status_label.setStyleSheet(
                "background-color: grey; font-weight: bold; color: white; border-radius: 10px;")
            self.progress_bar.setValue(0)


# Fügen Sie diese Methode zur Dashboard-Klasse hinzu

    def save_data(self):
        DataAccess.save_data(self.studium_manager.studenten)


# Ändern Sie den Konstruktor der Dashboard-Klasse
    def __init__(self, studium_manager):
        super().__init__()
        self.studium_manager = studium_manager
        self.setWindowTitle("Studium Monitor")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #E6F3FF;")
        self.initUI()

    # Verbinde das 'closeEvent' mit der Speichermethode
        self.closeEvent = self.save_and_close
    def save_and_close(self, event):
        self.save_data()
        event.accept()


    def close_application(self):
        # Speichern der Daten
        DataAccess.save_data(self.studium_manager.studenten)
        # Schließen der Anwendung
        QApplication.instance().quit()


# Überschreiben des closeEvent, um sicherzustellen, dass die Daten auch beim Schließen des Fensters gespeichert werden
    def closeEvent(self, event):
        self.close_application()
        event.accept()