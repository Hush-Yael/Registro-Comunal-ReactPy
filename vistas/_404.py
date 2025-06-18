from reactpy import component, html
from reactpy_router import link
from .componentes.main import Main
from .componentes.iconos import Iconos
from vistas.componentes.contenedor import Cabecera, Contenedor


@component
def NoEncontrado():
    return Main(
        Contenedor(
            Cabecera("Página no encontrada"),
            html.div(
                {"className": "flex flex-col gap-5 mt-13"},
                html.div(
                    {"class_name": "flex flex-col items-center gap-2"},
                    Iconos.N404({"className": "size-[3em]"}),
                    html.h1("No se encontró la página que buscas"),
                ),
                link(
                    {
                        "to": "/",
                        "class_name": "btn btn-primario",
                    },
                    Iconos.Casa(),
                    "Ir al inicio",
                ),
            ),
        )
    )
