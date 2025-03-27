import sys
from model import TournamentModel
from controller import TournamentController
from view import TournamentView
from PyQt5.QtWidgets import (QApplication)



# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TournamentView()
    controller = TournamentController(TournamentModel(), window)
    window.show()
    sys.exit(app.exec_())