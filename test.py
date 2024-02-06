import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dialog")
        self.setGeometry(200, 200, 200, 100)

        button = QPushButton("Open Main Window", self)
        button.clicked.connect(self.open_main_window)

    def open_main_window(self):
        main_window = MainWindow()
        main_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec())
