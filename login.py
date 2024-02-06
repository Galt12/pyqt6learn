import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.uic import loadUi

class Login(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("login.ui", self)
        self.setWindowTitle("Логин")
        self.enter_Button.clicked.connect(self.login)
        self.reg_Button_2.clicked.connect(self.registration)

    def login(self):
        pass
    def registration(self):
        # Implement your registration logic here
        pass


