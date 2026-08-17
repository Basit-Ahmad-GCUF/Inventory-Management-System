from PyQt6.QtWidgets import QApplication
from gui.mainwindow import MainWindow
from users.authenticate import authentication
from inventory.inventory import Inventory
from data.datamanager import Data_Manager

if __name__ == "__main__":
    database = Data_Manager()
    inventory = Inventory(database)

    app = QApplication([])

    window = MainWindow(inventory)

    window.show()
    
    app.exec()