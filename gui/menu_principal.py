from typing import override
from PySide6.QtWidgets import QLabel, QMainWindow, QTableView, QMessageBox, QWidget, QVBoxLayout, QGroupBox,QHBoxLayout, QLabel, QGridLayout
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import QTimer

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

        grupo_resumen = QGroupBox("Resumen")
        grupo_resumen.setFixedWidth(500)

        layout_resumen = QGridLayout()

        layout_resumen.addWidget(QLabel("Nº de elementos: "),0,1)
        self.__num_elem = QLabel(str(self.__datos.get_num_elems_total()))
        layout_resumen.addWidget(self.__num_elem,0,2)


        layout_resumen.addWidget(QLabel("Nº de atributos"),0,3)
        self.__num_atributos = QLabel(str(self.__datos.get_num_atributos()))
        layout_resumen.addWidget(self.__num_atributos,0,4)
        
        grupo_resumen.setLayout(layout_resumen)
        timer = QTimer(self)
        timer.timeout.connect(self.actualizar_resumen)
        timer.start(500)


        layout.addWidget(grupo_resumen) 
        

    @override
    def closeEvent(self, event: QCloseEvent, /) -> None:
        
        confirmacion = QMessageBox.question(self, "Confirmation", "Estas seguro de que quieres cerrar DualAxis?", QMessageBox.Yes | QMessageBox.No)

        if confirmacion == QMessageBox.Yes:
            self.__menu_bar.cerrar_app()
            event.accept()  
        else:
            event.ignore() 

    def actualizar_resumen(self) -> None:
        self.__num_elem.setText(str(self.__datos.get_num_elems_total()))
        self.__num_atributos.setText(str(self.__datos.get_num_atributos()))
    def get_ventana(self) -> object:
        return self
