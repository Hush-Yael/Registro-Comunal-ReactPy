from typing import Any, Callable
from reactpy import component, html
from reactpy.types import VdomChildren, VdomAttributes


@component
def Modal(
    *children: VdomChildren,
    props: VdomAttributes = {},
    cerrarse: Callable = lambda: None,
    confirmar: Any,
    cancelar_txt: str = "Cancelar",
    confirmar_txt: str = "Confirmar",
):
    return html.dialog(
        {
            **props,
            "className": "m-auto bg-white shadow-xl rounded-md open:animate-[aparecer_0.2s_ease-in-out] backdrop:bg-[#0002] open:backdrop:animate-[aparecer_0.2s_ease-in-out]",
        },
        html.div(
            {
                "className": "p-4",
            },
            html.div(
                {"className": "flex flex-col gap-6"},
                *children,
                html.div(
                    {"className": "flex justify-end gap-2"},
                    html.button(
                        {
                            "className": "btn btn-secundario",
                            "data-modal-btn": "",
                            "on_click": cerrarse,
                        },
                        cancelar_txt,
                    ),
                    html.button(
                        {
                            "className": "btn btn-primario",
                            "data-modal-btn": "",
                            "on_click": confirmar,
                        },
                        confirmar_txt,
                    ),
                ),
            ),
        ),
    )
