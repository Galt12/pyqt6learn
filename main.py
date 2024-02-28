import sys
import sqlite3
from PyQt6.QtWidgets import (
    QDialog,
    QMessageBox,
    QApplication,
    QTableWidgetItem,
    QMainWindow,
)
from PyQt6.uic import loadUi
from SqlFile import add_items, add_user
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from search import Search
from PyQt6.QtCore import QDate, QCalendar
from datetime import datetime


class MainWindow(QMainWindow):
    """
    Основное окно
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi("mainwin.ui", self)

        self.open1.clicked.connect(self.open_dialog)
        self.pushButton_2.clicked.connect(self.open_table)
        # self.lineEdit.setReadOnly(True)  # Set the lineEdit to be read-only
        # self.sum_trudoemkost()
        self.pushButton3.clicked.connect(self.search)
        self.login_button.clicked.connect(self.login_main)
        # self.reg_button.clicked.connect(self.registration)

    def open_dialog(self):
        dialog = AddNewOrder()
        self.stackedWidget.addWidget(dialog)
        self.stackedWidget.setCurrentWidget(dialog)

    def open_table(self):
        tableview = TableView()
        self.stackedWidget.addWidget(tableview)
        self.stackedWidget.setCurrentWidget(tableview)

    def search(self):
        search = Search()
        self.stackedWidget.addWidget(search)
        self.stackedWidget.setCurrentWidget(search)

    def login_main(self):
        log = Login()
        self.stackedWidget.addWidget(log)
        self.stackedWidget.setCurrentWidget(log)


class AddNewOrder(QDialog):
    """
    Добавление нового заказа
    """

    def __init__(self, name, parent=None):
        super(AddNewOrder, self).__init__(parent)
        loadUi("form_to_add.ui", self)
        self.setWindowTitle("Добавить работу")
        self.label_6.setText(name)
        self.pushButton.clicked.connect(self.accept)
        self.sumtrud.setReadOnly(True)
        self.dateEdit.setDate(QDate.currentDate())
        self.show_work_button.clicked.connect(self.show_works)
        self.date = self.dateEdit.date().toString("yyyy-MM-dd")
        self.user = name
        # Создание экземпляра класса Zakaz и получение списка значений
        zakaz = Zakaz()
        zakaz_list = zakaz.get_zakaz_list()

        # Добавление значений в QComboBox
        self.comboBox.addItems(zakaz_list)
        works = self.show_work_list()
        self.type_works.addItems(works)
        # Подключение сигнала изменения значения в comboBox к обновлению lineEdit_2
        self.comboBox.currentIndexChanged.connect(self.show_izdelie)
        self.lineEdit_2.setReadOnly(True)

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
        self.sum_trudoemkost()

    """Сумма работ за месяц"""

    def sum_trudoemkost(self):
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = "SELECT SUM(kol_list) FROM orders"
        cur.execute(sqlstr)
        result = cur.fetchone()[0]
        self.sumtrud.setText(str(result))
        self.sumtrud.setReadOnly(True)
        conn.close()

    def show_works(self):
        enter = TableView(self.user)
        enter.exec()


class TableView(QDialog):
    """Основной класс для отчета за месяца"""

    def __init__(self, user, parent=None):
        super(TableView, self).__init__(parent)
        loadUi("table_all.ui", self)
        self.setWindowTitle("Список дел за месяц")
        self.name = user
        self.date = QDate.currentDate()
        first_day, last_day = self.get_first_and_last_day_of_month()
        self.show_works_for_id(first_day, last_day)


    def get_first_and_last_day_of_month(self):
        first_day = self.date.addDays(-self.date.day() + 1)  # Получаем первый день месяца
        last_day = self.date.addDays(-self.date.day()).addMonths(1).addDays(-1)  # Получаем последний день месяца

        return first_day, last_day

    """Таблица отчета за месяца"""

    def show_works_for_id(self, first_day, last_day):
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
            (id_user, first_day.toString("yyyy-MM-dd"), last_day.toString("yyyy-MM-dd"))
        )

        rows = list(results)

            
        self.tableWidget.setRowCount(len(rows))
        for tablerow, row in enumerate(rows):
            for column, value in enumerate(row):
                self.tableWidget.setItem(
                    tablerow, column, QTableWidgetItem(str(value)))
        conn.close()

    def open_table(self):
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = (
            "SELECT zakaz, izdelie, lz_izv, number_lz, kol_list FROM orders"
        )

        results = cur.execute(sqlstr)
        rows = list(results)
        self.tableWidget.setRowCount(len(rows))
        for tablerow, row in enumerate(rows):
            for column, value in enumerate(row):
                self.tableWidget.setItem(
                    tablerow, column, QTableWidgetItem(str(value))
                )
        conn.close()


class Zakaz(QDialog):
    def __init__(self, parent=None):
        super(Zakaz, self).__init__(parent)
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = "SELECT zakaz_izdelie FROM izdelia_zakaz"
        cur.execute(sqlstr)
        results = cur.fetchall()
        conn.close()
        self.zakaz_list = [str(result[0]) for result in results]

    def get_zakaz_list(self):
        return self.zakaz_list


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
