from PySide6.QtWidgets import QDialog,QDialogButtonBox, QVBoxLayout, QLabel

class ColumnDialog(QDialog):
    def __init__(self, titulo: str):
        super().__init__()

        self.setWindowTitle(titulo)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

