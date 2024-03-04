from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from PyQt6.uic import loadUi
import sqlite3


class Admin_frame(QDialog):
    def __init__(self, parent=None):
        super(Admin_frame, self).__init__(parent)
        loadUi("UI_static/admin_franme.ui", self)
        self.show_work.pressed.connect(self.show_all_works)
        self.show_users.pressed.connect(self.show_user)
        self.pushButton_4.clicked.connect(self.update_work_or_role)

    def update_work_or_role(self):
        sender = self.sender()
        if sender == self.pushButton_4 and self.show_work.isChecked():
            self.update_work()
        elif sender == self.pushButton_4 and self.show_users.isChecked():
            self.update_role()

    def show_user(self):
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = "SELECT id, name, id_buro, role FROM users"
        results = cur.execute(sqlstr)
        rows = list(results)

        column_mapping = {
            "id": "ID",
            "name": "Логин",
            "password": "Пароль",
            "id_buro": "Бюро",
            "role": "Роль",
        }

        column_names = [
            column_mapping.get(column[0], column[0]) for column in results.description
        ]
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        self.tableWidget.setRowCount(len(rows))
        for tablerow, row in enumerate(rows):
            for column, value in enumerate(row):
                self.tableWidget.setItem(tablerow, column, QTableWidgetItem(str(value)))
        
        # Передаем список с названиями столбцов в функцию update_role
        self.column_names = [column[0] for column in results.description]

        conn.close()

    def update_role(self):
        """Обновляем записи в БД"""
        row = self.tableWidget.currentIndex().row()
        column = self.tableWidget.currentIndex().column()
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()

        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                new_value = item.text()

                # Используем названия столбцов из show_user для обновления данных в базе
                cur.execute(
                    """
                    UPDATE users
                    SET {} = ?
                    WHERE id = ?
                    """.format(self.column_names[column]),
                    (new_value, self.tableWidget.item(row, 0).text()),
                )
        conn.commit()
        conn.close()


    def show_all_works(self):
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = "SELECT id, zakaz, izdelie, lz_izv, number_lz, kol_list FROM orders"
        results = cur.execute(sqlstr)
        rows = list(results)

        column_mapping = {
            "id": "ID",
            "zakaz": "Заказ",
            "izdelie": "Изделие",
            "lz_izv": "ЛЗ ИЗВ",
            "number_lz": "Номер ЛЗ",
            "kol_list": "Кол-во листов",
        }

        column_names = [
            column_mapping.get(column[0], column[0]) for column in results.description
        ]

        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)

        self.tableWidget.setRowCount(len(rows))
        for tablerow, row in enumerate(rows):
            for column, value in enumerate(row):
                self.tableWidget.setItem(tablerow, column, QTableWidgetItem(str(value)))
        conn.close()



    def update_work(self):
        """Обновляем записи в БД"""
        row = self.tableWidget.currentIndex().row()
        column = self.tableWidget.currentIndex().column()
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        # Обновляем значение в базе данных и в QTableWidget
        cur.execute("SELECT * FROM orders")
        column_names = [column[0] for column in cur.description]

        # Обновляем значение в базе данных и в QTableWidget
        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                new_value = item.text()

                # Используем названия столбцов из запроса для обновления данных в базе
                cur.execute(
                    """
                    UPDATE orders
                    SET {} = ?
                    WHERE id = ?
                    """.format(
                        column_names[column]
                    ),
                    (new_value, self.tableWidget.item(row, 0).text()),
                )
        conn.commit()
        conn.close()


