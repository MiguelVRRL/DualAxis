from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow

class VentanaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DualAxis")
        
        
