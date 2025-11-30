from PySide6.QtWidgets import QApplication, QFrame, QGridLayout, QLabel, QLineEdit, QMenu, QMenuBar, QFileDialog, QMessageBox, QPushButton, QTableView
from PySide6.QtGui import QAction, QIntValidator
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from graficos.tablas_contigencia import TablaContigencia
import pandas as pd


from archivos import ArchivosRecientes
from graficos.graficos_barras import GraficoBarra
from graficos.graficos_dispersion import GraficoDispersion
from graficos.graficos_doble_entrada import GraficoDobleEntrada
from gui.dialog_general import DialogGeneral
from gui.dos_var_dialog import DosVarDialog
from gui.table_model import TableModel
from gui.un_var_dialog import UnVarDialog
from gui.tabla import Tabla
from modelos import TablaDatos
from modelos import medidas_resumen
from modelos import tablas_frecuencias
from modelos.anare import Anare
from modelos.medidas_resumen import MedidasResumen
from modelos.regresion_lineal import RegresionLineal
from modelos.tablas_frecuencias import TablaFrecuencia

class MenuBar(QMenuBar):

    def __init__(self, tabla: QTableView, datos: TablaDatos ) -> None:
        super().__init__()
        self.__datos = datos
        self.__tabla = tabla
        self.__archivos_recientes: ArchivosRecientes = ArchivosRecientes()
        self.__abrir_recientes: QMenu = QMenu("Abrir recientes",self)
        self.archivos_menu()

        self.estadisticas_menu()
        self.graficos_menu()


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
    
    
    


    def estadisticas_menu(self) -> None:
        estadisticas = self.addMenu("&Estadísticas")
        
        # Definir actions 
        medidas_resumen = QAction("Medidas resumen",self)
        medidas_resumen.triggered.connect(self.medidas_resumen)

        tablas_frecuencias = QAction("Tablas de frecuencias",self)
        tablas_frecuencias.triggered.connect(self.tablas_frecuencias)

        analisis_varianza = QAction("Analisis de varianza",self)
        analisis_varianza.triggered.connect(self.analisis_varianza)


        regresion_lineal = QAction("Regresion lineal",self)
        regresion_lineal.triggered.connect(self.regresion_lineal)
        
        # añadir elementos
        estadisticas.addAction(medidas_resumen)
        estadisticas.addAction(tablas_frecuencias)
        estadisticas.addAction(analisis_varianza)
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
        ], columns = ['Columna 1', 'Columna 2'], index=['0', '1', '2']))
        
        tabla: Tabla =  Tabla(self.__datos)
        self.__tabla.setModel(tabla)

    def abrir_archivo(self) -> None:
        nombre_archivo, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption="Open File",
            dir="",  # Initial directory
            filter="Csv Files (*.csv);; Excel Files (*.xls,*.xlsx) ;;All Files (*.*)" # File type filters
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
                lista = self.__datos.get_ocurrencias(dlg.get_atributo())[dlg.get_atributo()].to_list()
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
            datos = self.__datos.get_ocurrencias(dlg.get_atributo())
            tabla_frecuencia: TablaFrecuencia = TablaFrecuencia(datos,dlg.get_atributo(),self.__datos.get_tipo(dlg.get_atributo()))
            
            frame = QFrame()
            layout = QGridLayout()
            frame.setLayout(layout)
            model = TableModel(tabla_frecuencia.get_tabla(),tabla_frecuencia.get_headers())
            tabla: QTableView = QTableView()
            tabla.setModel(model)
            layout.addWidget(tabla)
            
            dlg_general = DialogGeneral("Tabla de frecuencias",frame)
            dlg_general.adjustSize()
            dlg_general.exec_()

    def analisis_varianza(self) -> None:
        dlg = DosVarDialog("Análisis de varianza",self.__datos.get_atributos())
        confianza = QLineEdit(self)
        confianza.setPlaceholderText("Ingresa el nivel de confianza")
        validator = QIntValidator(self) 
        confianza.setValidator(validator)
        dlg.addWidgetP(confianza,1,0)
        if dlg.exec_() and (confianza.text() and int(confianza.text()) >0 and int(confianza.text())<100):
            if not dlg.get_atributo_x() or not dlg.get_atributo_y():
                QMessageBox.critical(self, "Falta de variable", "Debe seleccionar dos variables.")
                return     

            x = self.__datos.get_dataFrame()[dlg.get_atributo_x()].to_list()
            y = self.__datos.get_dataFrame()[dlg.get_atributo_y()].to_list()
            regresion: RegresionLineal = RegresionLineal(x,y)

            analisis_varianza:Anare = Anare(regresion.b1(),int(confianza.text()),x,y)

            frame = QFrame()
            layout = QGridLayout()
            frame.setLayout(layout)
            model = TableModel(analisis_varianza.a_matriz(),analisis_varianza.columnas())
            tabla: QTableView = QTableView()
            tabla.setModel(model)
            layout.addWidget(tabla)
            


            dlg_general = DialogGeneral("Análisis de varianza",frame)
            dlg.setFixedSize(700,200)
            dlg_general.exec()
        else:
            QMessageBox.critical(self, "Valores erroneos", "Debe ingresar un nivel de confianza valido.")
       
 
    def regresion_lineal(self) -> None:
        dlg = DosVarDialog("Regresion",self.__datos.get_atributos())
        if dlg.exec_():
            if not dlg.get_atributo_x() or not dlg.get_atributo_y():
                QMessageBox.critical(self, "Falta de variable", "Debe seleccionar dos variables.")
                return     

            frame = QFrame()
            layout = QGridLayout()
            frame.setLayout(layout)
            x = self.__datos.get_dataFrame()[dlg.get_atributo_x()].to_list()
            y = self.__datos.get_dataFrame()[dlg.get_atributo_y()].to_list()
             
            regresion: RegresionLineal = RegresionLineal(x,y)

            layout.addWidget(QLabel("varianza x: "),0,0)
            layout.addWidget(QLabel(str(regresion.varianza_x())),0,1)
            layout.addWidget(QLabel("varianza y: "),1,0)
            layout.addWidget(QLabel(str(regresion.varianza_y())),1,1)
            layout.addWidget(QLabel("Covarianza:"),2,0)
            layout.addWidget(QLabel(str(regresion.cov_xy())),2,1)
            layout.addWidget(QLabel("r:"),3,0)
            layout.addWidget(QLabel(str(regresion.r())),3,1)
            layout.addWidget(QLabel("R²:"),4,0)
            layout.addWidget(QLabel(str(regresion.coeficiente_determinacion())),4,1)
            layout.addWidget(QLabel("Evaluación de R²:"),5,0)
            layout.addWidget(QLabel(str(regresion.evaluacion_R())),5,1)
            layout.addWidget(QLabel("Función:"),6,0)
            aux = "y = "+ str(regresion.b0()) + " + " + str(regresion.b1()) + "x"
            layout.addWidget(QLabel(aux),6,1) 
            # TODO: agregar calculadora de y estimado 
            dlg_general = DialogGeneral("Regresión",frame)
            dlg_general.exec_()
 
    # Actions de gráficos

    def guardar_grafico(self):
        nombre_archivo, _ = QFileDialog.getSaveFileName(self,"Csv Files (*.csv);; Excel Files (*.xls,*.xlsx) ;;All Files (*.*)")
        if nombre_archivo:
            return nombre_archivo
        return ""

    def diagrama_dispersion(self) -> None:
        dlg = DosVarDialog("Diagrama de dispersión",self.__datos.get_atributos("bool","literal"))
        if dlg.exec_():
            if not dlg.get_atributo_x() or not dlg.get_atributo_y():
                QMessageBox.critical(self, "Falta de variable", "Debe seleccionar dos variables.")
                return     
            atributo_x = self.__datos.get_valores(dlg.get_atributo_x()).to_list()
            atributo_y = self.__datos.get_valores(dlg.get_atributo_y()).to_list()
            graficos_doble = GraficoDispersion(atributo_x,atributo_y,dlg.get_atributo_x(),dlg.get_atributo_y())
            frame = QFrame()
            layout = QGridLayout()
            frame.setLayout(layout)

            canvas = FigureCanvas(graficos_doble.get_grafico())
            boton_guardar = QPushButton("Guardar gráfica")
            boton_guardar.setFixedSize(120,35)
            boton_guardar.clicked.connect(lambda: graficos_doble.guardar_grafico(self.guardar_grafico()))
            layout.addWidget(canvas)
            layout.addWidget(boton_guardar)

            canvas.draw()
            dlg_general = DialogGeneral("Diagrama de dispersión",frame)
            dlg_general.adjustSize()
            dlg_general.exec_()

    def grafico_barras(self) -> None:
        dlg = UnVarDialog("Gráfico de barras",self.__datos.get_atributos("bool"))
        if dlg.exec_():
            
            graficos_barras = GraficoBarra(self.__datos.get_ocurrencias(dlg.get_atributo()),dlg.get_atributo())
            frame = QFrame()
            layout = QGridLayout()
            frame.setLayout(layout)

            canvas = FigureCanvas(graficos_barras.get_grafico())
            boton_guardar = QPushButton("Guardar gráfica")
            boton_guardar.setFixedSize(120,35)
            boton_guardar.clicked.connect(lambda: graficos_barras.guardar_grafico(self.guardar_grafico()))
            layout.addWidget(canvas)
            layout.addWidget(boton_guardar)
            canvas.draw()

            dlg_general = DialogGeneral("Gráfico de barras",frame)
            dlg_general.adjustSize()
            dlg_general.exec_()
 
 
    def grafico_doble_entrada(self) -> None:
        dlg = DosVarDialog("Gráfico de doble entrada",self.__datos.get_atributos(),*self.__datos.get_atributos("bool","literal"))
        if dlg.exec_():
            if not dlg.get_atributo_x() or not dlg.get_atributo_y():
                QMessageBox.critical(self, "Falta de variable", "Debe seleccionar dos variables.")
                return     

            atributo_x = self.__datos.get_valores(dlg.get_atributo_x())
            atributo_y = self.__datos.get_valores(dlg.get_atributo_y())
            frame = QFrame()
            layout = QGridLayout()
            frame.setLayout(layout)
            
            graficos_doble = GraficoDobleEntrada(atributo_x,atributo_y,dlg.get_atributo_x(),dlg.get_atributo_y(),self.__datos)
            canvas = FigureCanvas(graficos_doble.get_grafico())
               
           
            boton_guardar = QPushButton("Guardar gráfica")
            boton_guardar.setFixedSize(120,35)
            boton_guardar.clicked.connect(lambda: graficos_doble.guardar_grafico(self.guardar_grafico()))
            layout.addWidget(canvas)
            layout.addWidget(boton_guardar)

            canvas.draw()
            dlg_general = DialogGeneral("Gráfico de doble entrada",frame)
            dlg_general.exec_()


    def tabla_contingencia(self) -> None:
        dlg = DosVarDialog("Regresion",self.__datos.get_atributos())
        if dlg.exec_():
            if not dlg.get_atributo_x() or not dlg.get_atributo_y():
                QMessageBox.critical(self, "Falta de variable", "Debe seleccionar dos variables.")
                return     
            

            atributo_x = self.__datos.get_valores(dlg.get_atributo_x()).to_list()

            atributo_y = self.__datos.get_valores(dlg.get_atributo_y()).to_list()
            tabla_contigencia: TablaContigencia = TablaContigencia(atributo_x,atributo_y,dlg.get_atributo_x(),dlg.get_atributo_y(),self.__datos)
            
            frame = QFrame()
            layout = QGridLayout()
            frame.setLayout(layout)
            table_view = QTableView()
            modelo = Tabla(tabla_contigencia.get_dataFrame())
            table_view.setModel(modelo)
            boton_guardar = QPushButton("Guardar gráfica")
            boton_guardar.setFixedSize(120,35)
            boton_guardar.clicked.connect(lambda: tabla_contigencia.guardar_grafico(self.guardar_grafico()))

            layout.addWidget(table_view)
            layout.addWidget(boton_guardar)
            dlg_general = DialogGeneral("Tabla de contigencia",frame)
            dlg_general.exec_()
 

    # Actions de Ayuda

    def cerrar_app(self) -> None:
        self.__archivos_recientes.guardar_datos()

