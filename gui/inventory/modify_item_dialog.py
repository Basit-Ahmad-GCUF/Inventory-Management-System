from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QFormLayout, QLineEdit, 
    QDoubleSpinBox, QSpinBox, QDateEdit, QCheckBox, QLabel
)
from PyQt6.QtCore import Qt, QDate, QEvent, pyqtSignal

class Modify_Item(QDialog):
    
    data_saved = pyqtSignal(dict)
    request_search = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modify Item Detials")
        self.setFixedWidth(500)
        
        self.default_entry_date = QDate.currentDate().toString("yyyy-MM-dd")
        
        self.set_ui()
        self.set_connections()
        
    def set_ui(self):
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        
        # Form Layout
        form_layout = QFormLayout()
        
        # Xreating Elments and Setting them up One Bye one
        
        self.top_label = QLabel("Modify Items")
        font = self.top_label.font()
        font.setPointSize(15)
        self.top_label.setFont(font)

        self.id_input_label = QLabel("Enter ID:")
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter Item ID to Find")
        self.id_input.installEventFilter(self)
        
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-weight: bold;")
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")
        self.cost_input = QDoubleSpinBox()
        self.cost_input.setMaximum(999999.99)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(999999)
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Item Descrition")
        self.expiry_cb = QCheckBox("Has Expiry")
        self.expiry_cb.setCheckState(Qt.CheckState.Unchecked)
        self.expiry_input = QDateEdit()
        self.expiry_input.setEnabled(False)
        self.expiry_cb.toggled.connect(self.expiry_input.setEnabled)
        
        form_layout.addRow("Name*"       , self.name_input)
        form_layout.addRow("Cost*"       , self.cost_input)
        form_layout.addRow("Quantity*"   , self.quantity_input)
        form_layout.addRow("Description" , self.description_input)
        form_layout.addRow(""            , self.expiry_cb)
        form_layout.addRow("Expiry Date" , self.expiry_input)
        
        self.button = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Discard | 
            QDialogButtonBox.StandardButton.Close 
        )
        self.save_btn = self.button.button(QDialogButtonBox.StandardButton.Save)
        self.save_btn.setEnabled(False)
        self.discard_btn = self.button.button(QDialogButtonBox.StandardButton.Discard)
        self.discard_btn.setEnabled(False)
        self.close_btn = self.button.button(QDialogButtonBox.StandardButton.Close)

        # Enter in the ID field is used for searching and must not trigger the
        # dialog's default Save action as well.
        self.save_btn.setAutoDefault(False)
        self.save_btn.setDefault(False)
        self.discard_btn.setAutoDefault(False)
        self.discard_btn.setDefault(False)
        self.close_btn.setAutoDefault(False)
        self.close_btn.setDefault(False)
        
        self.message_lable = QLabel("")
        self.message_lable.setStyleSheet("color: green; font-weight: bold;")
        
        self.main_layout.addWidget(self.top_label)
        self.main_layout.addWidget(self.id_input_label)
        self.main_layout.addWidget(self.id_input)
        self.main_layout.addWidget(self.error_label)
        self.main_layout.addLayout(form_layout)
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.message_lable)
        
    def set_connections(self):
        self.id_input.returnPressed.connect(self.item_id_to_search)
        self.save_btn.clicked.connect(self.save_data)
        self.discard_btn.clicked.connect(self.discard_data)
        self.close_btn.clicked.connect(self.reject)
        self.name_input.textChanged.connect(self.validate_form)
        self.cost_input.textChanged.connect(self.validate_form)
        self.quantity_input.textChanged.connect(self.validate_form)

    def eventFilter(self, watched, event):
        if watched is self.id_input and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.item_id_to_search()
                event.accept()
                return True
        return super().eventFilter(watched, event)
        
    def fill_fields(self, item_data) -> None:
        if item_data:
            self.error_label.clear()
            self.name_input.setText(item_data["name"])
            self.cost_input.setValue(item_data["cost"])
            self.quantity_input.setValue(item_data["quantity"])
            self.description_input.setText(item_data["description"])
            expiry = item_data["expiry_date"]
            if expiry and expiry not in ("No Expiry", "No Expirey"):
                self.expiry_cb.setChecked(True)
                self.expiry_input.setDate(QDate.fromString(expiry, "yyyy-MM-dd"))
            else:
                self.expiry_cb.setChecked(False)
                self.expiry_input.setDate(QDate.currentDate())
            self.expiry_input.setEnabled(self.expiry_cb.isChecked())

            self.default_entry_date = item_data["entry_date"]
        if not item_data:
            self.clear_fields()
            self.error_label.setText(f" ⚠️ Item ID not found!")

    def item_id_to_search(self) -> str:
        item_id = self.id_input.text().strip()
        if not item_id:
            self.error_label.setText(" 🛑 Please enter an item ID.")
            return
        self.error_label.clear()
        self.request_search.emit(item_id)

    def modified_item_data(self) -> dict:
        if self.expiry_cb.isChecked():
            expiry = self.expiry_input.date().toString("yyyy-MM-dd")
        else:
            expiry = "No Expirey"
        data = {
            "id" : self.id_input.text(),
            "name": self.name_input.text(),
            "cost": self.cost_input.value(),
            "quantity": self.quantity_input.value(),
            "description": self.description_input.text(),
            "entry_date": self.default_entry_date,
            "expiry_date": expiry
        }
        return data

    def clear_fields(self) -> None:
        self.id_input.clear()
        self.name_input.clear()
        self.cost_input.setValue(0)
        self.quantity_input.setValue(0)
        self.description_input.clear()
        self.expiry_cb.setChecked(False)
        self.expiry_input.setDate(QDate.currentDate())

    def save_data(self) -> dict:
        data = self.modified_item_data()
        self.data_saved.emit(data)
        self.message_lable.setText(" ✔️ Item Modified Succesfully!")
        self.clear_fields()

    def discard_data(self) -> None:
        self.message_lable.setText(" ❌ Item Modification Discarded!")
        self.clear_fields()
        
    def validate_form(self):
        name_filled = len(self.name_input.text().strip()) > 0
        cost_filled = self.cost_input.value() > 0
        quantity_filled = self.quantity_input.value() > 0
        
        All_filled = name_filled and cost_filled and quantity_filled
        
        self.save_btn.setEnabled(All_filled)
        self.discard_btn.setEnabled(All_filled)
        