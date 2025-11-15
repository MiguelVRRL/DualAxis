import pandas as pd

class TablaDatos:
    def __init__(self, ubicacion: str) -> None:
        aux: list[str] = ubicacion.split(".") 
        match aux[len(aux)-1]:
            case "csv":
                self.__data_frame: pd.DataFrame = pd.read_csv(ubicacion)
            case "xlsx" | "xlsm" | "xls" | "xlsb":
                self.__data_frame: pd.DataFrame = pd.read_excel(ubicacion)
            case "txt":
                self.__data_frame: pd.DataFrame = pd.read_csv(ubicacion,delimiter="\t")
            case _:
                return
            
    def get_atributos(self):
        return self.__data_frame.columns
    
    def get_num_elems_total(self) -> int:
        return self.__data_frame.size
    def get_ocurrencias(self, columna: str):
        return self.__data_frame[columna].value_counts()
    def get_valores(self, columna: str):
        return self.__data_frame[columna]

    def get_num_elems_grupo(self, columna_x: str, columna_y: str) -> int:
        return self.__data_frame.groupby([columna_x,columna_y])[columna_x].count().loc[columna_x]
    def get_num_elems(self, columna: str) -> int:
        return self.__data_frame[columna].size

    def get_dataFrame(self):
        return self.__data_frame
