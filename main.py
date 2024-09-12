# main.py
# Importiert alle notwendigen Module
import sys
from PyQt6.QtWidgets import QApplication
from logic import StudiumManager
from data_access import DataAccess
from gui import Dashboard

def main():
    # Initialisiere die QApplication für PyQt6
    # sys.argv übergibt Kommandozeilenargumente an die Anwendung
    app = QApplication(sys.argv)

    # Erstelle eine Instanz des StudiumManagers
    # StudiumManager repräsentiert die Anwendungslogik
    studium_manager = StudiumManager()

    # DataAccess.load_data() liest gespeicherte Studentendaten
    # und gibt sie als Liste von Studenten-Objekten zurück
    studium_manager.studenten = DataAccess.load_data()

    # Erstelle das Hauptfenster der Anwendung
    # und über gibt die erstelle Instanz von StudiumManager mit den geladenen Daten
    dashboard = Dashboard(studium_manager)

    # Zeige das Dashboard-Fenster an
    dashboard.show()

    # Aktualisiere die Dropdown-Liste der Studenten im Dashboard über die
    # Methode update_student_combo aus der Dashboard-Klasse
    # Dies füllt die Combobox mit den Namen der geladenen Studenten
    dashboard.update_student_combo()

    # Aktualisiere die gesamte Benutzeroberfläche über die Methode update_ui
    # aus der Dashboard-Klasse
    dashboard.update_ui()

    # Starte die Ereignisschleife in PyQt6
    sys.exit(app.exec())

if __name__ == "__main__":
    main()