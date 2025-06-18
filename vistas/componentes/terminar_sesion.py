from reactpy import component, html
from typing import Callable

from constantes.db import Sesion
from ..componentes.iconos import Iconos


@component
def TerminarSesion(set_sesion: Callable[[Sesion], None]):
    return html.button(
        {
            "className": "btn btn-secundario",
            "on_click": lambda _: set_sesion({"usuario": "", "rol": ""}),
        },
        Iconos.Salir({"className": "size-[1.25em]"}),
        "Terminar sesión",
    )
