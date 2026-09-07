from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton, QGridLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from datetime import date, timedelta

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
            self.percentage_label.setStyleSheet("color: gray; font-size: 14px; font-weight: bold;")
            layout.addWidget(self.percentage_label)
                       
class Report_Window(QWidget):
    def __init__(self, inventory, bill_controller):
        super().__init__()
        self.inventory = inventory
        self.bill_controller = bill_controller
        self.set_ui()
        self.set_connections()
        self.get_daily_report()
        
    def set_ui(self):
        main_layout = QGridLayout(self)
        
        self.title_label = QLabel("Reports")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 28px;")
        
        self.daily_button = QPushButton("Daily")
        self.weekly_button = QPushButton("Weekly")
        self.monthly_button = QPushButton("Monthly") 
        
        self.revenue_card = Card("Total Revenue", "0 Rs", "0%")
        self.bill_controller_card = Card("Total Bills", "0 Rs", "0%")
        self.average_sales_card = Card("Average Bill", "0 Rs", "0%")
        
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Sales Over Time")
        self.ax.set_xlabel("Time Span")
        self.ax.set_ylabel("Sales")
        
        self.chart_placeholder = FigureCanvasQTAgg(self.fig)

        # Create
        self.top_items_table = QTableWidget()
        self.top_items_table.setColumnCount(2)
        # Headers
        self.top_items_table.setHorizontalHeaderLabels(["Item Name", "Qty Sold"])
        # Lock editing
        self.top_items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.top_items_table.setFixedWidth(320)
        header = self.top_items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        
        main_layout.addWidget(self.title_label, 0, 0)
        main_layout.addWidget(self.daily_button, 0, 1)
        main_layout.addWidget(self.weekly_button, 0, 2)
        main_layout.addWidget(self.monthly_button, 0, 3)
        main_layout.addWidget(self.revenue_card, 1, 0)
        main_layout.addWidget(self.bill_controller_card, 1, 1)
        main_layout.addWidget(self.average_sales_card, 1, 2)
        main_layout.addWidget(self.top_items_table, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.chart_placeholder, 2, 0, 2, 4)
        
    def set_connections(self):
        self.daily_button.clicked.connect(self.get_daily_report)
        self.weekly_button.clicked.connect(self.get_weekly_report)
        self.monthly_button.clicked.connect(self.get_monthly_report)

    def get_daily_report(self) -> None:
        # Get previous day's report for comparison
        prev_Total_Revenue = self.bill_controller.get_revenue_between_dates(str(date.today() - timedelta(days=1)), str(date.today() - timedelta(days=1)))
        prev_Total_Bills = self.bill_controller.count_bills_between_dates(str(date.today() - timedelta(days=1)), str(date.today() - timedelta(days=1)))
        prev_Average_Sales = prev_Total_Revenue / prev_Total_Bills if prev_Total_Bills > 0 else 0
        
        # Get current day's report
        Total_Revenue = self.bill_controller.get_revenue_between_dates(str(date.today()), str(date.today()))
        Total_Bills = self.bill_controller.count_bills_between_dates(str(date.today()), str(date.today()))
        Top_Sellers = self.bill_controller.get_daily_top_items(str(date.today()))
        Average_Sales = Total_Revenue / Total_Bills if Total_Bills > 0 else 0 
        
        # Calculate percentage changes
        revenue_change = ((Total_Revenue - prev_Total_Revenue) / prev_Total_Revenue * 100) if prev_Total_Revenue > 0 else 0.00
        bills_change = ((Total_Bills - prev_Total_Bills) / prev_Total_Bills * 100) if prev_Total_Bills > 0 else 0.00
        average_sales_change = ((Average_Sales - prev_Average_Sales) / prev_Average_Sales * 100) if prev_Average_Sales > 0 else 0.00
        
        self.update_report(Total_Revenue, Total_Bills, Average_Sales, Top_Sellers, revenue_change, bills_change, average_sales_change)
        self.draw_Graph(["Yesterday", "Today"], [prev_Total_Revenue, Total_Revenue])
    
    def get_weekly_report(self):
        # Get previous Week's report for comparison
        prev_Total_Revenue = self.bill_controller.get_revenue_between_dates(str(date.today() - timedelta(days=7)), str(date.today() - timedelta(days=14)))
        prev_Total_Bills = self.bill_controller.count_bills_between_dates(str(date.today() - timedelta(days=7)), str(date.today() - timedelta(days=14)))
        prev_Average_Sales = prev_Total_Revenue / prev_Total_Bills if prev_Total_Bills > 0 else 0
        
        # Get current Week's report
        Total_Revenue_per_day = []
        for i in range(7):
            day = date.today() - timedelta(days=i)
            daily_revenue = self.bill_controller.get_revenue_between_dates(str(day), str(day))
            Total_Revenue_per_day.append(daily_revenue)
        
        Total_Revenue = self.bill_controller.get_revenue_between_dates(str(date.today() - timedelta(days=7)), str(date.today()))
        Total_Bills = self.bill_controller.count_bills_between_dates(str(date.today() - timedelta(days=7)), str(date.today()))
        Top_Sellers = self.bill_controller.get_top_items(str(date.today() - timedelta(days=7)), str(date.today()))
        Average_Sales = Total_Revenue / Total_Bills if Total_Bills > 0 else 0 
        
        # Calculate percentage changes
        revenue_change = ((Total_Revenue - prev_Total_Revenue) / prev_Total_Revenue * 100) if prev_Total_Revenue > 0 else 0.00
        bills_change = ((Total_Bills - prev_Total_Bills) / prev_Total_Bills * 100) if prev_Total_Bills > 0 else 0.00
        average_sales_change = ((Average_Sales - prev_Average_Sales) / prev_Average_Sales * 100) if prev_Average_Sales > 0 else 0.00
        
        self.update_report(Total_Revenue, Total_Bills, Average_Sales, Top_Sellers, revenue_change, bills_change, average_sales_change)
        self.draw_Graph([f"Day {i+1}" for i in range(7)], Total_Revenue_per_day)
    
    def get_monthly_report(self):
        # Get previous month's report for comparison
        prev_Total_Revenue = self.bill_controller.get_revenue_between_dates(str(date.today() - timedelta(days=30)), str(date.today() - timedelta(days=60)))
        prev_Total_Bills = self.bill_controller.count_bills_between_dates(str(date.today() - timedelta(days=30)), str(date.today() - timedelta(days=60)))
        prev_Average_Sales = prev_Total_Revenue / prev_Total_Bills if prev_Total_Bills > 0 else 0
        
        # Get current month's report
        Total_Revenue = self.bill_controller.get_revenue_between_dates(str(date.today() - timedelta(days=30)), str(date.today()))
        Total_Bills = self.bill_controller.count_bills_between_dates(str(date.today() - timedelta(days=30)), str(date.today()))
        Top_Sellers = self.bill_controller.get_top_items(str(date.today() - timedelta(days=30)), str(date.today()))
        Average_Sales = Total_Revenue / Total_Bills if Total_Bills > 0 else 0
        
        Total_Revenue_per_day = []
        for i in range(30):
            day = date.today() - timedelta(days=i)
            daily_revenue = self.bill_controller.get_revenue_between_dates(str(day), str(day))
            Total_Revenue_per_day.append(daily_revenue)
        
        # Calculate percentage changes
        revenue_change = ((Total_Revenue - prev_Total_Revenue) / prev_Total_Revenue * 100) if prev_Total_Revenue > 0 else 0.00
        bills_change = ((Total_Bills - prev_Total_Bills) / prev_Total_Bills * 100) if prev_Total_Bills > 0 else 0.00
        average_sales_change = ((Average_Sales - prev_Average_Sales) / prev_Average_Sales * 100) if prev_Average_Sales > 0 else 0.00        
        
        self.update_report(Total_Revenue, Total_Bills, Average_Sales, Top_Sellers, revenue_change, bills_change, average_sales_change)
        self.draw_Graph([f"{i+1}" for i in range(30)], Total_Revenue_per_day)
    
    def update_report(self,total_revenue, total_bills, average_sales, top_sellers, rev_change, bills_change, avg_sales_change):
        
        # Setting the Values in the Cards
        self.revenue_card.value_label.setText(f"{total_revenue:.2f} Rs")
        self.bill_controller_card.value_label.setText(f"{total_bills} Bills")
        self.average_sales_card.value_label.setText(f"{average_sales:.2f} Rs")
        self.revenue_card.percentage_label.setText(f"{rev_change:.2f}%")
        self.bill_controller_card.percentage_label.setText(f"{bills_change:.2f}%")
        self.average_sales_card.percentage_label.setText(f"{avg_sales_change:.2f}%")
        
        # Coloring percentage changes based on positive or negative values
        if rev_change > 0:
            self.revenue_card.percentage_label.setStyleSheet("color: green; font-size: 14px; font-weight: bold;")
        elif rev_change < 0:
            self.revenue_card.percentage_label.setStyleSheet("color: red; font-size: 14px; font-weight: bold;")
        else:
            self.revenue_card.percentage_label.setStyleSheet("color: gray; font-size: 14px; font-weight: bold;")

        if bills_change > 0:
            self.bill_controller_card.percentage_label.setStyleSheet("color: green; font-size: 14px; font-weight: bold;")
        elif bills_change < 0:
            self.bill_controller_card.percentage_label.setStyleSheet("color: red; font-size: 14px; font-weight: bold;")
        else:
            self.bill_controller_card.percentage_label.setStyleSheet("color: gray; font-size: 14px; font-weight: bold;")
        
        if avg_sales_change > 0:
            self.average_sales_card.percentage_label.setStyleSheet("color: green; font-size: 14px; font-weight: bold;")
        elif avg_sales_change < 0:
            self.average_sales_card.percentage_label.setStyleSheet("color: red; font-size: 14px; font-weight: bold;")
        else:
            self.average_sales_card.percentage_label.setStyleSheet("color: gray; font-size: 14px; font-weight: bold;")
            
        self.update_top_sellers_table(top_sellers)
        
    def draw_Graph(self,labels ,values) -> None:
        self.ax.clear()

        self.ax.bar(labels, values)
        self.ax.set_title("Revenue Comparison")
        self.ax.set_ylabel("Revenue (Rs)")
        self.ax.set_xlabel("Time Span")

        self.chart_placeholder.draw()
        
    def update_top_sellers_table(self, top_sellers):
        self.top_items_table.setRowCount(len(top_sellers))
        for i, (name, qty) in enumerate(top_sellers):
            self.top_items_table.setItem(i, 0, QTableWidgetItem(name))       # Item Name
            self.top_items_table.setItem(i, 1, QTableWidgetItem(str(qty)))   # Quantity Sold