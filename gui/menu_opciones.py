from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QMenu, QTableView

from modelos.tabla_de_datos import TablaDatos


class MenuOpciones(QMenu):
    def __init__(self, padre: QMainWindow,datos: TablaDatos, tabla: QTableView, index: QModelIndex):
        super().__init__()
        self.__datos = datos.get_dataFrame()
        self.__tabla = tabla
        
         # Actions Básicos
        
        action_cortar = QAction("Cortar",self)


        action_copiar = QAction("Copiar", self)
    

        action_pegar = QAction("Pegar",self)


        # Insertar
        menu_insertar = QMenu("Insertar") 
        
        action_insertar_celda_arriba = QAction("Insertar celda arriba",self)
        action_insertar_celda_abajo = QAction("Insertar celda abajo",self)
        action_insertar_fila = QAction("Insertar fila", self)
        action_insertar_columna = QAction("Insertar columna",self)

        menu_insertar.addAction(action_insertar_celda_arriba)
        menu_insertar.addAction(action_insertar_celda_abajo)
        menu_insertar.addAction(action_insertar_fila)
        menu_insertar.addAction(action_insertar_columna)

        # Eliminar
        menu_eliminar = QMenu("Eliminar")
        
        action_eliminar_celda = QAction("Eliminar celda",self)
        action_eliminar_fila = QAction("Eliminar fila", self)
        action_eliminar_columna = QAction("Eliminar columna",self)
       
        menu_eliminar.addAction(action_eliminar_celda)
        menu_eliminar.addAction(action_eliminar_fila)
        menu_eliminar.addAction(action_eliminar_columna)



        self.addAction(action_cortar)
        self.addAction(action_copiar)
        self.addAction(action_pegar)
        self.addMenu(menu_eliminar)
        self.addMenu(menu_insertar)

        
    
    def editar_fila(self, row):
        print(f"Editar fila {row}")
    
    def eliminar_fila(self, row):
        print(f"Eliminar fila {row}")
    
    def copiar_valor(self, index):
        value = self.__datos.iloc[index.row(), index.column()]
        print(f"Copiar valor: {value}")
