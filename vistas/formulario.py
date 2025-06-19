from datetime import date
from typing import Callable
from reactpy import component, html, event, use_context, use_state

from constantes.db import DatosComunidad, ErrorDeValidacion, NOMBRE_MÍNIMO
from lib.db.subida import añadir_datos_comunidad, verificar_cedula_existente

from .componentes.alerta import Alerta
from .componentes.contenedor import Contenedor, Cabecera
from .componentes.main import Main
from .componentes.formulario.input import Input
from .componentes.iconos import Iconos
from .componentes.terminar_sesion import TerminarSesion
from contexto.sesion import contexto_sesion
from contexto.formulario import contexto_formulario


def DatosIniciales():
    return DatosComunidad(
        {
            "nombres": "",
            "apellidos": "",
            "cedula": 0,
            "fecha_nacimiento": "",
            "patologia": "",
            "numero_casa": 0,
        }
    )


@component
def Formulario():
    datos, set_datos = use_state(DatosIniciales())
    respuesta, set_respuesta = use_state(
        {"estado": "", "error": {"mensaje": "", "motivo": ""}}
    )

    @event(prevent_default=True)
    async def subir(_):
        try:
            await verificacion_cedula(datos["cedula"], set_respuesta)
        except ErrorDeValidacion:
            return

        set_respuesta({"estado": "subiendo", "error": {"mensaje": "", "motivo": ""}})

        try:
            await añadir_datos_comunidad(datos)
            set_respuesta({"estado": "éxito", "error": {"mensaje": "", "motivo": ""}})
            set_datos(DatosIniciales())
        except ErrorDeValidacion as e:
            set_respuesta({"estado": "error", "error": e.args[0]})
        return

    return Main(
        Contenedor(
            Cabecera(
                "Formulario de registro",
                html.div(
                    {"className": "flex flex-col gap-2"},
                    TerminarSesion(),
                ),
            ),
            html.div(
                {"className": "flex flex-col gap-13 mt-13 max-w-[700px]"},
                contexto_formulario(
                    html.form(
                        {
                            "id": "formulario",
                            "on_submit": subir,
                        },
                        Campos(respuesta, set_respuesta),
                    ),
                    Botones(respuesta),
                    value={"datos": datos, "set_datos": set_datos},
                ),
            ),
        )
    )


@component
def Campos(respuesta: dict[str, str], set_respuesta: Callable):
    contexto = use_context(contexto_formulario)
    datos = contexto["datos"]
    set_datos = contexto["set_datos"]

    def change(evento, key: str):
        set_datos(lambda valor: {**valor, key: evento["target"]["value"]})  # type: ignore
        return

    async def cambiar_cedula(evento):
        change(evento, "cedula")
        try:
            await verificar_cedula_existente(evento["target"]["value"])
            set_respuesta({"estado": "error", "error": {"mensaje": "", "motivo": ""}})
        except ErrorDeValidacion as e:
            set_respuesta({"estado": "error", "error": e.args[0]})

    return html.div(
        {
            "className": "grid grid-cols-1 gap-8 *:grid *:grid-cols-3 *:gap-4",
        },
        html.div(
            Input(
                "Nombres",
                props={
                    "type": "text",
                    "minlength": NOMBRE_MÍNIMO,
                    "required": True,
                    "on_change": event(lambda evento: change(evento, "nombres")),
                    "value": datos["nombres"],
                },
                error=respuesta["error"]["mensaje"]  # type: ignore
                if respuesta["error"]["motivo"].startswith("nombres")  # type: ignore
                else None,
            ),
            Input(
                "Apellidos",
                props={
                    "type": "text",
                    "minlength": NOMBRE_MÍNIMO,
                    "required": True,
                    "on_change": event(lambda evento: change(evento, "apellidos")),
                    "value": datos["apellidos"],
                },
                error=respuesta["error"]["mensaje"]  # type: ignore
                if respuesta["error"]["motivo"].startswith("apellidos")  # type: ignore
                else None,
            ),
            Input(
                "Cédula",
                props={
                    "type": "number",
                    "required": True,
                    "on_change": cambiar_cedula,
                    "min": 1,
                    "value": datos["cedula"] or "",
                },
                error=respuesta["error"]["mensaje"]  # type: ignore
                if respuesta["error"]["motivo"].startswith("cedula")  # type: ignore
                else None,
            ),
        ),
        html.div(
            Input(
                "Fecha de nacimiento",
                props={
                    "type": "date",
                    "on_change": event(
                        lambda evento: change(evento, "fecha_nacimiento")
                    ),
                    "value": datos["fecha_nacimiento"],
                    "max": date.today().strftime("%Y-%m-%d"),
                },
            ),
            Input(
                "Patología / condición",
                props={
                    "type": "text",
                    "on_change": event(lambda evento: change(evento, "patologia")),
                    "value": datos["patologia"],
                },
            ),
            Input(
                "Número de casa",
                props={
                    "type": "number",
                    "min": 1,
                    "on_change": event(lambda evento: change(evento, "numero_casa")),
                    "value": datos["numero_casa"] or "",
                },
            ),
        ),
    )


@component
def Botones(respuesta: dict[str, str]):
    set_datos = use_context(contexto_formulario)["set_datos"]

    sesion = use_context(contexto_sesion)["sesion"]
    ADMIN = sesion["rol"] == "admin"

    return html.fieldset(
        {"className": "flex flex-col gap-4 m-auto "},
        Alerta(
            "Guardando...",
            "carga",
            respuesta["estado"] == "subiendo",
        ),
        Alerta(
            "Registro guardado correctamente",
            "éxito",
            respuesta["estado"] == "éxito",
        ),
        html.div(
            {"className": "flex gap-2"},
            html.button(
                {
                    "className": "btn btn-secundario",
                    "disabled": not ADMIN,
                    "on_click": lambda _: set_datos(DatosIniciales()),
                },
                Iconos.Borrar(),
                "Limpiar campos",
            ),
            html.button(
                {
                    "className": "btn btn-primario",
                    "form": "formulario",
                    "disabled": not ADMIN,
                },
                Iconos.Añadir(),
                "Añadir registro",
            ),
        ),
    )


async def verificacion_cedula(cedula: int, set_respuesta: Callable):
    try:
        await verificar_cedula_existente(cedula)
        set_respuesta({"estado": "error", "error": {"mensaje": "", "motivo": ""}})
    except ErrorDeValidacion as e:
        set_respuesta({"estado": "error", "error": e.args[0]})
