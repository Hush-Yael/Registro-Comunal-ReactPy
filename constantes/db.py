from typing import TypedDict

NOMBRE_MÍNIMO = 3
CONTRASEÑA_MÍNIMA = 6


class DatosUsuario(TypedDict):
    nombre: str
    contraseña: str


class DatosComunidad(TypedDict):
    nombres: str
    apellidos: str
    cedula: int | str
    fecha_nacimiento: str
    patologia: str
    numero_casa: int | str


# para mostrar errores en los campos
class ErrorDeValidacion(Exception):
    campo: str  # el identificador del campo ("id"), para mostrar el mensaje debajo
    mensaje: str


class Sesion(TypedDict):
    usuario: str
    rol: str
