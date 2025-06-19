from typing import TypedDict

NOMBRE_MÍNIMO = 3
CONTRASEÑA_MÍNIMA = 6


class DatosUsuario(TypedDict):
    nombre: str
    contraseña: str


class DatosComunidad(TypedDict):
    nombres: str
    apellidos: str
    cedula: int
    fecha_nacimiento: str
    patologia: str
    numero_casa: int


class ErrorDeValidacion(Exception):
    motivo: str
    mensaje: str


class Sesion(TypedDict):
    usuario: str
    rol: str
