from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
                             QComboBox, QDialog, QLabel, QCalendarWidget, QMessageBox,
                             QToolBar, QAction, QFileDialog, QTreeWidget, QTreeWidgetItem)

#Контроллер (Controller)
class TournamentController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def add_tournament(self, name, date, sport, winner, prize_money):
        try:
            prize_money = float(prize_money)
            self.model.add_tournament(name, date, sport, winner, prize_money)
            self.view.update_display()
        except ValueError:
            QMessageBox.critical(self.view, "Ошибка", "Размер призовых должен быть числом")

    def search_tournaments(self, conditions):
        return self.model.search_tournaments(conditions)

    def delete_tournaments(self, conditions):
        deleted = self.model.delete_tournaments(conditions)
        self.view.update_display()
        return deleted

    def save_to_xml(self, filename):
        self.model.save_to_xml(filename)
