import sys
import sqlite3
from PyQt6.QtWidgets import (
    QDialog,
    QMessageBox,
    QApplication,
    QWidget,
)
from PyQt6.uic import loadUi
from SqlFile import add_user, check_buro
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from user_frame import AddNewOrder
from admin_panel import Admin_frame
from PyQt6.QtCore import pyqtSignal


class Login(QWidget):
    login_successful = pyqtSignal(str)  # Сигнал, который передает логин

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        loadUi("UI_static/login.ui", self)
        self.setWindowTitle("Логин")
        self.enter_Button.clicked.connect(self.login)
        self.reg_Button_2.clicked.connect(self.registration)

    def login(self):
        login_name = self.login_line.text()
        passw = self.pass_line.text()
        with sqlite3.connect("table.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE name = ?;", (login_name,))
            value = cur.fetchall()
            if value and value[0][2] == passw:
                # Если вход успешен, отправляем сигнал
                self.login_successful.emit(login_name)
                
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")

    def registration(self):
        Login.close(self)
        reg = Registration()
        reg.exec()


class Registration(QDialog):
    def __init__(self, parent=None):
        super(Registration, self).__init__(parent)
        loadUi("UI_static/registration.ui", self)
        self.setWindowTitle("Регистрация")
        buro_name = check_buro()
        for name_buro in buro_name:
            self.list_buro.addItem(name_buro)
        self.buttonBox.accepted.connect(self.add_user)
        self.buttonBox.rejected.connect(self.exit_reg)

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

    def exit_reg(self):
        Registration.close(self)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Login()
#     window.show()
#     sys.exit(app.exec())
