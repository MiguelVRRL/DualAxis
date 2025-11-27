from typing import override
from PySide6.QtWidgets import QDialog,QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QListWidget, QVBoxLayout, QGroupBox

class DosVarDialog(QDialog):
    def __init__(self, titulo: str,atributos: list[str], *tipo_excluido):
        super().__init__()
        self.__tipos_excluidos = tipo_excluido
        self.__atributos = atributos
        self.setWindowTitle(titulo)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


        grupo_atributos = QGroupBox("Atributos")
        layout_atributos = QVBoxLayout()
        grupo_atributos.setLayout(layout_atributos)

        self.lista_atributos = QListWidget()
        self.lista_atributos.setFixedSize(175,300)
        self.lista_atributos.addItems(self.__atributos)
        self.lista_atributos.doubleClicked.connect(self.add_item)

        layout_atributos.addWidget(self.lista_atributos)

        grupo_variables = QGroupBox("Variables")
        layout_variables = QVBoxLayout()
        grupo_variables.setLayout(layout_variables)

        label_variable_x = QLabel("Variable X") 

        self.lista_x = QListWidget()
        self.lista_x.setFixedSize(175,130)
        self.lista_x.doubleClicked.connect(self.quitar_item_x)
        
        label_variable_y = QLabel("Variable Y") 

        self.lista_y = QListWidget()
        self.lista_y.setFixedSize(175,130)
        self.lista_y.doubleClicked.connect(self.quitar_item_y)
        # layout de variables
        layout_variables.addWidget(label_variable_x)
        layout_variables.addWidget(self.lista_x)
        layout_variables.addWidget(label_variable_y)
        layout_variables.addWidget(self.lista_y)

        # layout principal
        self.layout.addWidget(grupo_atributos,0,0)
        self.layout.addWidget(grupo_variables,0,1)
        self.layout.addWidget(self.buttonBox,1,1)

    def add_item(self,i) -> None:
        if self.lista_x.count() == 0:
            if self.lista_atributos.item(i.row()).text() in self.__tipos_excluidos:
                return

            self.lista_x.addItem(self.lista_atributos.item(i.row()).text())
            self.lista_atributos.takeItem(i.row())
        elif self.lista_x.count() == 1 and self.lista_y.count() == 0:


            self.lista_y.addItem(self.lista_atributos.item(i.row()).text())
            self.lista_atributos.takeItem(i.row())

    def quitar_item_x(self,i) -> None: 
        self.lista_atributos.addItem(self.lista_x.item(i.row()).text())
        self.lista_x.takeItem(i.row())
    def quitar_item_y(self,i) -> None:
        self.lista_atributos.addItem(self.lista_y.item(i.row()).text())
        self.lista_y.takeItem(i.row())
    
    def get_atributo_x(self) -> str:
        return self.lista_x.item(0).text()
    def get_atributo_y(self) -> str:
        return self.lista_y.item(0).text()

