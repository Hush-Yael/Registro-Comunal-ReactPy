from datetime import date
from reactpy import component, html, use_context

from constantes.db import DatosComunidad, ErrorDeValidacion, NOMBRE_MÍNIMO
from lib.db.subida import añadir_datos_comunidad, verificar_cedula_existente


from .componentes.formulario.index import (
    ContextoFormulario,
    contexto_formulario,
    Formulario as FormularioComponente,
    MensajeCarga,
    MensajeExito,
    mapa_errores,
)
from .componentes.contenedor import Contenedor, Cabecera
from .componentes.main import Main
from .componentes.formulario.input import Input
from .componentes.iconos import Iconos
from .componentes.terminar_sesion import TerminarSesion
from contexto.sesion import contexto_sesion


def DatosIniciales():
    return DatosComunidad(
        {
            "nombres": "",
            "apellidos": "",
            "cedula": "",
            "fecha_nacimiento": "",
            "patologia": "",
            "numero_casa": "",
        }
    )


@component
def RegistroComunidad():
    async def subir(contexto: ContextoFormulario):
        datos, set_datos, set_estado, set_errores = (
            contexto["datos"],
            contexto["set_datos"],
            contexto["set_estado"],
            contexto["set_errores"],
        )
        try:
            await añadir_datos_comunidad(datos)
            set_estado("éxito")
            set_datos(DatosIniciales())
        except ErrorDeValidacion as e:
            campo, error = e.args[0].values()
            set_estado("error")
            set_errores(lambda _: {**_, campo: error})  # type: ignore

    return Main(
        Contenedor(
            Cabecera(
                "Formulario de registro",
                html.div(
                    {"className": "flex flex-col gap-2"},
                    TerminarSesion(),
                ),
            ),
            FormularioComponente(
                DatosIniciales(),
                {
                    "id": "formulario",
                    "on_submit": subir,
                },
                html.div(
                    {"className": "flex flex-col gap-13 mt-13 max-w-[700px]"},
                    Campos(),
                    Botones(),
                ),
            ),
        )
    )


@component
def Campos():
    set_errores = use_context(contexto_formulario)["set_errores"]

    async def cambiar_cedula(evento):
        try:
            await verificar_cedula_existente(evento["target"]["value"])
        except ErrorDeValidacion as e:
            campo, error = e.args[0].values()
            set_errores(lambda _: {**_, campo: error})

    return html.div(
        {
            "className": "grid grid-cols-1 gap-8 *:grid *:grid-cols-3 *:gap-4",
        },
        html.div(
            Input(
                "Nombres",
                "nombres",
                props={
                    "name": "formulario",
                    "type": "text",
                    "minlength": NOMBRE_MÍNIMO,
                    "required": True,
                },
            ),
            Input(
                "Apellidos",
                "apellidos",
                props={
                    "name": "formulario",
                    "type": "text",
                    "minlength": NOMBRE_MÍNIMO,
                    "required": True,
                },
            ),
            Input(
                "Cédula",
                "cedula",
                props={
                    "name": "formulario",
                    "type": "number",
                    "required": True,
                    "on_change": cambiar_cedula,
                    "min": 1,
                },
            ),
        ),
        html.div(
            Input(
                "Fecha de nacimiento",
                "fecha_nacimiento",
                props={
                    "name": "formulario",
                    "type": "date",
                    "max": date.today().strftime("%Y-%m-%d"),
                },
            ),
            Input(
                "Patología / condición",
                "patologia",
                props={
                    "name": "formulario",
                    "type": "text",
                },
            ),
            Input(
                "Número de casa",
                "numero_casa",
                props={
                    "name": "formulario",
                    "type": "number",
                    "min": 1,
                },
            ),
        ),
    )


@component
def Botones():
    contexto = use_context(contexto_formulario)

    set_estado, set_errores, set_datos = (
        contexto["set_estado"],
        contexto["set_errores"],
        use_context(contexto_formulario)["set_datos"],
    )

    sesion = use_context(contexto_sesion)["sesion"]
    ADMIN = sesion["rol"] == "admin"

    def limpiar_campos(_):
        datos_iniciales = DatosIniciales()
        set_datos(datos_iniciales)
        set_errores(mapa_errores(datos_iniciales))
        set_estado("")

    return html.fieldset(
        {"className": "flex flex-col gap-4 m-auto "},
        MensajeCarga(
            "Guardando...",
        ),
        MensajeExito(
            "Registro guardado correctamente",
        ),
        html.div(
            {"className": "flex gap-2"},
            html.button(
                {
                    "className": "btn btn-secundario",
                    "disabled": not ADMIN,
                    "type": "reset",
                    "on_click": limpiar_campos,
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
