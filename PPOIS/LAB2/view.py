from model import TournamentModel


from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
                             QComboBox, QDialog, QLabel, QCalendarWidget, QMessageBox,
                             QToolBar, QAction, QFileDialog, QTreeWidget, QTreeWidgetItem)

# Представление (View)
class TournamentView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Спортивные турниры")
        self.setGeometry(100, 100, 900, 600,)
        self.model = TournamentModel()
        self.controller = None
        self.current_page = 0
        self.records_per_page = 10

        # Главный виджет и布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Панель инструментов
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        add_action = QAction("Добавить", self)
        add_action.triggered.connect(self.show_add_dialog)
        toolbar.addAction(add_action)
        search_action = QAction("Поиск", self)
        search_action.triggered.connect(self.show_search_dialog)
        toolbar.addAction(search_action)
        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(self.show_delete_dialog)
        toolbar.addAction(delete_action)
        save_action = QAction("Сохранить в XML", self)
        save_action.triggered.connect(self.save_to_xml)
        toolbar.addAction(save_action)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Дата", "Спорт", "Победитель", "Призовые", "Заработок"])
        layout.addWidget(self.table)

        # Пагинация
        pagination_layout = QHBoxLayout()
        self.first_btn = QPushButton("Первая")
        self.first_btn.clicked.connect(self.first_page)
        pagination_layout.addWidget(self.first_btn)
        self.prev_btn = QPushButton("Пред.")
        self.prev_btn.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_btn)
        self.next_btn = QPushButton("След.")
        self.next_btn.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_btn)
        self.last_btn = QPushButton("Последняя")
        self.last_btn.clicked.connect(self.last_page)
        pagination_layout.addWidget(self.last_btn)
        self.page_label = QLabel()
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(QLabel("Записей на странице:"))
        self.per_page_edit = QLineEdit("10")
        self.per_page_edit.textChanged.connect(self.update_display)
        pagination_layout.addWidget(self.per_page_edit)
        layout.addLayout(pagination_layout)

        # Кнопка для дерева
        tree_btn = QPushButton("Показать дерево")
        tree_btn.clicked.connect(self.show_tree_view)
        layout.addWidget(tree_btn)

        self.update_display()

    def set_controller(self, controller):
        self.controller = controller

    def update_display(self):
        records = self.model.get_all_tournaments()
        try:
            self.records_per_page = int(self.per_page_edit.text())
        except ValueError:
            self.records_per_page = 10
        total_records = len(records)
        total_pages = (total_records + self.records_per_page - 1) // self.records_per_page
        self.current_page = min(self.current_page, total_pages - 1) if total_pages > 0 else 0
        start = self.current_page * self.records_per_page
        end = min(start + self.records_per_page, total_records)

        self.table.setRowCount(end - start)
        for i, record in enumerate(records[start:end]):
            for j, value in enumerate(record):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        self.page_label.setText(f"Страница {self.current_page + 1} из {total_pages}, Всего: {total_records}")

    def first_page(self):
        self.current_page = 0
        self.update_display()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    def next_page(self):
        total_pages = (len(self.model.get_all_tournaments()) + self.records_per_page - 1) // self.records_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_display()

    def last_page(self):
        total_pages = (len(self.model.get_all_tournaments()) + self.records_per_page - 1) // self.records_per_page
        self.current_page = total_pages - 1 if total_pages > 0 else 0
        self.update_display()

    def show_add_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить турнир")
        dialog.setFixedSize(500, 700)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Название:"))
        name_edit = QLineEdit()
        layout.addWidget(name_edit)

        layout.addWidget(QLabel("Дата:"))
        date_edit = QCalendarWidget()
        layout.addWidget(date_edit)

        layout.addWidget(QLabel("Вид спорта:"))
        sport_edit = QLineEdit()
        layout.addWidget(sport_edit)

        layout.addWidget(QLabel("Победитель:"))
        winner_edit = QLineEdit()
        layout.addWidget(winner_edit)

        layout.addWidget(QLabel("Призовые:"))
        prize_edit = QLineEdit()
        layout.addWidget(prize_edit)

        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(lambda: self.controller.add_tournament(
            name_edit.text(), date_edit.selectedDate().toString("yyyy-MM-dd"),
            sport_edit.text(), winner_edit.text(), prize_edit.text()
        ) or dialog.accept())
        layout.addWidget(add_btn)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_search_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Поиск турниров")
        dialog.setFixedSize(500, 900)
        layout = QVBoxLayout()

        conditions = {}

        layout.addWidget(QLabel("Название:"))
        name_edit = QLineEdit()
        layout.addWidget(name_edit)

        layout.addWidget(QLabel("Дата:"))
        date_edit = QCalendarWidget()
        layout.addWidget(date_edit)

        layout.addWidget(QLabel("Вид спорта:"))
        sport_combo = QComboBox()
        sport_combo.addItems(set(row[3] for row in self.model.get_all_tournaments()))
        layout.addWidget(sport_combo)

        layout.addWidget(QLabel("Победитель:"))
        winner_edit = QLineEdit()
        layout.addWidget(winner_edit)

        layout.addWidget(QLabel("Призовые (мин):"))
        prize_min_edit = QLineEdit()
        layout.addWidget(prize_min_edit)

        layout.addWidget(QLabel("Призовые (макс):"))
        prize_max_edit = QLineEdit()
        layout.addWidget(prize_max_edit)

        result_table = QTableWidget()
        result_table.setColumnCount(7)
        result_table.setHorizontalHeaderLabels(["ID", "Название", "Дата", "Спорт", "Победитель", "Призовые", "Заработок"])
        layout.addWidget(result_table)

        def perform_search():
            conditions["name"] = name_edit.text()
            conditions["date"] = date_edit.selectedDate().toString("yyyy-MM-dd") if name_edit.text() == "" else ""
            conditions["sport"] = sport_combo.currentText()
            conditions["winner"] = winner_edit.text()
            conditions["prize_min"] = float(prize_min_edit.text()) if prize_min_edit.text() else None
            conditions["prize_max"] = float(prize_max_edit.text()) if prize_max_edit.text() else None
            results = self.controller.search_tournaments(conditions)
            result_table.setRowCount(len(results))
            for i, row in enumerate(results):
                for j, value in enumerate(row):
                    result_table.setItem(i, j, QTableWidgetItem(str(value)))

        search_btn = QPushButton("Поиск")
        search_btn.clicked.connect(perform_search)
        layout.addWidget(search_btn)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_delete_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Удалить турниры")
        dialog.setFixedSize(400, 500)
        layout = QVBoxLayout()

        conditions = {}

        layout.addWidget(QLabel("Название:"))
        name_edit = QLineEdit()
        layout.addWidget(name_edit)

        layout.addWidget(QLabel("Дата:"))
        date_edit = QCalendarWidget()
        layout.addWidget(date_edit)

        layout.addWidget(QLabel("Вид спорта:"))
        sport_combo = QComboBox()
        sport_combo.addItems(set(row[3] for row in self.model.get_all_tournaments()))
        layout.addWidget(sport_combo)

        layout.addWidget(QLabel("Победитель:"))
        winner_edit = QLineEdit()
        layout.addWidget(winner_edit)

        layout.addWidget(QLabel("Призовые (мин):"))
        prize_min_edit = QLineEdit()
        layout.addWidget(prize_min_edit)

        layout.addWidget(QLabel("Призовые (макс):"))
        prize_max_edit = QLineEdit()
        layout.addWidget(prize_max_edit)

        def perform_delete():
            conditions["name"] = name_edit.text()
            conditions["date"] = date_edit.selectedDate().toString("yyyy-MM-dd") if name_edit.text() == "" else ""
            conditions["sport"] = sport_combo.currentText()
            conditions["winner"] = winner_edit.text()
            conditions["prize_min"] = float(prize_min_edit.text()) if prize_min_edit.text() else None
            conditions["prize_max"] = float(prize_max_edit.text()) if prize_max_edit.text() else None
            deleted = self.controller.delete_tournaments(conditions)
            QMessageBox.information(dialog, "Результат", f"Удалено записей: {deleted}")
            dialog.accept()

        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(perform_delete)
        layout.addWidget(delete_btn)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_tree_view(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Дерево турниров")
        dialog.setFixedSize(600, 400)
        layout = QVBoxLayout()

        tree = QTreeWidget()
        tree.setHeaderLabel("Турниры")
        for record in self.model.get_all_tournaments():
            parent = QTreeWidgetItem(tree, [f"Турнир {record[0]}"])
            for i, field in enumerate(["Название", "Дата", "Спорт", "Победитель", "Призовые", "Заработок"]):
                QTreeWidgetItem(parent, [f"{field}: {record[i + 1]}"])
        layout.addWidget(tree)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_to_xml(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "XML Files (*.xml)")
        if filename:
            self.controller.save_to_xml(filename)
