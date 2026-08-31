from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, 
    QVBoxLayout, QPushButton, QStackedWidget, QLabel
)
from gui.inventory.inventory_page import Inventory_Page
from gui.bills.billing_page import Billing_Window

class MainWindow(QMainWindow):
    def __init__(self, inventory, bill_controller):
        super().__init__()
        self.inventory = inventory
        self.bill_controller = bill_controller
        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        self.setWindowTitle("Inventory Management System")
        self.resize(800,400)
        
        # Main Window of the Screen That Hold the Sidebar and the Content menu.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout That is Horizontal.
        self.main_parent_layout = QHBoxLayout(central_widget)
        # Setting Up the Sidebar and Content Menu.
        self.set_sidebar()
        self.set_context_menu()
        
    def set_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        
        sidebar_layout = QVBoxLayout(sidebar)
        
        self.Dashboard_button = QPushButton("Dashboard")
        self.Inventory_button = QPushButton("Inventory")
        self.Billing_button = QPushButton("Billing")
        self.Report_button = QPushButton("Reports")
        self.settings_button = QPushButton("Setting")
        self.Logout_buton = QPushButton("Logout")
        
        self.Main_label = QLabel("Main")
        self.Reports_label = QLabel("Reports")
        self.Additional_label = QLabel("Additionals")
        
        self.seperating_line = QLabel("───────────────────────────────────────────")
        
        sidebar_layout.addWidget(self.Main_label)
        sidebar_layout.addWidget(self.Dashboard_button)
        sidebar_layout.addWidget(self.Inventory_button)
        sidebar_layout.addWidget(self.Billing_button)
        sidebar_layout.addWidget(self.Reports_label)
        sidebar_layout.addWidget(self.Report_button)
        sidebar_layout.addWidget(self.seperating_line)
        sidebar_layout.addWidget(self.Additional_label)
        sidebar_layout.addWidget(self.settings_button)
        sidebar_layout.addWidget(self.Logout_buton)
        
        self.main_parent_layout.addWidget(sidebar)
    
    def set_context_menu(self):
        
        self.stacked_widget = QStackedWidget()
        
        p1 = QWidget()
        p1_layout = QVBoxLayout(p1)
        p1_layout.addWidget(QLabel("Welcome to the Dashboard"))
        
        self.p2 = Inventory_Page(self.inventory)
        
        self.p3 = Billing_Window(self.inventory, self.bill_controller)
                
        p4 = QWidget()
        p4_layout = QVBoxLayout(p4)
        p4_layout.addWidget(QLabel("Reports will be show here"))
                
        p5 = QWidget()
        p5_layout = QVBoxLayout(p5)
        p5_layout.addWidget(QLabel("All settings are Here."))
        
        self.stacked_widget.addWidget(p1)
        self.stacked_widget.addWidget(self.p2)
        self.stacked_widget.addWidget(self.p3)
        self.stacked_widget.addWidget(p4)
        self.stacked_widget.addWidget(p5)
        
        self.main_parent_layout.addWidget(self.stacked_widget)
    
    def _connect_signals(self):
        
        self.p3.Bill_Saved.connect(self.p2.refresh_table)
        
        self.Dashboard_button.clicked.connect(lambda:  self.stacked_widget.setCurrentIndex(0))
        self.Inventory_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.Billing_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.Report_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))