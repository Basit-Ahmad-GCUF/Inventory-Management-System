from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableView, QHeaderView, QAbstractItemView, QDialog
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from gui.add_item_dialog import Add_Item

class Inventory_Page(QWidget):
    
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory
        self.main_inventory_layout = QVBoxLayout(self)
        self.set_ui()
        self.set_model()
        self.set_connection()
    
    def set_connection(self):
        self.Add_button.clicked.connect(self.manage_add_item)
    
    def set_ui(self):
        # Top Text Headers.
        
        self.Top_label = QLabel("Inventory Management")
        font = self.Top_label.font()
        font.setPointSize(20)
        font.setBold
        self.Top_label.setFont(font)
        
        # Top Tool Bar.
        self.top_tool_bar = QWidget()
        self.top_tool_bar_layout = QHBoxLayout(self.top_tool_bar)
        
        self.search_bar = QLineEdit()
        self.Add_button = QPushButton("Add Item")
        self.Modify_button = QPushButton("Modify Item")
        self.Delete_button = QPushButton("Delete Item")
        
        self.search_bar.setPlaceholderText("Search Inventory")
        
        self.top_tool_bar_layout.addWidget(self.search_bar)
        self.top_tool_bar_layout.addWidget(self.Add_button)
        self.top_tool_bar_layout.addWidget(self.Modify_button)
        self.top_tool_bar_layout.addWidget(self.Delete_button)
        
        # The Table For Holding all the Items in it.
        self.table_view = QTableView()
        
        # Table Styling & Scroll Behavior
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)   # Select full row
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)      # 1 row at a time
        self.table_view.setAlternatingRowColors(True)                                   # Clean zebra striping
        self.table_view.setSortingEnabled(True)                                         # Allow header click sorting

        # Ensure vertical & horizontal scrollbars appear automatically when needed
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Adding It to the Main Inventory Widget So We Can Place It.
        self.main_inventory_layout.addWidget(self.Top_label)
        self.main_inventory_layout.addWidget(self.top_tool_bar)
        self.main_inventory_layout.addWidget(self.table_view)
        
        # Stretch columns cleanly across available space
        Table_header = self.table_view.horizontalHeader()
        if Table_header is not None:
            Table_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
    def set_model(self):
        self.Item_model = QStandardItemModel()
        self.Item_model.setHorizontalHeaderLabels(["ID", "Name", "Cost", "Quantity", "Description", "Entry Date", "Expirey Date"])
        
        self.table_view.setModel(self.Item_model)
        # Adding Items to Table
        items = self.inventory.get_all_items()
        for item in items:
            self.add_item_to_table(
                item["id"],
                item["name"],
                item["cost"],
                item["quantity"],
                item["description"],
                item["entry_date"],
                item["expiry_date"]
            )
        
    def add_item_to_table(self, id, name, cost, quantity, description, entry_date, expirey_date):
        row = [
            QStandardItem(str(id)),
            QStandardItem(str(name)),
            QStandardItem(f"{cost:.2f}"),  # Formats float to 2 decimal places as str
            QStandardItem(str(quantity)),  # Converts int to str
            QStandardItem(str(description)),
            QStandardItem(str(entry_date)),
            QStandardItem(str(expirey_date))
        ]
        self.Item_model.appendRow(row)
        
    def manage_add_item(self):
        dialog = Add_Item()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item = dialog.get_item_data()
            # Adding to Database with separate values
            self.inventory.add_item(
                item["id"],
                item["name"],
                item["cost"],
                item["quantity"],
                item["description"],
                item["entry_date"],
                item["expiry_date"]
            )
            # Adding to Table
            print(item)
            self.add_item_to_table(
                item["id"],
                item["name"],
                item["cost"],
                item["quantity"],
                item["description"],
                item["entry_date"],
                item["expiry_date"]
            )