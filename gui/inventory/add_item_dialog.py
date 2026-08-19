from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDoubleSpinBox, 
    QSpinBox, QDialogButtonBox, QVBoxLayout, QLabel, QDateEdit, QCheckBox
)
from PyQt6.QtCore import Qt
from datetime import date

class Add_Item(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Item to Inventory")
        self.setFixedWidth(500)
        self.set_ui()
        self.set_connection()
            
    def set_ui(self):
        # Layout of the Dialouge
        self.Main_Layout = QVBoxLayout(self)
        
        # Top Label
        self.Top_label = QLabel("Add Items Detials")
        font = self.Top_label.font()
        font.setPointSize(15)
        self.Top_label.setFont(font)
        
        # Form Layout
        form_layout = QFormLayout()
        
        # Getting Details
        self.get_id = QLineEdit()
        self.get_name = QLineEdit()
        self.get_cost = QDoubleSpinBox()
        self.get_cost.setMaximum(99999.99)
        self.get_quantity = QSpinBox()
        self.get_quantity.setMaximum(999999)
        self.get_description = QLineEdit()
        self.get_expirey = QDateEdit()
        self.get_expirey.setEnabled(False)
        
        # Expirey Checkbox
        self.expiry_cb = QCheckBox("Has A Expirey")
        self.expiry_cb.setCheckState(Qt.CheckState.Unchecked)
        self.expiry_cb.toggled.connect(self.get_expirey.setEnabled)
        
        self.get_id.setPlaceholderText("Enter Item ID")
        self.get_name.setPlaceholderText("Enter Item Name")
        self.get_description.setPlaceholderText("Enter Item Description")
        
        # Addin to Form Layout
        form_layout.addRow("Item ID*", self.get_id)
        form_layout.addRow("Item Name*", self.get_name)
        form_layout.addRow("Cost*", self.get_cost)
        form_layout.addRow("Quantity*", self.get_quantity)
        form_layout.addRow("Description", self.get_description)
        form_layout.addRow("", self.expiry_cb)
        form_layout.addRow("Expiry Date", self.get_expirey)
        
        # OK Button
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.ok_button = self.button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.ok_button.setEnabled(False)
        
        # Connect built-in slot behavior
        self.button_box.accepted.connect(self.accept)  # Returns QDialog.DialogCode.Accepted
        self.button_box.rejected.connect(self.reject)  # Returns QDialog.DialogCode.Rejected
        
        # Setting the Main Layout.
        self.Main_Layout.addWidget(self.Top_label)
        self.Main_Layout.addLayout(form_layout)
        self.Main_Layout.addWidget(self.button_box)
               
    def set_connection(self):
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        self.get_id.textChanged.connect(self.validate_form)
        self.get_name.textChanged.connect(self.validate_form)
        self.get_cost.textChanged.connect(self.validate_form)
        self.get_quantity.textChanged.connect(self.validate_form)
    
    def get_item_data(self):
        if self.expiry_cb == Qt.CheckState.Checked:
            expiry = self.get_expirey.date().toString()
        else:
            expiry = "No Expiry"
        return {
            "id": self.get_id.text(),
            "name": self.get_name.text(),
            "cost": self.get_cost.value(),
            "quantity": self.get_quantity.value(),
            "description": self.get_description.text(),
            "entry_date" : date.today(),
            "expiry_date": expiry
        }
        
    def validate_form(self):
        id_filled = len(self.get_id.text().strip()) > 0
        name_filled = len(self.get_name.text().strip()) > 0
        cost_filled = self.get_cost.value() > 0
        quantity_filled = self.get_quantity.value() > 0
        
        all_filled = id_filled and name_filled and cost_filled and quantity_filled
        
        self.ok_button.setEnabled(all_filled)
        