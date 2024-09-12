# main.py

import sys
from PyQt6.QtWidgets import QApplication
from business_logic import StudiumManager
from data_access import DataAccess
from gui import Dashboard

def main():
    # Initialisiere die Anwendung
    app = QApplication(sys.argv)

    # Erstelle den StudiumManager und lade die Daten
    studium_manager = StudiumManager()
    studium_manager.studenten = DataAccess.load_data()

    # Erstelle und zeige das Dashboard
    dashboard = Dashboard(studium_manager)
    dashboard.show()

    # Aktualisiere die Benutzeroberfläche
    dashboard.update_student_combo()
    dashboard.update_ui()

    # Starte die Ereignisschleife
    sys.exit(app.exec())

if __name__ == "__main__":
    main()