import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
)
from PyQt6.uic import loadUi
from login import Login, Registration
from admin_panel import Admin_frame
from user_frame import AddNewOrder, TableView

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi("UI_static/mainwin.ui", self)
        self.show_work.clicked.connect(self.add_work)
        self._createStatusBar()

        # Создаем экземпляр Login и подписываемся на сигнал
        self.login_window = Login()
        self.login_window.login_successful.connect(self.update_status_bar)
        self.login_window.login_successful.connect(self.user_add_work)
        self.obgect521.clicked.connect(self.user_add_work)



    def _createStatusBar(self):
        self.statusbar = self.statusBar()
        self.wcLabel = QLabel("Не вошли")
        self.statusbar.addPermanentWidget(self.wcLabel)

    def update_status_bar(self, login_name):
        self.wcLabel.setText(f"Логин: {login_name}")

    def registration(self):
        reg = Registration()
        self.stackedWidget.addWidget(reg)
        self.stackedWidget.setCurrentWidget(reg)

    def login(self):
        login = Login()
        self.stackedWidget.addWidget(login)
        self.stackedWidget.setCurrentWidget(login)


    def add_work(self):
        add_work = Admin_frame()
        self.stackedWidget.addWidget(add_work)
        self.stackedWidget.setCurrentWidget(add_work)

    def user_add_work(self,login_name):
        user_add_work = AddNewOrder(login_name)
        user_show_work = TableView(login_name)
        self.stackedWidget.addWidget(user_add_work)
        self.stackedWidget.setCurrentWidget(user_add_work)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()

    # Показываем окно логина
main_window.login_window.show()

sys.exit(app.exec())
