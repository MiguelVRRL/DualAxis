from PySide6.QtWidgets import QMainWindow, QTableView
import pandas as pd

from gui.menubar import MenuBar
from gui.tabla import Tabla



class VentanaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.table = QTableView()

        self.setMenuBar(MenuBar(self.table))

        self.setWindowTitle("DualAxis")



        

       
        self.setCentralWidget(self.table)
        
    def get_ventana(self) -> object:
        return self
