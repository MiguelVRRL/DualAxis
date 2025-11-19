from PySide6.QtWidgets import QDialog,QDialogButtonBox, QGridLayout, QListWidget, QLabel

class UnVarDialog(QDialog):
    def __init__(self, titulo: str,atributos: list[str]):
        super().__init__()
        self.__atributos = atributos
        self.setWindowTitle(titulo)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        label_atributos = QLabel("Atributos")

        self.lista_atributos = QListWidget()
        self.lista_atributos.setFixedSize(175,300)
        self.lista_atributos.addItems(self.__atributos)
        self.lista_atributos.doubleClicked.connect(self.add_item)

        label_variable = QLabel("Variable") 

        self.lista_x = QListWidget()
        self.lista_x.setFixedSize(175,300)
        self.lista_x.doubleClicked.connect(self.quitar_item)
        
        self.layout.addWidget(label_atributos,0,0)
        self.layout.addWidget(label_variable,0,1)
        self.layout.addWidget(self.lista_atributos,1,0)
        self.layout.addWidget(self.lista_x,1,1)
        self.layout.addWidget(self.buttonBox,2,1)
    def get_atributo(self) -> str:
        return self.lista_x.item(0).text()
    def add_item(self,i) -> None:
        if self.lista_x.count() < 1:
            self.lista_x.addItem(self.lista_atributos.item(i.row()).text())
            self.lista_atributos.takeItem(i.row())

    def quitar_item(self,i) -> None:
        self.lista_atributos.addItem(self.lista_x.item(i.row()).text())
        self.lista_x.takeItem(i.row())

