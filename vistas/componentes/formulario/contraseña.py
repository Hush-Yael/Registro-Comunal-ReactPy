from reactpy import component, event, html, use_context, use_state
from reactpy.types import VdomDict

from vistas.componentes.iconos import Iconos
from .input import Contenedor, Titulo, Descripcion, MensajeError, _input

from .index import contexto_formulario


@component
def Contraseña(
    props: VdomDict = {},  # type: ignore
    desc: str | None = None,
):
    errores = use_context(contexto_formulario)["errores"]
    error = errores["contraseña"]

    visible, set_visible = use_state(False)

    id = props.get("id") or "contraseña"

    return Contenedor(
        html.div(
            {"className": "relative"},
            html.label(
                {"for": id},
                Titulo("Contraseña"),
                _input(
                    "contraseña",
                    id,
                    desc,
                    error,
                    {
                        **props,
                        "type": "password" if not visible else "text",
                    },
                ),
            ),
            html.button(
                {
                    "className": "absolute right-1 top-[2px]",
                    "type": "button",
                    "aria-label": f"{'ocultar' if visible else 'mostrar'} contraseña",
                    "onClick": event(lambda _: set_visible(not visible)),
                },
                Iconos.Ocultar({"className": "size-[1em]"})
                if visible
                else Iconos.Ver({"className": "size-[1.125em]"}),
            ),
        ),
        Descripcion(desc, id),
        MensajeError(error, id),
    )
