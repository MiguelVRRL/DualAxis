from typing import override
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import Qt, QModelIndex
import pandas as pd

from modelos.tabla_de_datos import TablaDatos

class Tabla(QAbstractTableModel):

    def __init__(self, data: TablaDatos | pd.DataFrame):
        super().__init__()
        if isinstance(data,TablaDatos):
            self._data = data.get_dataFrame()
        else:
            self._data = data
        self.__modificado: bool = False

    @override
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
    @override
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self.__modificado = True
            valor = value 
            if valor.isdecimal():
                valor = int(valor)
        
            self._data.iloc[index.row(),index.column()] = valor
            return True
    @override
    def rowCount(self, index: QModelIndex ):
        return self._data.shape[0]
    @override
    def columnCount(self, index):
        return self._data.shape[1]
    @override
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])
    @override
    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )

    def insertar_fila(self, position,parent=QModelIndex()):
    
        self.beginInsertRows(parent, position, position)
    
        # Método más directo - añadir fila vacía

        for i in range(len(self._data)-2, position-1, -1):  # -2 porque ya añadimos una fila
            if i >= position:
                self._data.iloc[i+1] = self._data.iloc[i].copy()
        lista_elementos = []
        for i in self._data.dtypes:
            match i:
                case 'int64':
                    lista_elementos.append(0)
                case 'object':
                    lista_elementos.append(' ')
                case 'bool':
                    lista_elementos.append(True)
                case 'float64':
                    lista_elementos.append(0.0)


        self._data.loc[len(self._data)] = lista_elementos
    

        for i in range(len(self._data)-2, position-1, -1):
            if i >= position:
                self._data.iloc[i+1] = self._data.iloc[i].copy()
    

        self._data.loc[position] = lista_elementos
        self.endInsertRows()
        self.__modificado = True

        return True


    def eliminar_fila(self,position, parent=QModelIndex()):
        # Verificar que hay filas para eliminar
        if self.rowCount(parent) <= 1 or position >= self.rowCount(parent) :
            return False
     
    
        # Comenzar a eliminar - UNA fila en la última posición
        self.beginRemoveRows(parent, position, position)
    
        # Eliminar la última fila del DataFrame
        self._data.drop(self._data.index[position], inplace=True)
        self._data.reset_index(drop=True, inplace=True)
        # Finalizar la eliminación
        self.endRemoveRows()
        self.__modificado = True
        return True
    def insertar_columna(self, position, nombre_columna, parent=QModelIndex()):

        # Verificar posición válida
        if position < 0 or position > self.columnCount(parent):
            return False
    
        # Comenzar a insertar columnas
        self.beginInsertColumns(parent, position, position)
    
        # Insertar la nueva columna en el DataFrame

        self._data.insert(position, nombre_columna, [""] * len(self._data))
    
        # Finalizar la inserción
        self.endInsertColumns()
        self.__modificado = True
        return True
    def eliminar_columna(self, position, parent=QModelIndex()):

        # Verificar que la posición sea válida
        if position < 0 or position >= self.columnCount(parent):
            print(f"Posición {position} inválida. Columnas disponibles: 0-{self.columnCount(parent)-1}")
            return False
    
        # Verificar que no sea la última columna
        if self.columnCount(parent) <= 1:
            QMessageBox.warning(None, "Error", "No se puede eliminar la última columna")
            return False
    
        # Comenzar a eliminar columnas
        self.beginRemoveColumns(parent, position, position)
    
        # Obtener nombre de la columna y eliminarla
        nombre_columna = self._data.columns[position]
        self._data = self._data.drop(columns=[nombre_columna])
    
        # Finalizar la eliminación
        self.endRemoveColumns()
        self.__modificado = True
    

        return True
    def set_modificado(self) -> None:
        self.__modificado = False

    def get_modificado(self) -> bool:
        return self.__modificado
