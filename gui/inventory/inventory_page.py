from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableView, QHeaderView, QAbstractItemView, QDialog
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QRegularExpression, QSortFilterProxyModel, Qt
from gui.inventory.add_item_dialog import Add_Item
from gui.inventory.modify_item_dialog import Modify_Item

class Inventory_Page(QWidget):
    
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory
        self.main_inventory_layout = QVBoxLayout(self)
        self.set_ui()
        self.set_model()
        self.set_connection()
    
    def set_connection(self):
        self.search_bar.textChanged.connect(self.filter_search)
        self.Add_button.clicked.connect(self.manage_add_item)
        self.Modify_button.clicked.connect(self.manage_modify_item)
    
    def set_ui(self):
        # Top Text Headers.
        
        self.Top_label = QLabel("Inventory Management")
        font = self.Top_label.font()
        font.setPointSize(20)
        font.setBold(True)
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
        Table_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
    def set_model(self):
        self.Item_model = QStandardItemModel()
        self.Item_model.setHorizontalHeaderLabels(["ID", "Name", "Cost", "Quantity", "Description", "Entry Date", "Expirey Date"])
        
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
        
        # Creating the Filter Modal
        self.proxy_model = Filter_Inventory()
        self.proxy_model.setSourceModel(self.Item_model)

        # Set PROXY model to View (Not Item_model directly)
        self.table_view.setModel(self.proxy_model)
        
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
    def filter_search(self, text):
        # Case-insensitive search regex
        regex = QRegularExpression(
            QRegularExpression.escape(text),
            QRegularExpression.PatternOption.CaseInsensitiveOption,
        )
        self.proxy_model.setFilterRegularExpression(regex)
        
    def manage_modify_item(self):
        self.dialog = Modify_Item()
        self.dialog.show()
        self.dialog.data_saved.connect(self.save_modified_data)
        self.dialog.request_search.connect(self.manual_data_modification)
        
        # Auto-populate if user selected a row in QTableView before clicking Modify
        selected = self.table_view.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            item_id = self.proxy_model.index(row, 0).data()
            self.dialog.id_input.setText(str(item_id))
            item_data = self.inventory.get_item_by_id(item_id)
            self.dialog.fill_fields(item_data)
    
    def manual_data_modification(self, item_id: str):
        if item_id:
            item_data = self.inventory.get_item_by_id(item_id)
            self.dialog.fill_fields(item_data)        
    
    def save_modified_data(self, data: dict):
        self.inventory.modify_item(
            data["id"],
            data["name"],
            data["cost"],
            data["quantity"],
            data["description"],
            data["entry_date"],
            data["expiry_date"]
        )
        self.refresh_table()

    def refresh_table(self):
        self.Item_model.removeRows(0, self.Item_model.rowCount())

        for item in self.inventory.get_all_items():
            self.add_item_to_table(
                item["id"],
                item["name"],
                item["cost"],
                item["quantity"],
                item["description"],
                item["entry_date"],
                item["expiry_date"]
            )
        
class Filter_Inventory(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):
        # If no search text is typed, show all rows
        regex = self.filterRegularExpression()
        if not regex.pattern():
            return True

        model = self.sourceModel()

        # Column 1 = Name, Column 4 = Description
        name_idx = model.index(source_row, 1, source_parent)
        desc_idx = model.index(source_row, 4, source_parent)

        name_text = str(model.data(name_idx, Qt.ItemDataRole.DisplayRole) or "")
        desc_text = str(model.data(desc_idx, Qt.ItemDataRole.DisplayRole) or "")

        # Check if either column matches search query
        return bool(
            regex.match(name_text).hasMatch() or regex.match(desc_text).hasMatch()
        )