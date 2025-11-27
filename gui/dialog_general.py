from PySide6.QtWidgets import QDialog,QDialogButtonBox, QGridLayout, QFrame, QWidget

class DialogGeneral(QDialog):
    def __init__(self, titulo: str,frame: QFrame):
        super().__init__()
        self.setWindowTitle(titulo)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addWidget(frame,0,0)
        self.layout.addWidget(self.buttonBox,1,0)
    def addWidgetP(self, widget: QWidget,columna: int, fila: int):
        self.layout.addWidget(widget,columna,fila)




