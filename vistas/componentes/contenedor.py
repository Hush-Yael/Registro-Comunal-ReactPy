from reactpy import component, html
from reactpy.types import VdomChildren


@component
def Contenedor(*children: VdomChildren):
    return html.section(
        {
            "className": "flex flex-col m-auto py-5 px-6 rounded-xl border border-neutral-200 bg-white shadow-lg"
        },
        children,
    )


@component
def Cabecera(title: str, *children: VdomChildren):
    return html.header(
        {"className": "flex justify-between items-center gap-15 w-full"},
        html.div(
            {"className": "flex flex-col gap-2"},
            html.h1({"className": " font-bold text-xl"}, title),
            html.h2(
                {"className": " text-neutral-500"}, "Comunidad Santo Domingo de Guzmán"
            ),
        ),
        *children,
    )
