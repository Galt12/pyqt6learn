from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QApplication, QCheckBox
from PyQt6.uic import loadUi
import sqlite3
from user_frame import AddNewOrder
from SqlFile import check_buro, fetch_orders_for_monts
import sys
from PyQt6.QtCore import QDate

class Admin_frame(QDialog):
    def __init__(self, parent=None):
        super(Admin_frame, self).__init__(parent)
        loadUi("UI_static/admin_franme.ui", self)
        self.setWindowTitle("АДМИНЫ ТУТ")

        self.startdate.setDate(QDate.currentDate())
        self.end_date.setDate(QDate.currentDate())
        self.show_work.pressed.connect(self.show_all_works)
        self.show_users.pressed.connect(self.show_user)
        self.pushButton_4.clicked.connect(self.update_work_or_role)
        self.test_buro2.clicked.connect(self.test_buro)
        zakaz_list = AddNewOrder.get_zakaz_list(self)
        self.zakazBox.addItems(zakaz_list)
        self.otchet_btn.clicked.connect(self.show_otchet)
        buro_name = check_buro()
        for name_buro in buro_name:
            self.type_buro.addItem(name_buro)

        self.column_mapping = {
            "id": "ID",
            "name": "Логин",
            "password": "Пароль",
            "id_buro": "Бюро",
            "role": "Роль",
            "zakaz": "Заказ",
            "izdelie": "Изделие",
            "lz_izv": "ЛЗ ИЗВ",
            "number_lz": "Номер ЛЗ",
            "kol_list": "Кол-во листов",
        }





    def update_work_or_role(self):
        sender = self.sender()
        if sender == self.pushButton_4 and self.show_work.isChecked():
            self.update_work()
        elif sender == self.pushButton_4 and self.show_users.isChecked():
            self.update_role()

    def show_user(self):
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = "SELECT u.id, u.name, u.id_buro, u.role FROM users u "
        results = cur.execute(sqlstr)
        rows = list(results)

        self._extracted_tableview_column(results, self.column_mapping, rows)
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
                    """.format(
                        self.column_names[column]
                    ),
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
        self._extracted_tableview_column(results, self.column_mapping, rows)
        conn.close()


    def _extracted_tableview_column(self, results, column_mapping, rows):
        column_names = [
            column_mapping.get(column[0], column[0]) for column in results.description
        ]
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setRowCount(len(rows))
        for tablerow, row in enumerate(rows):
            for column, value in enumerate(row):
                self.tableWidget.setItem(tablerow, column, QTableWidgetItem(str(value)))

        sum_kol_list_value = self.sum_kol_list()
        self.sum_trud.setText(str(sum_kol_list_value))

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
        sum_kol_list_value = self.sum_kol_list()
        self.sum_trud.setText(str(sum_kol_list_value))

    def get_selected_columns(self, column_mapping):
        selected_columns = []
        layout = self.verticalLayout_2
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                column_text = widget.text()
                if column_text in column_mapping.values():
                    selected_columns.append(
                        list(column_mapping.keys())[
                            list(column_mapping.values()).index(column_text)
                        ]
                    )
                else:
                    print(f"Столбец '{column_text}' не найден в column_mapping")
                widget.setChecked(False)
        columns_str = ", ".join(selected_columns)
        return columns_str

    def test_buro(self):
        zakaz = self.zakazBox.currentText()
        buro_name = self.type_buro.currentText()
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        selected_columns = self.get_selected_columns(self.column_mapping)
        if len(selected_columns) != 0:
            results = cur.execute(
                # f"SELECT {selected_columns} FROM orders WHERE zakaz = ?", (zakaz,)
                f"""SELECT o.{selected_columns}, b.name_buro
                    FROM orders o
                    JOIN users u ON o.id_user = u.id
                    JOIN buro b ON u.id_buro = b.id
                    WHERE b.name_buro = ?
                    AND o.zakaz = ?""", (buro_name, zakaz)
            )
        rows = list(results)
        self._extracted_tableview_column(results, self.column_mapping, rows)
        conn.close()


    def show_otchet(self):
        zakaz = self.zakazBox.currentText()
        buro_name = self.type_buro.currentText()
        date = (QDate.currentDate())
        first_day = self.startdate.date().toString("yyyy-MM-dd")
        last_day = self.end_date.date().toString("yyyy-MM-dd")
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        selected_columns = self.get_selected_columns(self.column_mapping)
        if len(selected_columns) != 0:
            results = cur.execute(
                f"SELECT {selected_columns} FROM orders WHERE zakaz = ? AND id_buro = ?", (zakaz, buro_name)
            )
        elif first_day != date:
            results = cur.execute(
            """
            SELECT zakaz, izdelie, sum(kol_list)
            FROM orders
            WHERE orders.date BETWEEN ? AND ?
            GROUP BY zakaz
            """,
            (first_day, last_day),
        )
        else:
            results = cur.execute(
                f"SELECT id, zakaz, izdelie, lz_izv, number_lz, kol_list FROM orders WHERE zakaz = ?",
                (zakaz,),
            )
        rows = list(results)
        self._extracted_tableview_column(results, self.column_mapping, rows)
        conn.close()


    def sum_kol_list(self):
        header_labels = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(self.tableWidget.columnCount())]
        column_name = "Кол-во листов"
        if column_name in header_labels:
            kol_list_index = header_labels.index(column_name)
        else:
            return -1

        sum_kol_list = 0
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, kol_list_index)
            if item is not None:
                sum_kol_list += int(item.text())

        return sum_kol_list

    def work_on_monts(self):
        first_day = self.startdate.date().toString("yyyy-MM-dd")
        last_day = self.end_date.date().toString("yyyy-MM-dd")
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        results = cur.execute(
            """
            SELECT zakaz, izdelie, sum(kol_list)
            FROM orders
            WHERE orders.date BETWEEN ? AND ?
            GROUP BY zakaz
        """,
            (first_day, last_day),
        )
        rows = list(results)

        self._extracted_tableview_column(results, self.column_mapping, rows)
        # Передаем список с названиями столбцов в функцию update_role
        self.column_names = [column[0] for column in results.description]

        conn.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Admin_frame()
    window.show()
    sys.exit(app.exec())
