from reactpy import component, html, use_location, use_context
from reactpy.types import VdomChildren
from reactpy_router import link

from contexto.sesion import contexto_sesion

from vistas.componentes.iconos import Iconos


@component
def Nav():
    sesion = use_context(contexto_sesion)["sesion"]

    if not sesion["usuario"]:
        return

    return html.nav(
        {
            "className": "flex items-center gap-3 bg-white p-1.5 px-2 rounded-md border border-neutral-200 shadow-lg"
        },
        A(
            "/",
            Iconos.Campo(),
            "Formulario",
        ),
        A(
            "/usuarios",
            Iconos.Personas({"className": "size-6"}),
            "Usuarios",
        ),
        A(
            "/registros",
            Iconos.Registros(),
            "Registros",
        ),
    )


@component
def A(
    to: str,
    *children: VdomChildren,
):
    pathname = use_location().pathname

    return link(
        {
            "to": to,
            "className": "flex items-center gap-2 aria-[current=page]:font-bold aria-[current=page]:bg-neutral-900 aria-[current=page]:text-white rounded-lg p-1 px-2.5",
            "aria-current": "page" if to == pathname else None,
        },
        *children,
    )
