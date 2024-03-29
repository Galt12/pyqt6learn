import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
)
from PyQt6.uic import loadUi
from login import Login, Registration
from admin_panel import Admin_frame


class MainWindow(QMainWindow):
    """
    Основное окно
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi("UI_static/mainwin.ui", self)
        self.login_btn.clicked.connect(self.login)
        self.login()
        self.show_work.clicked.connect(self.add_work)
        self.pushButton_3.clicked.connect(self.registration)

    def registration(self):
        reg = Registration()
        self.stackedWidget.addWidget(reg)
        self.stackedWidget.setCurrentWidget(reg)

    def login(self):
        login = Login()
        self.stackedWidget.addWidget(login)
        self.stackedWidget.setCurrentWidget(login)

    # def update_status_bar(self, message)
    #     self.statusBar().showMessage(message)


    def add_work(self):
        add_work = Admin_frame()
        self.stackedWidget.addWidget(add_work)
        self.stackedWidget.setCurrentWidget(add_work)

    def enter_to_prog(self):
        self.stackedWidget.addWidget(Admin_frame)
        self.stackedWidget.setCurrentWidget(Admin_frame)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
