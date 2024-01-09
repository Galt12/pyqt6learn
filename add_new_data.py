from PyQt6.QtWidgets import (QDialog, QMessageBox, QApplication,
                             QTableWidgetItem, QMainWindow)
from PyQt6.uic import loadUi
import sys
import sqlite3
from SqlFile import add_items


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi('mainwin.ui', self)
        self.open1.clicked.connect(self.open_dialog)
        self.pushButton_2.clicked.connect(self.open_table)
        # self.lineEdit.setReadOnly(True)  # Set the lineEdit to be read-only
        # self.sum_trudoemkost()

    def open_dialog(self):
        dialog = AddNewOrder()
        self.stackedWidget.addWidget(dialog)
        self.stackedWidget.setCurrentWidget(dialog)

    def open_table(self):
        tableview = TableView()
        self.stackedWidget.addWidget(tableview)
        self.stackedWidget.setCurrentWidget(tableview)


class AddNewOrder(QDialog):
    def __init__(self, parent=None):
        super(AddNewOrder, self).__init__(parent)
        loadUi('form_to_add.ui', self)
        self.pushButton.clicked.connect(self.accept)
        self.sumtrud.setReadOnly(True)
        # Создание экземпляра класса Zakaz и получение списка значений
        zakaz = Zakaz()
        zakaz_list = zakaz.get_zakaz_list()

        # Добавление значений в QComboBox
        self.comboBox.addItems(zakaz_list)

    def accept(self):
        # Получение выбранного значения из QComboBox
        zakaz = self.comboBox.currentText()
        izdelies = self.lineEdit_2.text()
        lz = self.lineEdit_3.text()
        number_lz = self.lineEdit_4.text()
        kol_lista = self.lineEdit_5.text()
        if len(zakaz) == 0 or len(izdelies) == 0 or len(lz) == 0 or len(number_lz) == 0 or len(kol_lista) == 0:
            QMessageBox.warning(self,
                                "Warning",
                                "Zakaz, izdelies, lz, number_lz, kol_lista can't be empty")
        else:
            value = [zakaz, izdelies, lz, number_lz, int(kol_lista)]
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
        sqlstr = 'SELECT SUM(kol_list) FROM orders'
        cur.execute(sqlstr)
        result = cur.fetchone()[0]
        self.sumtrud.setText(str(result))
        self.sumtrud.setReadOnly(True)
        conn.close()


"""Основной класс для отчета за месяца"""


class TableView(QDialog):
    def __init__(self, parent=None):
        super(TableView, self).__init__(parent)
        loadUi('table_all.ui', self)
        self.tableWidget.setColumnCount(5)
        self.open_table()

    """Таблица отчета за месяца"""
    def open_table(self):
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = 'SELECT * FROM orders'

        results = cur.execute(sqlstr)
        rows = list(results)
        self.tableWidget.setRowCount(len(rows))
        for tablerow, row in enumerate(rows):
            for column, value in enumerate(row):
                self.tableWidget.setItem(tablerow,
                                         column,
                                         QTableWidgetItem(str(value)))
        conn.close()


class Zakaz(QDialog):
    def __init__(self, parent=None):
        super(Zakaz, self).__init__(parent)
        conn = sqlite3.connect("table.db")
        cur = conn.cursor()
        sqlstr = 'SELECT DISTINCT zakaz FROM orders'
        cur.execute(sqlstr)
        results = cur.fetchall()
        conn.close()
        self.zakaz_list = [str(result[0]) for result in results]

    def get_zakaz_list(self):
        return self.zakaz_list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())
