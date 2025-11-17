from PySide6.QtWidgets import QApplication, QMenu, QMenuBar, QFileDialog, QMessageBox, QTableView
from PySide6.QtGui import QAction

import pandas as pd

from archivos import ArchivosRecientes
from gui.tabla import Tabla
from modelos import TablaDatos

class MenuBar(QMenuBar):

    def __init__(self, tabla: QTableView, datos: TablaDatos ) -> None:
        super().__init__()
        self.__datos = datos
        self.__tabla = tabla
        self.__archivos_recientes: ArchivosRecientes = ArchivosRecientes()
        self.__abrir_recientes: QMenu = QMenu("Abrir recientes",self)
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
        nuevo_archivo.triggered.connect(self.nueva_tabla)

        abrir_archivo = QAction("Abrir archivo",self,shortcut="Ctrl+o")
        abrir_archivo.triggered.connect(self.abrir_archivo)


        guardar_archivo = QAction("Guardar archivo",self,shortcut="Ctrl+S")
        guardar_archivo.triggered.connect(self.guardar_archivo)

        guardar_archivo_como = QAction("Guardar archivo como",self,shortcut="Ctrl+Shift+s")
        guardar_archivo_como.triggered.connect(self.guardar_archivo_como)

        cerrar_tabla = QAction("Cerrar tabla",self,shortcut="Ctrl+w")
        cerrar_tabla.triggered.connect(self.cerrar_tabla)

        salir = QAction("Salir",self,shortcut="Ctrl+Q")
        salir.triggered.connect(QApplication.quit)
        # definir sub menus
        self.archivos_recientes()
                
        # agregar elementos
        archivos.addAction(nuevo_archivo)
        archivos.addAction(abrir_archivo)
        archivos.addMenu(self.__abrir_recientes)
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
    
    def nueva_tabla(self) -> None:
        self.__datos.set_dataFrame(pd.DataFrame([
          ["", ""],
          ["", ""],
          ["", ""],
        ], columns = ['Columna 1', 'Columna 2'], index=['1', '2', '3']))
        
        tabla: Tabla =  Tabla(self.__datos)
        self.__tabla.setModel(tabla)

    def abrir_archivo(self) -> None:
        nombre_archivo, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption="Open File",
            dir="",  # Initial directory
            filter="Csv Files (*.csv);; Excel Files (*.xls) ;;All Files (*.*)" # File type filters
        )
        if nombre_archivo: 
            if self.__archivos_recientes.add_archivo(nombre_archivo):
                self.agregar_archivos_recientes(nombre_archivo)
            self.__datos = TablaDatos(nombre_archivo)
            tabla: Tabla =  Tabla(self.__datos)
            self.__tabla.setModel(tabla)

    def guardar_archivo(self) -> None:
        self.__datos.guardar_archivo()
        self.__tabla.model().set_modificado()
    def guardar_archivo_como(self) -> None:
        if self.__datos.get_num_elems_total() == 0:
            return
        nombre_archivo, _ = QFileDialog.getSaveFileName(self,"Csv Files (*.csv);; Excel Files (*.xls) ;;All Files (*.*)")
        if nombre_archivo:
            if self.__archivos_recientes.add_archivo(nombre_archivo):
                self.agregar_archivos_recientes(nombre_archivo)
            self.__datos.guardar_archivo(nombre_archivo) 
            self.__tabla.model().set_modificado()
    def cerrar_tabla(self) -> None:
        if self.__tabla.model().get_modificado():
            confirmacion = QMessageBox.question(self, "Confirmation", "Deseas guardar los cambios antes de cerrar?", QMessageBox.Yes | QMessageBox.No)

            if confirmacion == QMessageBox.Yes:
                if self.__datos.get_ubicacion() == "":
                    self.guardar_archivo_como()
                else:
                    self.guardar_archivo()
        self.__datos.set_dataFrame(pd.DataFrame()) 
        tabla: Tabla =  Tabla(self.__datos)
        self.__tabla.setModel(tabla)
        self.__tabla.model().set_modificado() 
    def abrir_archivo_reciente(self, ubicacion: str) -> None:
        if self.__tabla.model().get_modificado():
            confirmacion = QMessageBox.question(self, "Confirmation", "Deseas guardar los cambios antes de cerrar?", QMessageBox.Yes | QMessageBox.No)

            if confirmacion == QMessageBox.Yes:
                if self.__datos.get_ubicacion() == "":
                    self.guardar_archivo_como()
                else:
                    self.guardar_archivo()

        if self.__archivos_recientes.add_archivo(ubicacion):
                self.agregar_archivos_recientes(ubicacion)
        self.__datos = TablaDatos(ubicacion)
        tabla: Tabla =  Tabla(self.__datos)
        self.__tabla.setModel(tabla)
        self.__tabla.model().set_modificado()

    def archivos_recientes(self ) -> None:
     
        for i in self.__archivos_recientes.get_archivos():
            aux: QAction = QAction(i,self)
            aux.triggered.connect(lambda _, ubicacion=i: self.abrir_archivo_reciente(ubicacion))
            self.__abrir_recientes.addAction(aux)
    def agregar_archivos_recientes(self,ubicacion: str) -> None:
        aux: QAction = QAction(ubicacion,self)
        aux.triggered.connect(lambda _, ubicacion=ubicacion: self.abrir_archivo_reciente(ubicacion))
        self.__abrir_recientes.addAction(aux)

    # Actions de Archivos

    # Actions de edicion

    # Actions de estadisticas

    # Actions de gráficos

    # Actions de Ayuda

    def cerrar_app(self) -> None:
        self.__archivos_recientes.guardar_datos()

