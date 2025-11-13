from PySide6.QtWidgets import QMainWindow

from gui.menubar import MenuBar



class VentanaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setMenuBar(MenuBar())

        self.setWindowTitle("DualAxis")


        
        
