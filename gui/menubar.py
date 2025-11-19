from PySide6.QtWidgets import QApplication, QFrame, QGridLayout, QLabel, QMenu, QMenuBar, QFileDialog, QMessageBox, QTableView
from PySide6.QtGui import QAction

import pandas as pd

from archivos import ArchivosRecientes
from gui.dialog_general import DialogGeneral
from gui.dos_var_dialog import DosVarDialog
from gui.un_var_dialog import UnVarDialog
from gui.tabla import Tabla
from modelos import TablaDatos
from modelos import medidas_resumen
from modelos.medidas_resumen import MedidasResumen

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
        medidas_resumen.triggered.connect(self.medidas_resumen)

        tablas_frecuencias = QAction("Tablas de frecuencias",self)
        tablas_frecuencias.triggered.connect(self.tablas_frecuencias)

        analisis_varianza = QAction("Analisis de varianza",self)
        analisis_varianza.triggered.connect(self.analisis_varianza)

        coeficiente_determinacion = QAction("Coeficiente de determinación",self)
        coeficiente_determinacion.triggered.connect(self.coeficiente_determinacion)

        regresion_lineal = QAction("Regresion lineal",self)
        regresion_lineal.triggered.connect(self.regresion_lineal)
        
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
        diagrama_dispersion.triggered.connect(self.diagrama_dispersion)

        grafico_barras = QAction("Gráfico de barras",self)
        grafico_barras.triggered.connect(self.grafico_barras)

        grafico_doble_entrada = QAction("Gráfico de doble entrada",self)
        grafico_doble_entrada.triggered.connect(self.grafico_doble_entrada)

        tabla_contingencia = QAction("Tabla de contingencia",self)
        tabla_contingencia.triggered.connect(self.tabla_contingencia)

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
        self.__datos.set_nuevos_datos()
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
            self.agregar_archivos_recientes(nombre_archivo)
            self.__archivos_recientes.add_archivo(nombre_archivo)
            self.__datos.set_nuevos_datos(nombre_archivo)
            tabla: Tabla =  Tabla(self.__datos)
            self.__tabla.setModel(tabla)

    def guardar_archivo(self) -> None:
        if not self.__datos.get_ubicacion(): 
            self.guardar_archivo_como()
            return
        self.__datos.guardar_archivo()
        self.__tabla.model().set_modificado()
    def guardar_archivo_como(self) -> None:
        if self.__datos.get_num_elems_total() == 0:
            return
        nombre_archivo, _ = QFileDialog.getSaveFileName(self,"Csv Files (*.csv);; Excel Files (*.xls) ;;All Files (*.*)")
        if nombre_archivo:
            self.__archivos_recientes.add_archivo(nombre_archivo)
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

        self.__archivos_recientes.add_archivo(ubicacion)
        self.agregar_archivos_recientes(ubicacion)
        self.__datos.set_nuevos_datos(ubicacion)
        tabla: Tabla =  Tabla(self.__datos)
        self.__tabla.setModel(tabla)
        self.__tabla.model().set_modificado()

    def archivos_recientes(self ) -> None:
     
        for i in self.__archivos_recientes.get_archivos():
            aux: QAction = QAction(i,self)
            aux.triggered.connect(lambda _, ubicacion=i: self.abrir_archivo_reciente(ubicacion))
            self.__abrir_recientes.addAction(aux)
    def agregar_archivos_recientes(self,ubicacion: str) -> None:
        if ubicacion in self.__archivos_recientes.get_archivos():
            return
        acciones = self.__abrir_recientes.actions()
        if len(acciones)+1 > 7:

            ultima_accion = acciones[0]
            self.__abrir_recientes.removeAction(ultima_accion)
        
        aux: QAction = QAction(ubicacion,self)
        aux.triggered.connect(lambda _, ubicacion=ubicacion: self.abrir_archivo_reciente(ubicacion))
        self.__abrir_recientes.addAction(aux)
    # Actions de Archivos

    # Actions de edicion

    # Actions de estadisticas
    def  medidas_resumen(self) -> None:
        dlg = UnVarDialog("Medidas resumen",self.__datos.get_atributos())
        if dlg.exec_():
            lista: list[int | float] = []
            if self.__datos.get_tipo(dlg.get_atributo()) == "literal":
                lista = self.__datos.get_ocurrencias(dlg.get_atributo()).tolist()
            else:
                lista = self.__datos.get_dataFrame()[dlg.get_atributo()].tolist()  
            medidas_resumen_var: MedidasResumen = MedidasResumen(lista)
            frame = QFrame()
            layout = QGridLayout()
            frame.setLayout(layout)
            
            layout.addWidget(QLabel("Nº de elementos:"),0,0)
            layout.addWidget(QLabel(str(medidas_resumen_var.n)),0,1)
            layout.addWidget(QLabel("Promedio: "),1,0)
            layout.addWidget(QLabel(str(medidas_resumen_var.promedio())),1,1)
            layout.addWidget(QLabel("Media:"),2,0)
            layout.addWidget(QLabel(str(medidas_resumen_var.media())),2,1)
            layout.addWidget(QLabel("Moda"),3,0)
            layout.addWidget(QLabel(str(medidas_resumen_var.moda())),3,1)
            layout.addWidget(QLabel("Mínimo"),4,0)
            layout.addWidget(QLabel(str(medidas_resumen_var.minimo())),4,1)
            layout.addWidget(QLabel("Máximo"),5,0)
            layout.addWidget(QLabel(str(medidas_resumen_var.maximo())),5,1)
            layout.addWidget(QLabel("Suma de cuadrados"),6,0) 
            layout.addWidget(QLabel(str(medidas_resumen_var.suma_cuadrados())),6,1) 
            layout.addWidget(QLabel("Varianza Poblacional"),7,0) 
            layout.addWidget(QLabel(str(medidas_resumen_var.varianza())),7,1) 
            layout.addWidget(QLabel("Varianza Muestral"),8,0) 
            layout.addWidget(QLabel(str(medidas_resumen_var.varianza(True))),8,1) 
            layout.addWidget(QLabel("Desv. Estandar Poblacional"),9,0) 
            layout.addWidget(QLabel(str(medidas_resumen_var.desviacion_estandar())),9,1) 
            layout.addWidget(QLabel("Desv. Estandar Muestral"),10,0) 
            layout.addWidget(QLabel(str(medidas_resumen_var.desviacion_estandar(True))),10,1) 


            dlg_general = DialogGeneral("Medidas resumen",frame)
            dlg_general.exec_()
    def tablas_frecuencias(self) -> None:
        dlg = UnVarDialog("Tabla de frecuencias",self.__datos.get_atributos())
        if dlg.exec_():
            pass 

    def analisis_varianza(self) -> None:
        dlg = DosVarDialog("Analisis de varianza",self.__datos.get_atributos())
        if dlg.exec_():
            pass 
       
    def coeficiente_determinacion(self) -> None:
        dlg = DosVarDialog("Coeficiente de determinación",self.__datos.get_atributos())
        if dlg.exec_():
            pass 
 
    def regresion_lineal(self) -> None:
        dlg = DosVarDialog("Regresion",self.__datos.get_atributos())
        if dlg.exec_():
            pass 
    # Actions de gráficos
    def diagrama_dispersion(self) -> None:
        dlg = DosVarDialog("Diagrama de dispersión",self.__datos.get_atributos())
        if dlg.exec_():
            pass 

    def grafico_barras(self) -> None:
        dlg = UnVarDialog("Gráfico de barras",self.__datos.get_atributos())
        if dlg.exec_():
            pass 
 
    def grafico_doble_entrada(self) -> None:
        dlg = DosVarDialog("Gráfico de doble entrada",self.__datos.get_atributos())
        if dlg.exec_():
            pass 

    def tabla_contingencia(self) -> None:
        dlg = DosVarDialog("Regresion",self.__datos.get_atributos())
        if dlg.exec_():
            pass 

    # Actions de Ayuda

    def cerrar_app(self) -> None:
        self.__archivos_recientes.guardar_datos()

