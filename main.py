import sys
from PySide6.QtWidgets import QApplication

from gui import VentanaPrincipal


def main():
    app = QApplication(sys.argv)

    window = VentanaPrincipal()
    window.showMaximized()
    app.setStyle('Universal')
    _ = app.exec()

if __name__ == "__main__":
    main()
