import os
from pathlib import Path


class ArchivosRecientes:
    def __init__(self) -> None:
        ubicacion = os.getcwd() + "/datos/archivos_recientes.txt"
        archivo = Path(ubicacion)
        if not archivo.exists():
            archivo.parent.mkdir(parents=True, exist_ok=True)
            archivo.touch()
        archivo = open(ubicacion,"r")
        self.__ubicacion: str = ubicacion
        self.__archivos: list[str] = []
        for i in archivo.readlines():
            if i.strip():
                self.__archivos.append(i.rstrip("\n"))
        archivo.close()
    def add_archivo(self, ubicacion: str) -> bool:
        if ubicacion in self.__archivos:
            return False
        if ubicacion == "":
            return False
        if len(self.__archivos) <= 7:
            self.__archivos.append(ubicacion)
            return True
        else:
            self.__archivos.insert(0,ubicacion)
            _ = self.__archivos.pop()
            return True

    def guardar_datos(self) -> None:
        with open(self.__ubicacion, "w+", encoding='utf-8') as archivo:
            archivo.write("\n".join(self.__archivos))

    
    def get_archivos(self) -> list[str]:
        return self.__archivos
