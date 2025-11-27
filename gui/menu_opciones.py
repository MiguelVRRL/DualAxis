from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QMenu, QTableView
from pandas.plotting import table

from gui.dialog_nombre_columna import DialogoNombreColumna
from gui.tabla import Tabla
from modelos.tabla_de_datos import TablaDatos


class MenuOpciones(QMenu):
    def __init__(self, padre: QMainWindow,datos: TablaDatos, tabla: QTableView, indice: QModelIndex):
        super().__init__()
        self.__indice: QModelIndex = indice 
        self.__datos = datos.get_dataFrame()
        self.__tabla = tabla
        self.__modelo: Tabla = tabla.model()
         # Actions Básicos
        
        #action_cortar = QAction("Cortar",self)


        #action_copiar = QAction("Copiar", self)
    

        #action_pegar = QAction("Pegar",self)


        # Insertar
        menu_insertar = QMenu("Insertar") 
        
       
        action_insertar_fila = QAction("Insertar fila", self)
        action_insertar_columna = QAction("Insertar columna",self)
        

        menu_insertar.addAction(action_insertar_fila)
        action_insertar_fila.triggered.connect(lambda: self.insertar_fila(-1))


        menu_insertar.addAction(action_insertar_columna)
        action_insertar_columna.triggered.connect(lambda: self.insertar_columna(self.__indice.column()))

        # Eliminar
        menu_eliminar = QMenu("Eliminar")
         

        action_eliminar_fila = QAction("Eliminar fila", self)
        action_eliminar_fila.triggered.connect(lambda: self.__modelo.eliminar_fila(self.__indice.row()))
        action_eliminar_columna = QAction("Eliminar columna",self)
        action_eliminar_columna.triggered.connect(lambda: self.__modelo.eliminar_columna(self.__indice.column())) 

        menu_eliminar.addAction(action_eliminar_fila)
        menu_eliminar.addAction(action_eliminar_columna)



        #self.addAction(action_cortar)
        #self.addAction(action_copiar)
        #self.addAction(action_pegar)
        self.addMenu(menu_eliminar)
        self.addMenu(menu_insertar)

    def insertar_columna(self,posicion:int):
        dlg: DialogoNombreColumna = DialogoNombreColumna(self)
        if dlg.exec_():
            self.__modelo.insertar_columna(posicion,dlg.get_nombre())
    def insertar_fila(self,valor: int):
        print(self.__indice.row())
        self.__modelo.insertar_fila(self.__indice.row())
    def editar_fila(self, row):
        print(f"Editar fila {row}")
    
    def eliminar_fila(self, row):
        print(f"Eliminar fila {row}")
    
    def copiar_valor(self, index):
        value = self.__datos.iloc[index.row(), index.column()]
        print(f"Copiar valor: {value}")
