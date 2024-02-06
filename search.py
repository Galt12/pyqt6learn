from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel


class Search(QDialog):
    """Поиск"""

    def __init__(self, parent=None):
        super(Search, self).__init__(parent)
        loadUi("search.ui", self)
        # self.initUI()
        self.search_input = self.lineEdit
        # self.tableView

        self.pushButton.clicked.connect(self.search)

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("table.db")
        self.db.open()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.lineEdit)
        hbox.addWidget(self.tableView)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def search(self):
        query = QSqlQueryModel()
        query.setQuery(
                f"SELECT * FROM orders WHERE zakaz LIKE '%{self.search_input.text()}%'"
            # f"SELECT * FROM users JOIN buro ON users.id_buro = buro.id WHERE buro.name_buro LIKE '%{self.search_input.text()}%'"
            # f"SELECT * FROM orders "
        )

        self.tableView.setModel(query)
