from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal

class LoginWidget(QWidget):
    
    login_successful = pyqtSignal(dict)
    
    def __init__(self, auth):
        super().__init__()
        
         