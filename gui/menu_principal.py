from typing import override
from PySide6.QtWidgets import QMainWindow, QTableView, QMessageBox, QWidget, QVBoxLayout
from PySide6.QtGui import QCloseEvent


from gui.menubar import MenuBar
from gui.tabla import Tabla
from modelos import TablaDatos



class VentanaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.__datos = TablaDatos()
        self.__tabla = QTableView()
        self.__tabla.setModel(Tabla(self.__datos))
        self.__menu_bar = MenuBar(self.__tabla,self.__datos)

        self.setMenuBar(self.__menu_bar)

        self.setWindowTitle("DualAxis")
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        layout.addWidget(self.__tabla)
        
        self.setCentralWidget(widget)
        

    
    @override
    def closeEvent(self, event: QCloseEvent, /) -> None:
        
        confirmacion = QMessageBox.question(self, "Confirmation", "Estas seguro de que quieres cerrar DualAxis?", QMessageBox.Yes | QMessageBox.No)

        if confirmacion == QMessageBox.Yes:
            self.__menu_bar.cerrar_app()
            event.accept()  
        else:
            event.ignore()     
    def get_ventana(self) -> object:
        return self
