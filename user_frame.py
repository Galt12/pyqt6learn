import sqlite3
from PyQt6.QtWidgets import (
    QDialog,
    QMessageBox,
    QTableWidgetItem,
)
from PyQt6.uic import loadUi
from SqlFile import add_items
from PyQt6.QtCore import QDate


class AddNewOrder(QDialog):
    """
    Добавление нового заказа
    """

    def __init__(self, name, parent=None):
        super(AddNewOrder, self).__init__(parent)
        loadUi("UI_static/form_to_add.ui", self)
        self.setWindowTitle("Добавить работу")
        self.label_6.setText(name)
        self.pushButton.clicked.connect(self.accept)
        self.sumtrud.setReadOnly(True)
        self.dateEdit.setDate(QDate.currentDate())
        self.show_work_button.clicked.connect(self.show_works)
        self.date = self.dateEdit.date().toString("yyyy-MM-dd")
        self.user = name
        # Создание экземпляра класса Zakaz и получение списка значений
        zakaz_list = self.get_zakaz_list()
        self.sum_trudoemkost(self.user)
        # Добавление значений в QComboBox
        self.comboBox.addItems(zakaz_list)
        works = self.show_work_list()
        self.type_works.addItems(works)
        # Подключение сигнала изменения значения в comboBox к обновлению lineEdit_2
        self.comboBox.currentIndexChanged.connect(self.show_izdelie)
        self.lineEdit_2.setReadOnly(True)

    def get_zakaz_list(self):
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = "SELECT zakaz_izdelie FROM izdelia_zakaz"
        cur.execute(sqlstr)
        results = cur.fetchall()
        conn.close()
        self.zakaz_list = [str(result[0]) for result in results]
        return self.zakaz_list

    def show_izdelie(self):
        zakaz = self.comboBox.currentText()
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT name_izdelie FROM izdelia_zakaz WHERE zakaz_izdelie = ?",
            (zakaz,),
        )
        result = cur.fetchone()
        if result:
            name_izdelie = result[0]
            self.lineEdit_2.setText(name_izdelie)
        else:
            self.lineEdit_2.clear()
        conn.close()

    def show_work_list(self):
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()

        cur.execute(
            """SELECT u.id_buro, w.name_works
            FROM users u
            JOIN work_buro w
            ON u.id_buro = w.id_buro
            WHERE u.name = ?""",
            (self.user,),
        )
        results = cur.fetchall()

        if not results:
            print("Бюро с таким названием не найдено")
            conn.close()
            return []

        work_list = [result[1] for result in results]

        conn.close()
        return work_list

    def accept(self):
        # Получение выбранного значения из QComboBox

        date = self.dateEdit.date().toString("yyyy-MM-dd")
        zakaz = self.comboBox.currentText()
        izdelies = self.lineEdit_2.text()
        works = self.type_works.currentText()
        lz = self.lineEdit_3.text()
        number_lz = self.lineEdit_4.text()
        kol_lista = self.lineEdit_5.text()
        user = self.label_6.text()

        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE name = ?", (user,))
        result = cur.fetchone()
        if result is None:
            print("Бюро с таким названием не найдено")
            conn.close()
            return

        id_user = result[0]
        conn.commit()
        conn.close()

        if (
            len(zakaz) == 0
            or len(izdelies) == 0
            or len(lz) == 0
            or len(number_lz) == 0
            or len(kol_lista) == 0
        ):
            QMessageBox.warning(
                self,
                "Warning",
                "Zakaz, izdelies, lz, number_lz, kol_lista can't be empty",
            )
        else:
            value = [
                zakaz,
                izdelies,
                lz,
                number_lz,
                int(kol_lista),
                id_user,
                date,
                works,
            ]
            add_items(value)
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()

    def sum_trudoemkost(self, user):
        """Сумма работ за месяц"""
        try:
            with sqlite3.connect("table.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT id FROM users WHERE name = ?", (user,))
                result = cur.fetchone()
                if result is None:
                    print("Юзера нет")
                    return

                id_user = result[0]

                cur.execute(
                    "SELECT SUM(kol_list) FROM orders WHERE id_user = ? ", (id_user,)
                )
                result = cur.fetchone()[0]
                self.sumtrud.setText(str(result))
                self.sumtrud.setReadOnly(True)
        except sqlite3.Error as e:
            print("Error executing SQL query:", e)

    def show_works(self):
        enter = TableView(self.user)
        enter.exec()


class TableView(QDialog):
    """Основной класс для отчета за месяца"""

    def __init__(self, user, parent=None):
        super(TableView, self).__init__(parent)
        loadUi("UI_static/table_all.ui", self)
        self.setWindowTitle("Список дел за месяц")
        self.name = user
        self.date = QDate.currentDate()
        first_day, last_day = self.get_first_and_last_day_of_month()
        self.show_works_for_id(first_day, last_day)

    def get_first_and_last_day_of_month(self):
        first_day = self.date.addDays(
            -self.date.day() + 1
        )  # Получаем первый день месяца
        last_day = (
            self.date.addDays(-self.date.day()).addMonths(1).addDays(-1)
        )  # Получаем последний день месяца

        return first_day, last_day

    def show_works_for_id(self, first_day, last_day):
        """Таблица отчета за месяца"""
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE name = ?", (self.name,))
        result = cur.fetchone()
        if result is None:
            print("Бюро с таким названием не найдено")
            conn.close()
            return

        id_user = str(result[0])

        results = cur.execute(
            """
            SELECT zakaz, izdelie, lz_izv, number_lz, kol_list
            FROM orders
            WHERE orders.id_user = ?
            AND orders.date BETWEEN ? AND ?
            """,
            (
                id_user,
                first_day.toString("yyyy-MM-dd"),
                last_day.toString("yyyy-MM-dd"),
            ),
        )

        rows = list(results)

        self.tableWidget.setRowCount(len(rows))
        for tablerow, row in enumerate(rows):
            for column, value in enumerate(row):
                self.tableWidget.setItem(tablerow, column, QTableWidgetItem(str(value)))
        conn.close()

    def open_table(self):
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = "SELECT zakaz, izdelie, lz_izv, number_lz, kol_list FROM orders"

        results = cur.execute(sqlstr)
        rows = list(results)
        self.tableWidget.setRowCount(len(rows))
        for tablerow, row in enumerate(rows):
            for column, value in enumerate(row):
                self.tableWidget.setItem(tablerow, column, QTableWidgetItem(str(value)))
        conn.close()
