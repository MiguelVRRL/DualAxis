import pandas as pd

class TablaDatos:
    def __init__(self, ubicacion: str = "") -> None:
        self.set_nuevos_datos(ubicacion)
    def set_dataFrame(self, dataFrame: pd.DataFrame) -> None:
        self.__data_frame = dataFrame
    def set_nuevos_datos(self, ubicacion: str = "") -> None:
        if ubicacion == "":
            self.__ubicacion = ""
            self.__ext = ""
            self.__data_frame = pd.DataFrame()
            return
        self.__ubicacion: str = ubicacion
        aux: list[str] = ubicacion.split(".")
        self.__ext: str = aux[len(aux)-1]
        match aux[len(aux)-1]:
            case "csv":
                self.__data_frame: pd.DataFrame = pd.read_csv(ubicacion)
            case "xlsx" | "xlsm" | "xls" | "xlsb":
                self.__data_frame: pd.DataFrame = pd.read_excel(ubicacion)
            case "txt":
                self.__data_frame: pd.DataFrame = pd.read_csv(ubicacion,delimiter="\t")
            case _:
                return
    def get_tipo(self,columna: str) -> str:
        if type(self.__data_frame[columna].iloc[0]) == str:
            return "literal"
        return "numerico"
    def get_atributos(self):
        return self.__data_frame.columns.to_list()
    def get_num_atributos(self) -> int:
        return self.__data_frame.shape[1]
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
    def get_ubicacion(self) -> str:
        return self.__ubicacion
    def guardar_archivo(self,ubicacion: str = "") -> None:
        if ubicacion != "":
            self.__ubicacion = ubicacion
            aux: list[str] = ubicacion.split(".")
            self.__ext: str = aux[len(aux)-1]
        if self.__ubicacion == "":
            return
        match self.__ext:
            case "csv":
                self.__data_frame.to_csv(self.__ubicacion,index=False)
            case "xlsx" | "xlsm" | "xls" | "xlsb":
                self.__data_frame.to_excel(self.__ubicacion,index=False,engine='xlrd')
            case "txt":
                self.__data_frame.to_csv(self.__ubicacion,sep="\t",index=False)
            case _:
                return
    
