from reactpy import component, html
from reactpy.types import VdomChildren

from vistas.componentes.navegacion import Nav


@component
def Main(*children: VdomChildren):
    return html.div(
        {"class": "flex flex-col justify-center items-center h-full"},
        Nav(),
        html.main({"class": "flex flex-col p-4"}, children),
    )
