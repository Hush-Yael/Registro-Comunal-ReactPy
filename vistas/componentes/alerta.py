from reactpy import component, html

from .carga import Carga
from .iconos import Iconos

FONDOS = {"éxito": "bg-emerald-100", "carga": "bg-neutral-100"}

BORDES = {"éxito": "bg-emerald-500", "carga": "bg-neutral-500"}

TEXTOS = {"éxito": "text-emerald-600"}

ICONOS = {
    "éxito": lambda: Iconos.Check({"className": "size-6 text-emerald-600"}),
    "carga": lambda: Carga({"className": "size-5 mx-1"}),
}


@component
def Alerta(texto: str, variante: str, visible: bool = False):
    if visible:
        return html.p(
            {
                "className": f"flex items-center gap-2.5 p-1.5 rounded text-center animate-[aparecer_0.2s_ease-in-out] {FONDOS[variante]}",
                "role": "alert",
            },
            html.span(
                {
                    "className": f"rounded-full h-full min-h-[30px] w-1 {BORDES[variante]}"
                }
            ),
            html.span(
                {"className": "flex items-center gap-2 font-medium"},
                ICONOS[variante](),
                texto,
            ),
        )
