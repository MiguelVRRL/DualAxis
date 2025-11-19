from typing import override
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import Qt, QModelIndex


from modelos.tabla_de_datos import TablaDatos

class Tabla(QAbstractTableModel):

    def __init__(self, data: TablaDatos):
        super().__init__()
        self._data = data.get_dataFrame()
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
            self._data.iloc[index.row(),index.column()] = value
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



    def set_modificado(self) -> None:
        self.__modificado = False

    def get_modificado(self) -> bool:
        return self.__modificado
