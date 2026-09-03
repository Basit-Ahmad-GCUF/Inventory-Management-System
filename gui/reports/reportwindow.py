from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton, QGridLayout,
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Card(QWidget):
    def __init__(self, title, value, percentage_change=None):
        super().__init__()
        self.title = title
        self.value = value
        self.percentage_change = percentage_change
        self.set_ui()
        self.setStyleSheet("color: black; background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
    
    def set_ui(self):
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.value_label = QLabel(str(self.value))
        self.value_label.setStyleSheet("font-size: 16px;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        if self.percentage_change is not None:
            self.percentage_label = QLabel(self.percentage_change)
            self.percentage_label.setStyleSheet("font-size: 14px;")
            layout.addWidget(self.percentage_label)
                       
class Report_Window(QWidget):
    def __init__(self, inventory, bill_controller):
        super().__init__()
        self.inventory = inventory
        self.bill_controller = bill_controller
        self.set_ui()
        self.set_connections()
    
    def set_ui(self):
        main_layout = QGridLayout(self)
        
        self.title_label = QLabel("Reports")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 24px;")
        
        self.daily_button = QPushButton("Daily")
        self.weekly_button = QPushButton("Weekly")
        self.monthly_button = QPushButton("Monthly") 
        
        self.revenue_card = Card("Total Revenue", "+$10,000", "+13%")
        self.bill_controller_card = Card("Total Bills", "50", "+8%")
        self.average_sales_card = Card("Average Sales", "+$200", "+5%")
        
        self.chart_placeholder = QLabel("[ Chart goes here ]")
        self.chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_placeholder.setFrameShape(QFrame.Shape.Box)

        self.items_placeholder = QLabel("[ Top Items ]")
        self.items_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.items_placeholder.setFrameShape(QFrame.Shape.Box)
        
        main_layout.addWidget(self.title_label, 0, 0)
        main_layout.addWidget(self.daily_button, 0, 1)
        main_layout.addWidget(self.weekly_button, 0, 2)
        main_layout.addWidget(self.monthly_button, 0, 3)
        main_layout.addWidget(self.revenue_card, 1, 0)
        main_layout.addWidget(self.bill_controller_card, 1, 1)
        main_layout.addWidget(self.average_sales_card, 1, 2)
        main_layout.addWidget(self.chart_placeholder, 2, 0, 2, 3)
        main_layout.addWidget(self.items_placeholder, 2, 3, 2, 1)
        
    def set_connections(self):
        self.daily_button.clicked.connect(self.get_daily_report)
        self.weekly_button.clicked.connect(self.get_weekly_report)
        self.monthly_button.clicked.connect(self.get_monthly_report)

    def get_daily_report(self):
        self.update_report()
    
    def get_weekly_report(self):
        self.update_report()
    
    def get_monthly_report(self):
        self.update_report()
    
    def update_reports(self):
        pass
        
        
        