from PyQt6.QtWidgets import QApplication
from gui.mainwindow import MainWindow
from users.authenticate import authentication

if __name__ == "__main__":

    app = QApplication([])

    window = MainWindow()

    window.show()
    
    app.exec()