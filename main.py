from PyQt6.QtWidgets import QApplication
from gui.mainwindow import MainWindow
from users.authenticate import authentication
from inventory.inventory import Inventory
from data.datamanager import Data_Manager
from bill.billingmanager import Billing_Manager

if __name__ == "__main__":
    database = Data_Manager()
    inventory = Inventory(database)
    billing_manager = Billing_Manager(database)

    app = QApplication([])

    window = MainWindow(inventory, billing_manager)

    window.show()
    app.exec()