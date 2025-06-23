from reactpy import component, html
from reactpy.types import VdomChildren, VdomAttributes
from typing import TypedDict


class Thead(TypedDict):
    label: str
    pos: str
    tamaño: int


@component
def Tabla(cabeceras: list[Thead], *children: VdomChildren):
    return html.div(
        # wrapper de la tabla para poder hacer scroll
        {"className": "max-h-[400px] mt-8 overflow-y-auto"},
        html.table(
            {
                "className": "w-full table-auto border-tools-table-outline rounded-md border-neutral-500 text-sm"
            },
            html.thead(
                html.tr(
                    (
                        Cabecera(
                            {
                                "style": {
                                    "width": f"{cabeceras[i].get('tamaño', 10)}ch",
                                    "text-align": cabeceras[i].get("pos", "left"),
                                },
                            },
                            cabeceras[i].get("label", "N/A"),
                        )
                        for i in range(len(cabeceras))
                    ),
                ),
            ),
            html.tbody(*children),
        ),
    )


@component
def Cabecera(
    props: VdomAttributes = {},
    *children: VdomChildren,
):
    return html.th(
        {
            **props,
            "className": f"sticky top-0 p-1.5 px-2 bg-neutral-900 text-white border-b border-neutral-600 first:rounded-tl-md last:rounded-tr-md text-nowrap {props.get('className', '')}",
        },
        *children,
    )


@component
def Fila(*children: VdomChildren, props: VdomAttributes = {}):  # type: ignore
    return html.tr(
        {
            "className": f"odd:bg-neutral-100 border-b border-neutral-200 {props.get('className', '')}",
            **props,
        },
        *children,
    )
