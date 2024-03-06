import sys
import sqlite3
from PyQt6.QtWidgets import (
    QDialog,
    QMessageBox,
    QApplication,
)
from PyQt6.uic import loadUi
from SqlFile import add_user
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from user_frame import AddNewOrder
from admin_panel import Admin_frame


class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        loadUi("UI_static/login.ui", self)
        self.setWindowTitle("Логин")
        self.enter_Button.clicked.connect(self.login)
        self.reg_Button_2.clicked.connect(self.registration)
        self.base_line_edit = [self.login_line, self.pass_line]

    def login(self):
        name = self.login_line.text()
        passw = self.pass_line.text()
        con = sqlite3.connect("table.db")
        cur = con.cursor()

        cur.execute("SELECT * FROM users WHERE name = ?;", (name,))
        value = cur.fetchall()
        print(value[0][4])
        if value and value[0][2] == passw:
            role = value[0][4]
            if role == "user":
                enter = AddNewOrder(name)
                enter.exec()
            elif role == "admin":
                enter = Admin_frame()
                enter.exec()

            Login.close(self)
        else:
            QMessageBox.warning(self, "Ошибка вышла")

        cur.close()
        con.close()

    def registration(self):
        Login.close(self)
        reg = Registration()
        reg.exec()


class Registration(QDialog):
    def __init__(self, parent=None):
        super(Registration, self).__init__(parent)
        loadUi("UI_static/registration.ui", self)
        self.setWindowTitle("Регистрация")
        buro_name = self.check_buro()
        for name_buro in buro_name:
            self.list_buro.addItem(name_buro)
        self.buttonBox.accepted.connect(self.add_user)

    def check_buro(self):
        list_buro = []
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("table.db")
        if not db.open():
            print("Не удалось открыть базу данных")
            return list_buro

        query = QSqlQuery()
        query.prepare("SELECT DISTINCT name_buro FROM buro")
        if not query.exec():
            print("Ошибка выполнения запроса")
            return list_buro

        while query.next():
            name_buro = query.value(0)
            list_buro.append(name_buro)
        db.close()

        return list_buro

    def add_user(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        buro = self.list_buro.currentText()

        if len(login) == 0 or len(password) == 0:
            QMessageBox.warning(
                self,
                "Warning",
                "Login, password can't by empty",
            )
        else:

            conn = sqlite3.connect("table.db")
            cur = conn.cursor()

            cur.execute("SELECT * FROM users WHERE name = ?;", (login,))
            value = cur.fetchall()
            if value != []:
                QMessageBox.warning(self, "Есть такой пользователь")
            # Получаем id_buro по названию бюро
            cur.execute("SELECT id FROM buro WHERE name_buro = ?", (buro,))
            result = cur.fetchone()
            if result is None:
                print("Бюро с таким названием не найдено")
                conn.close()
                return

            id_buro = result[0]
            conn.commit()
            conn.close()

            user_info = [login, password, id_buro]
            add_user(user_info)
            Registration.close(self)
            enter = Login()
            enter.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())
