from typing import Callable, TypedDict
from reactpy import create_context
from constantes.db import Sesion


class Contexto(TypedDict):
    sesion: Sesion
    set_sesion: Callable[[Sesion], None]


_default: Contexto = {
    "sesion": {"usuario": "", "rol": ""},
    "set_sesion": lambda _: {"usuario": "", "rol": ""},  # type: ignore
}

contexto_sesion = create_context(_default)
