from typing import override
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import Qt, QModelIndex

class Tabla(QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self._data = data
    
    @override
    def data(self, index, role: Qt.DisplayRole) -> str:
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
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
