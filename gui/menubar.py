from PySide6.QtWidgets import QMenu, QMenuBar, QTableView, QFileDialog
from PySide6.QtGui import QAction
import pandas as pd

from gui.tabla import Tabla
from modelos import TablaDatos

class MenuBar(QMenuBar):

    def __init__(self, tabla: QTableView, datos: pd.DataFrame ) -> None:
        super().__init__()
        self.__datos = datos
        self.__tabla = tabla
        self.archivos_menu()

        self.edicion_menu()
        self.estadisticas_menu()
        self.graficos_menu()
        self.ayuda()

    # Menus

    def archivos_menu(self) -> None:
        archivos = self.addMenu("&Archivos")

        # definir actions
        nuevo_archivo = QAction("Nueva tabla",self,shortcut="Ctrl+n")

        abrir_archivo = QAction("Abrir archivo",self,shortcut="Ctrl+o")
        abrir_archivo.triggered.connect(self.abrir_archivo)


        guardar_archivo = QAction("Guardar archivo",self,shortcut="Ctrl+S")
        guardar_archivo_como = QAction("Guardar archivo como",self,shortcut="Ctrl+Shift+S")
        cerrar_tabla = QAction("Cerrar tabla",self,shortcut="Ctrl+w")
        salir = QAction("Salir",self,shortcut="Ctrl+Q")

        # definir sub menus
        abrir_recientes = QMenu("Abrir recientes",self)


        # agregar elementos
        archivos.addAction(nuevo_archivo)
        archivos.addAction(abrir_archivo)
        archivos.addMenu(abrir_recientes)
        archivos.addAction(guardar_archivo)
        archivos.addAction(guardar_archivo_como)
        archivos.addAction(cerrar_tabla)
        archivos.addSeparator()
        archivos.addAction(salir)

    def edicion_menu(self) -> None:
        edicion = self.addMenu("&Edición")

        # definir actions
        cortar = QAction("Cortar",self,shortcut="Ctrl+x")
        copiar = QAction("Copiar", self,shortcut="Ctrl+c")
        pegar = QAction("Pegar",self,shortcut="Ctrl+v")
        borrar = QAction("Borrar",self,shortcut="Ctrl+d")
        seleccionar_todo = QAction("Seleccionar todo",self,shortcut="Ctrl+A")

        # definir menus

        # agregar elementos
        edicion.addAction(cortar)
        edicion.addAction(copiar)
        edicion.addAction(pegar)
        edicion.addAction(borrar)
        _ = edicion.addSeparator()
        edicion.addAction(seleccionar_todo)


    def estadisticas_menu(self) -> None:
        estadisticas = self.addMenu("&Estadísticas")
        
        # Definir actions 
        medidas_resumen = QAction("Medidas resumen",self)
        tablas_frecuencias = QAction("Tablas de frecuencias",self)
        analisis_varianza = QAction("Analisis de varianza",self)
        coeficiente_determinacion = QAction("Coeficiente de determinación",self)
        regresion_lineal = QAction("Regresion lineal",self)
        
        # añadir elementos
        estadisticas.addAction(medidas_resumen)
        estadisticas.addAction(tablas_frecuencias)
        estadisticas.addAction(analisis_varianza)
        estadisticas.addAction(coeficiente_determinacion)
        estadisticas.addSeparator()
        estadisticas.addAction(regresion_lineal)

        
    def graficos_menu(self) -> None:
        graficos = self.addMenu("&graficos")  
   
        # definir actions
        diagrama_dispersion = QAction("Diagrama de dispersion",self)
        grafico_barras = QAction("Gráfico de barras",self)
        grafico_doble_entrada = QAction("Gráfico de doble entrada",self)
        tabla_contingencia = QAction("Tabla de contingencia",self)
        # definir menus

        # añadir elementos
        graficos.addAction(diagrama_dispersion)
        graficos.addAction(grafico_barras)
        graficos.addAction(grafico_doble_entrada)
        graficos.addSeparator()
        graficos.addAction(tabla_contingencia)

    def ayuda(self) -> None:
        ayuda = self.addMenu("&Ayuda")
        
        # definir actions
        guia = QAction("Guia",self,shortcut="Ctrl+g")
        acerca_de = QAction("Acerca de...",self)
        novedades = QAction("Novedades",self)

        # añadir elementos
        ayuda.addAction(guia)
        ayuda.addAction(acerca_de)
        ayuda.addAction(novedades)
    
    # actions

    def abrir_archivo(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption="Open File",
            dir="",  # Initial directory
            filter="Csv Files (*.csv);;All Files (*.*)" # File type filters
        )
        if file_name: 
            self.__datos = TablaDatos(file_name)
            tabla: Tabla =  Tabla(self.__datos.get_dataFrame())
            self.__tabla.setModel(tabla)

    # Actions de Archivos

    # Actions de edicion

    # Actions de estadisticas

    # Actions de gráficos

    # Actions de Ayuda
