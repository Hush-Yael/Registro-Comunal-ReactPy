from reactpy import component, html, use_context
from reactpy_router import link

from lib.db.subida import registrar_usuario
from constantes.db import (
    NOMBRE_MÍNIMO,
    CONTRASEÑA_MÍNIMA,
    DatosUsuario,
    ErrorDeValidacion,
)
from vistas.componentes.formulario.index import (
    Formulario,
    contexto_formulario,
    ContextoFormulario,
    MensajeCarga,
    MensajeExito,
)

from .componentes.main import Main
from .componentes.formulario.input import Input
from .componentes.formulario.contraseña import Contraseña
from .componentes.contenedor import Cabecera, Contenedor


@component
def Registro():
    async def subir(contexto: ContextoFormulario):
        datos, set_datos, set_estado, set_errores = (
            contexto["datos"],
            contexto["set_datos"],
            contexto["set_estado"],
            contexto["set_errores"],
        )

        try:
            await registrar_usuario(datos)
            set_estado("éxito")
            set_datos({"nombre": "", "contraseña": ""})
        except ErrorDeValidacion as e:
            campo, error = e.args[0].values()
            set_estado("error")
            set_errores(lambda _: {**_, campo: error})

    return Main(
        Contenedor(
            Cabecera(
                "Registrar nuevo usuario",
            ),
            Formulario(
                DatosUsuario(
                    {
                        "nombre": "",
                        "contraseña": "",
                    }
                ),
                {
                    "id": "registro-form",
                    "on_submit": subir,
                },
                Campos(),
            ),
        ),
    )


def Campos():
    contexto = use_context(contexto_formulario)
    estado = contexto["estado"]

    return html.div(
        {"className": "flex flex-col gap-6 mt-16 ma max-w-sm"},
        html.div(
            {"className": "flex flex-col gap-6"},
            Input(
                label="Nombre de usuario",
                campo="nombre",
                props={
                    "type": "text",
                    "id": "nombre",
                    "required": True,
                    "min_length": NOMBRE_MÍNIMO,
                },
            ),
            Contraseña(
                {
                    "required": True,
                    "min_length": CONTRASEÑA_MÍNIMA,
                    "id": "contraseña",
                },
            ),
        ),
        MensajeCarga(
            "Registrando...",
        ),
        MensajeExito(
            "Usuario registrado con éxito",
        ),
        html.div(
            {"className": "flex flex-col gap-1.5 w-full"},
            html.button(
                {
                    "className": "btn btn-primario",
                    "disabled": estado == "subiendo" or estado == "éxito",
                },
                "Registrar",
            ),
            link(
                {
                    "to": "/",
                    "class_name": "btn btn-secundario",
                },
                "Ir al inicio de sesión",
            ),
        ),
    )
