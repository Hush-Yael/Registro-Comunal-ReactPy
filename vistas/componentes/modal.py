from typing import Any, Callable
from reactpy import component, html, event
from reactpy.types import VdomChildren


@component
def Modal(
    *children: VdomChildren,
    abierto: bool,
    set_abierto: Callable[[bool], None] | None = None,
    cerrarse: Callable = lambda: None,
    confirmar: Any,
    confirmar_txt: str = "Confirmar",
):
    @event
    def cerrar(evento):
        if evento["target"]["tagName"] == "DIALOG":
            if set_abierto is not None:
                set_abierto(False)
            cerrarse()

    @event
    async def confirmacion(_):
        await confirmar(_)
        if set_abierto is not None:
            set_abierto(False)

    return html.dialog(
        {
            "open": abierto,
            "className": "not-open:hidden fixed z-10 inset-0 flex items-center justify-center size-full bg-[#0002] open:animate-[aparecer_0.2s_ease-in-out]",
            "on_click": cerrar,
        },
        html.div(
            {"className": "m-auto p-4 rounded-md  bg-white shadow-xl"},
            html.div(
                {"className": "flex flex-col gap-6"},
                *children,
                html.div(
                    {"className": "flex justify-end gap-2"},
                    html.button(
                        {
                            "className": "btn btn-primario",
                            "on_click": confirmacion,
                        },
                        confirmar_txt,
                    ),
                ),
            ),
        ),
    )
