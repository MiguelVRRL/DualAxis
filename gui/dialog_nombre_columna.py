from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt

class DialogoNombreColumna(QDialog):
    def __init__(self, parent=None, titulo="Nueva Columna", columnas_existentes=None):
        super().__init__(parent)
        self.columnas_existentes = columnas_existentes or []
        self.setWindowTitle(titulo)
        self.setModal(True)
        self.setFixedSize(300, 150)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Etiqueta y campo de texto
        self.etiqueta = QLabel("Nombre de la columna:")
        layout.addWidget(self.etiqueta)
        
        self.campo_nombre = QLineEdit()
        self.campo_nombre.setPlaceholderText("Ingrese el nombre de la columna...")
        self.campo_nombre.textChanged.connect(self.validar_nombre)
        layout.addWidget(self.campo_nombre)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.clicked.connect(self.aceptar)
        self.boton_aceptar.setEnabled(False)  # Inicialmente deshabilitado
        
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.reject)
        
        botones_layout.addWidget(self.boton_aceptar)
        botones_layout.addWidget(self.boton_cancelar)
        
        layout.addLayout(botones_layout)
        
        self.setLayout(layout)
        
        # Establecer foco en el campo de texto
        self.campo_nombre.setFocus()
        
    def validar_nombre(self, texto):
        """Valida el nombre de la columna"""
        texto = texto.strip()
        
        # Verificar que no esté vacío
        if not texto:
            self.boton_aceptar.setEnabled(False)
            return
            
        # Verificar que no exista ya
        if texto in self.columnas_existentes:
            self.boton_aceptar.setEnabled(False)
            return
            
        self.boton_aceptar.setEnabled(True)
        
    def aceptar(self):
        """Maneja la aceptación del diálogo"""
        nombre = self.get_nombre()
        
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre no puede estar vacío")
            return
            
        if nombre in self.columnas_existentes:
            QMessageBox.warning(self, "Error", f"La columna '{nombre}' ya existe")
            return
            
        self.accept()
        
    def get_nombre(self):
        """Retorna el nombre ingresado"""
        return self.campo_nombre.text().strip()
