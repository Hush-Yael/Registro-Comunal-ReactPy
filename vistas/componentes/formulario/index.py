from reactpy import (
    component,
    html,
    event,
    use_context,
    create_context,
    use_state,
    use_effect,
)
from reactpy.types import VdomChildren, VdomAttributes
from typing import Any, Callable, TypedDict

from vistas.componentes.alerta import Alerta


class ContextoFormulario(TypedDict):
    datos: dict[str, Any]
    set_datos: Callable[[dict[str, Any]], None]
    errores: dict[str, str]
    set_errores: Callable[[dict[str, str]], None]
    estado: str
    set_estado: Callable[[str], None]


_valor_default_contexto = ContextoFormulario(
    {
        "datos": {},
        "set_datos": lambda _: None,
        "errores": {},
        "set_errores": lambda _: None,
        "estado": "",
        "set_estado": lambda _: None,
    }
)

contexto_formulario = create_context(_valor_default_contexto)


@component
def Formulario(
    datos_iniciales: dict[str, Any],
    props: VdomAttributes = {},
    *children: VdomChildren,
):
    datos, set_datos = use_state(datos_iniciales)
    errores, set_errores = use_state(mapa_errores(datos_iniciales))
    estado, set_estado = use_state("")

    contexto: ContextoFormulario = {
        "datos": datos,
        "set_datos": set_datos,
        "errores": errores,
        "set_errores": set_errores,
        "estado": estado,
        "set_estado": set_estado,
    }

    @event(prevent_default=True)
    async def subir(_):
        set_estado("subiendo")
        if "on_submit" in props:
            await props["on_submit"](contexto)

    return html.form(
        {**props, "on_submit": subir},
        contexto_formulario(*children, value=contexto),
    )


@component
def MensajeExito(texto: str):
    estado = use_context(contexto_formulario)["estado"]

    return Alerta(
        texto,
        "éxito",
        estado == "éxito",
    )


@component
def MensajeCarga(texto: str):
    estado = use_context(contexto_formulario)["estado"]

    return Alerta(
        texto,
        "carga",
        estado == "subiendo",
    )


def mapa_errores[T](datos_iniciales: dict[str, T]):
    return dict([[key, ""] for key in datos_iniciales.keys()])
