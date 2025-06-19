from typing import Callable, TypedDict
from reactpy import create_context

from constantes.db import DatosComunidad


class Contexto(TypedDict):
    datos: DatosComunidad
    set_datos: Callable[[DatosComunidad], None]


_default: Contexto = {
    "datos": {
        "nombres": "",
        "apellidos": "",
        "cedula": 0,
        "fecha_nacimiento": "",
        "patologia": "",
        "numero_casa": 0,
    },
    "set_datos": lambda _: None,
}

contexto_formulario = create_context(_default)
