from matplotlib.figure import Figure
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

from modelos.tabla_de_datos import TablaDatos

class GraficoDobleEntrada:
    def __init__(self, atributo_x,atributo_y, titulo_x,titulo_y,tabla_datos: TablaDatos) -> None:
        self.titulo_x = titulo_x
        self.titulo_y = titulo_y
        self.tabla_datos = tabla_datos
        self.atributo_x = atributo_x
        self.atributo_y = atributo_y
        self.__fig = Figure(figsize=(5, 5), dpi=100)
        self.__axes = self.__fig.add_subplot(111)

        if tabla_datos.get_tipo(titulo_y) == 'literal':
            atributo_x_ = tabla_datos.get_valores(titulo_x).to_list()
            atributo_y_ = tabla_datos.get_valores(titulo_y).to_list()
            self.tabla = pd.crosstab(atributo_x_,atributo_y_)

            self.tabla.plot.bar(ax=self.__axes)

            return
        lista_literales = self.tabla_datos.get_ocurrencias(self.titulo_x)[self.titulo_x].index.to_list() 

        aux_grupos = self.tabla_datos.get_ocurrencias(self.titulo_y)[self.titulo_y].index.to_list() 
        menor_valor = int(aux_grupos[0].split("-")[0]) if self.tabla_datos.get_tipo(self.titulo_y) == "discreto" else float(aux_grupos[0].split("-")[0]) 
        mayor_valor = int(aux_grupos[0].split("-")[1]) if self.tabla_datos.get_tipo(self.titulo_y) == "discreto" else float(aux_grupos[0].split("-")[1])
        c = mayor_valor-menor_valor
        diccionario_tipos = {}
        for i in range(len(aux_grupos)):
            diccionario_tipos[aux_grupos[i]] = [0 for i in range(len(lista_literales))]
        for x, y in zip(self.atributo_x, self.atributo_y):
            for i in range(len(aux_grupos)): 

                if (menor_valor+(i*c) <= y and ( y <  menor_valor+((i+1)*c) or (i==len(aux_grupos)-1 and y <=  menor_valor+((i+1)*c)) )  ):
                    diccionario_tipos[aux_grupos[i]][lista_literales.index(x)] += 1
        
        
        x = np.arange(len(lista_literales))

        


        width = 0.15 # the width of the bars
        multiplier = 0

        self.__fig, ax = plt.subplots(figsize=(max(8, len(aux_grupos) * 2 * len(lista_literales) ),6),layout='constrained')
        i = 0
        for attribute, measurement in diccionario_tipos.items():
            lista_filtrada = list(filter(lambda x: x != 0, measurement))
            measurement_arr = np.array(measurement)
            mascara = measurement_arr != 0
    
            # Filtrar measurement y x
            measurement_filtrado = measurement_arr[mascara]
            x_filtrado = x[mascara]  # Esto debería funcionar ahora
            offset = width * multiplier
            rects = ax.bar( x_filtrado+ offset, lista_filtrada, width, label=attribute)
            ax.bar_label(rects, padding=len(aux_grupos)+1)
            multiplier += 1
            i += 1
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel("fi")
        ax.set_xticks(x + width, lista_literales)
        ax.legend(loc='upper left', ncols=len(aux_grupos)+1)



    def get_grafico(self):
        return self.__fig

    def guardar_grafico(self,nombre_archivo: str):
        if nombre_archivo:
            self.__fig.savefig(nombre_archivo)
