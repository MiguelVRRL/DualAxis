

from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import Qt, QModelIndex

class TableModel(QAbstractTableModel):
    def __init__(self, data,headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]
    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
            # Headers de columnas desde la lista
                return self._headers[section] 
        
            elif orientation == Qt.Vertical:
            # Headers de filas - siempre números
                return str(section + 1)
    
        return None
