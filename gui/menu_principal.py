from PySide6.QtWidgets import QMainWindow, QTableView
import pandas as pd

from gui.menubar import MenuBar
from gui.tabla import Tabla



class VentanaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.__tabla = QTableView()
        self.__datos = pd.DataFrame()
        self.__menu_bar = MenuBar(self.__tabla,self.__datos)
        self.setMenuBar(self.__menu_bar)

        self.setWindowTitle("DualAxis")
       
        self.setCentralWidget(self.__tabla)
        
    def get_ventana(self) -> object:
        return self
