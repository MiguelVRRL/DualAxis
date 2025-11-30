import pandas as pd
import matplotlib.pyplot as plt
from modelos.tabla_de_datos import TablaDatos

class TablaContigencia:
    def __init__(self, atributo_x,atributo_y, titulo_x,titulo_y,tabla_datos: TablaDatos) -> None:
        self.titulo_x = titulo_x
        self.titulo_y = titulo_y
        self.tabla_datos = tabla_datos
        self.atributo_x = atributo_x
        self.atributo_y = atributo_y

        self.tabla = pd.crosstab(atributo_x,atributo_y)
    def get_dataFrame(self):
        return self.tabla

    def guardar_grafico(self,nombre_archivo: str):
        if nombre_archivo:
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.axis('tight')
            ax.axis('off')
    
            # Crear tabla
            table = ax.table(cellText=self.tabla.values,
                    colLabels=self.tabla.columns,
                    cellLoc='center',
                    loc='center')
    
            # Formatear tabla
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.5)
    
            plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight', pad_inches=0.05)
            plt.close()

