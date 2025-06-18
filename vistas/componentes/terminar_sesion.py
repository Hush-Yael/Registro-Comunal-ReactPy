from reactpy import component, html, use_context
from contexto.sesion import contexto_sesion

from ..componentes.iconos import Iconos


@component
def TerminarSesion():
    set_sesion = use_context(contexto_sesion)["set_sesion"]

    return html.button(
        {
            "className": "btn btn-secundario",
            "on_click": lambda _: set_sesion({"usuario": "", "rol": ""}),
        },
        Iconos.Salir({"className": "size-[1.25em]"}),
        "Terminar sesión",
    )
