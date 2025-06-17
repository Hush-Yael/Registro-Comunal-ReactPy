from typing import TypedDict

NOMBRE_MÍNIMO = 3
CONTRASEÑA_MÍNIMA = 6


class DatosUsuario(TypedDict):
    nombre: str
    contraseña: str


class ErrorDeValidacion(Exception):
    motivo: str
    mensaje: str
