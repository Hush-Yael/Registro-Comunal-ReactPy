from reactpy import component, event, html, use_state
from reactpy.types import VdomDict

from vistas.componentes.iconos import Iconos
from .input import Contenedor, Titulo, Descripcion, MensajeError, _input


@component
def Contraseña(
    desc: str | None = None,
    props: VdomDict = {},  # type: ignore
    error: str | None = None,
):
    visible, set_visible = use_state(False)

    id = props.get("id")

    return Contenedor(
        html.div(
            {"className": "relative"},
            html.label(
                {"for": id},
                Titulo("Contraseña"),
                _input(
                    {
                        **props,
                        "type": "password" if not visible else "text",
                    },
                    id,
                    desc,
                    error,
                ),
            ),
            html.button(
                {
                    "className": "absolute right-1 top-[3px]",
                    "type": "button",
                    "aria-label": f"{'ocultar' if visible else 'mostrar'} contraseña",
                    "onClick": event(lambda _: set_visible(not visible)),
                },
                Iconos.Ocultar({"className": "size-[1.125em]"})
                if visible
                else Iconos.Ver({"className": "size-[1.125em]"}),
            ),
        ),
        Descripcion(desc, id),
        MensajeError(error, id),
    )
