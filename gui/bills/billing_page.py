from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QHeaderView, 
    QCheckBox, QCompleter, QSplitter, QGridLayout, QTableView, QAbstractItemView,
    QSpinBox, QDoubleSpinBox, QMessageBox
)
from PyQt6.QtGui import QShortcut, QKeySequence, QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class Billing_Window(QWidget):
    def __init__(self, db):
        super().__init__()
        
        self.inventory = db
        self.cart = []
        self.items = self.inventory.get_all_items()
        self.names = [item["name"] for item in self.items]
        
        self.set_ui()
        self.set_model()
        self.set_connections()
        
    def set_ui(self):
        
        Main_layout = QHBoxLayout(self)
        
        Left_panel = QWidget()
        Left_panel.setFixedWidth(200)
        Left_layout = QVBoxLayout(Left_panel)
        Right_panel = QWidget()
        Right_layout = QVBoxLayout(Right_panel)
        
        self.Top_label = QLabel("Create Bills")
        font = self.Top_label.font()
        font.setPointSize(20)
        font.setBold(True)
        self.Top_label.setFont(font)
        
        self.Search_by_id_label = QLabel("Search by ID:")
        
        self.Get_id_to_search = QLineEdit()
        self.Get_id_to_search.setPlaceholderText("Enter ID")
        
        self.Search_by_name_label = QLabel("Search by Name:")
        
        self.Completer = QCompleter(self.names)
        self.Completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.Completer.setFilterMode(Qt.MatchFlag.MatchContains)
        
        self.Get_name_to_search = QLineEdit()
        self.Get_name_to_search.setPlaceholderText("Enter Name") 
        self.Get_name_to_search.setCompleter(self.Completer)
        
        self.Has_discount_cb = QCheckBox("Has Discount")
        
        self.Get_discount_on_bill = QDoubleSpinBox()
        self.Get_discount_on_bill.setSingleStep(0.10)
        self.Get_discount_on_bill.setSuffix(" % ")
        self.Get_discount_on_bill.setMaximum(100.00)
        self.Get_discount_on_bill.setEnabled(False)
        
        self.seperating_line = QLabel("───────────────────────────────────────────")
        
        self.Get_Cutomer_name_label = QLabel("Customer Name:")
                
        self.Get_Cutomer_name = QLineEdit()
        self.Get_Cutomer_name.setPlaceholderText("Enter Customer Name")
        self.Get_Cutomer_name.setText("Shop Keeper")
        
        Left_layout.addWidget(self.Top_label)
        Left_layout.addWidget(self.Search_by_id_label)
        Left_layout.addWidget(self.Get_id_to_search)
        Left_layout.addWidget(self.Search_by_name_label)
        Left_layout.addWidget(self.Get_name_to_search)
        Left_layout.addWidget(self.Has_discount_cb)
        Left_layout.addWidget(self.Get_discount_on_bill)
        Left_layout.addWidget(self.seperating_line)
        Left_layout.addWidget(self.Get_Cutomer_name_label)
        Left_layout.addWidget(self.Get_Cutomer_name)
        
        grid = QGridLayout()
        
        self.name_label = QLabel("Item Name")
        
        self.cost_label = QLabel("Item Cost")
        
        self.qty_label = QLabel("Quantity")
        
        self.desc_label = QLabel("Item Descritpion")
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name In Inventory")
        self.name_input.setReadOnly(True)
        
        self.cost_input = QLineEdit()
        self.cost_input.setPlaceholderText("Item Cost In Inventory")
        self.cost_input.setReadOnly(True)
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Item Description In Inventory")
        self.desc_input.setReadOnly(True)
        
        self.qty_input = QSpinBox()
        self.qty_input.setMaximum(99999)
        
        self.add_button = QPushButton("Add to Bill")
        self.add_button.setDefault(True)
        self.add_button.setEnabled(False)
        self.delete_button = QPushButton("Remove")
        
        grid.addWidget(self.name_label,  0, 0)  # row 0, col 0
        grid.addWidget(self.cost_label,  0, 1)  # row 0, col 1
        grid.addWidget(self.qty_label,   0, 2)  # row 0, col 2
        grid.addWidget(self.name_input,  1, 0)  # row 1, col 0
        grid.addWidget(self.cost_input,  1, 1)
        grid.addWidget(self.qty_input,   1, 2)
        grid.addWidget(self.desc_label,  2, 0)
        grid.addWidget(self.desc_input,  3, 0, 1, 2)  # row 2, col 0, spans 1 row 2 cols
        grid.addWidget(self.add_button,  3, 2)  # row 2, col 2
        grid.addWidget(self.delete_button, 4, 2)
        
        self.table_view = QTableView()
        # Table Styling & Scroll Behavior
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)   # Select full row
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)      # 1 row at a time
        self.table_view.setAlternatingRowColors(True)                                   # Clean zebra striping
        self.table_view.setSortingEnabled(True)                                         # Allow header click sorting

        # Ensure vertical & horizontal scrollbars appear automatically when needed
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.bottom_bar = QHBoxLayout()

        self.clear_btn = QPushButton("Clear (F1)")
        self.save_btn = QPushButton("Save and New (F2)")

        # Totals labels
        self.total_label = QLabel("Total: 0.00")
        self.total_label.setStyleSheet("color: blue; font-weight: bold;")
        self.discount_label = QLabel("After Discount: 0.00")
        self.discount_label.setStyleSheet("color: green; font-weight: bold;")

        self.bottom_bar.addWidget(self.clear_btn)
        self.bottom_bar.addWidget(self.save_btn)
        self.bottom_bar.addStretch()  # pushes totals and buttons to the right
        self.bottom_bar.addWidget(self.total_label)
        self.bottom_bar.addWidget(self.discount_label)
        
        Right_layout.addLayout(grid)
        Right_layout.addWidget(self.table_view)
        Right_layout.addLayout(self.bottom_bar)
        
        Main_layout.addWidget(Left_panel)
        Main_layout.addWidget(Right_panel)
        
    def set_connections(self):
        self.Has_discount_cb.toggled.connect(self.Get_discount_on_bill.setEnabled)
        # self.Completer.activated.connect(self.Get_name_to_search)
        self.Get_id_to_search.returnPressed.connect(self.search_item_by_id)
        self.Get_name_to_search.returnPressed.connect(self.search_item_by_name)
        self.add_button.clicked.connect(self.add_item_to_cart)
        self.delete_button.clicked.connect(self.remove_item_from_cart)
        self.Item_model.itemChanged.connect(self.item_changed)
        self.qty_input.textChanged.connect(self.validate_add_button)
        self.name_input.textChanged.connect(self.validate_add_button)
        QShortcut(QKeySequence("F1"), self).activated.connect(self.clear_ALL_fields)
        QShortcut(QKeySequence("del"), self).activated.connect(self.remove_item_from_cart)
        
    def set_model(self):
        
        self.Item_model = QStandardItemModel()
        self.Item_model.setHorizontalHeaderLabels(["Name", "Cost", "Qty", "Sub-Total"])
        
        self.table_view.setModel(self.Item_model)
        
        for bill_item in self.cart:
            self.add_item_to_table(
                bill_item["name"],
                bill_item["cost"],
                bill_item["quantity"],
                bill_item["sub_total"]
            )
        
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

    def add_item_to_table(self, name, cost, quantity, sub_total):
        cost = float(cost)
        row = [
            QStandardItem(str(name)),
            QStandardItem(f"{cost:.2f}"),  # Formats float to 2 decimal places as str
            QStandardItem(str(quantity)),  # Converts int to str
            QStandardItem(f"{sub_total:.2f}")
        ]
        self.Item_model.appendRow(row)
    
    def fill_fields(self,name ,cost ,description):
        self.name_input.setText(name)
        self.cost_input.setText(str(cost))
        self.desc_input.setText(description)
    def clear_fields(self):
        self.Get_id_to_search.clear()
        self.Get_name_to_search.clear()
        self.name_input.clear()
        self.desc_input.clear()
        self.qty_input.setValue(0)
        self.cost_input.clear()
    def clear_ALL_fields(self):
        self.clear_fields()
        self.cart.clear()
        self.Item_model.removeRows(0, self.Item_model.rowCount())
        self.Calculate_total()
        
    def search_item_by_name(self):
        item_name = self.Get_name_to_search.text()
        item_data = self.inventory.get_item_by_name(item_name)
        
        if item_data:
            self.current_selected_item = item_data
            self.fill_fields(item_data["name"], item_data["cost"], item_data["description"])
            self.searched_item_id = item_data["id"]
        else:
            QMessageBox.warning(
                self,
                "Item Not Found",
                f"Item With Name '{item_name}' not Found",
                QMessageBox.StandardButton.Ok
            )
        self.Get_name_to_search.clear()
    
    def search_item_by_id(self):
        item_id = self.Get_id_to_search.text()
        item_data = self.inventory.get_item_by_id(item_id)
                
        if item_data:
            self.current_selected_item = item_data
            self.fill_fields(item_data["name"], item_data["cost"], item_data["description"])
        else:
            QMessageBox.warning(
                self,
                "Item Not Found",
                f"Item With ID '{item_id}' not Found",
                QMessageBox.StandardButton.Ok
            )
        self.Get_id_to_search.clear()
    
    def remove_item_from_cart(self) -> None:
        selected_row = self.table_view.selectionModel().selectedRows()
        if selected_row:
            row = selected_row[0].row()
            item_name = self.Item_model.index(row, 0).data()
            confirmation = QMessageBox.question(
                self,   # Parent
                "Selection Required", # Window Name
                f"   Are You Sure You Want to Delete the Item? \n─────────────────────────────────── \n Name : {item_name}", # Message
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, # Buttons
                QMessageBox.StandardButton.No   # Default Pointing on the Button No
            )
            
            if confirmation == QMessageBox.StandardButton.Yes:
                self.cart.pop(row)
                self.refresh_table()
                self.Calculate_total()
                QMessageBox.information(
                    self,
                    "Item Deletion",
                    f"  Deleted the Item from the table with \n─────────────────────────────────── \n Name : {item_name}."
                )
        self.clear_fields()
        
    
    def add_item_to_cart(self) -> None:
        
        if self.qty_input.value() <= 0:
            QMessageBox.warning(
                self,
                "Invalid Quantity",
                f"Cannot Add Quantity of '{self.qty_input.value()}' to bill",
                QMessageBox.StandardButton.Ok
            )
            return None
        
        if self.qty_input.value() > self.current_selected_item["quantity"]:
            QMessageBox.warning(
                self,
                "Invalid Quantity",
                f"Not Enough Stock in Inventory '{self.qty_input.value()}'",
                QMessageBox.StandardButton.Ok
            )
            return None
        
        Sub_total = float(self.cost_input.text()) * int(self.qty_input.text())
        
        item = {
            "id" : self.searched_item_id,
            "name": self.name_input.text(),
            "cost": self.cost_input.text(),
            "quantity": self.qty_input.text(),
            "sub_total": Sub_total
        }
        
        if self.cart:
            for item_in_cart in self.cart:
                if item["name"] == item_in_cart["name"]:
                    QMessageBox.warning(
                        self,
                        "Can't Add Item",
                        f"'{item["name"]}' Item is Already in Bill",
                        QMessageBox.StandardButton.Ok
                    )
                    return
        
        self.cart.append(item)
        self.add_item_to_table(item["name"], item["cost"], item["quantity"], item["sub_total"])
        self.Calculate_total()
        self.clear_fields()
        
    def Calculate_total(self):
        Bill_total = sum(item["sub_total"] for item in self.cart)
        Discount_percentage = self.Get_discount_on_bill.value()
        Discounted_total = Bill_total - (Bill_total / 100) * Discount_percentage
        
        self.total_label.setText(f"Total: {Bill_total:.2f}")
        self.discount_label.setText(f"After Discount: {Discounted_total:.2f}")
    
    def item_changed(self, item : QStandardItem) ->  None:
        
        row = item.row()
        col = item.column()
        
        if col == 2:
            cost = float(self.Item_model.item(row, 1).text())
            new_qty = int(item.text())
            new_subtotal = cost * new_qty
            
            self.Item_model.blockSignals(True) # Blocking Signals from Table so No recurssion happens
            self.Item_model.item(row, 3).setText(f"{new_subtotal:.2f}")
            self.Item_model.blockSignals(False) # Re Enabling After Editing.
            
            self.cart[row]["quantity"] = new_qty
            self.cart[row]["sub_total"] = new_subtotal
            
            self.Calculate_total()
        else:    
            return None
    
    def validate_add_button(self):
        name_filled = len(self.name_input.text()) > 0
        qty_filled = self.qty_input.value() > 0
        
        all_filled = name_filled and qty_filled
        
        self.add_button.setEnabled(all_filled)
    
    def refresh_table(self):
        self.Item_model.removeRows(0, self.Item_model.rowCount())
        
        for item in self.cart:
            self.add_item_to_table(
                item["name"],
                item["cost"],
                item["quantity"],
                item["sub_total"]
            )
