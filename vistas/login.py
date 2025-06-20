from reactpy import component, html, use_context
from reactpy_router import link, navigate

from lib.db.subida import iniciar_sesion
from constantes.db import (
    NOMBRE_MÍNIMO,
    CONTRASEÑA_MÍNIMA,
    DatosUsuario,
    ErrorDeValidacion,
)
from contexto.sesion import contexto_sesion

from .componentes.formulario.index import (
    Formulario,
    MensajeCarga,
    contexto_formulario,
    ContextoFormulario,
)
from .componentes.main import Main
from .componentes.contenedor import Contenedor, Cabecera
from .componentes.formulario.input import Input
from .componentes.formulario.contraseña import Contraseña


@component
def Login():
    set_sesion = use_context(contexto_sesion)["set_sesion"]

    async def subir(contexto: ContextoFormulario):
        datos, set_estado, set_errores = (
            contexto["datos"],
            contexto["set_estado"],
            contexto["set_errores"],
        )

        try:
            rol = await iniciar_sesion(datos)
            set_sesion({"usuario": datos["nombre"], "rol": rol})
            set_estado("éxito")
        except ErrorDeValidacion as e:
            campo, error = e.args[0].values()
            set_estado("error")
            set_errores(lambda _: {**_, campo: error})

    return Main(
        Contenedor(
            Cabecera(
                "Inicio de sesión",
            ),
            Formulario(
                DatosUsuario({"nombre": "", "contraseña": ""}),
                {
                    "id": "login-form",
                    "on_submit": subir,
                },
                Campos(),
            ),
        ),
    )


@component
def Campos():
    contexto = use_context(contexto_formulario)
    estado = contexto["estado"]

    return html.div(
        {
            "className": "flex flex-col mt-16 gap-6",
        },
        navigate("/") if estado == "éxito" else None,
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
                "type": "password",
                "required": True,
                "min_length": CONTRASEÑA_MÍNIMA,
            },
        ),
        MensajeCarga(
            "Verificando datos...",
        ),
        html.div(
            {"className": "flex flex-col gap-1.5"},
            html.button(
                {
                    "className": "btn btn-primario",
                    "form": "login-form",
                    "disabled": estado == "subiendo",
                },
                "Entrar",
            ),
            link(
                {
                    "to": "/registro",
                    "class_name": "btn btn-secundario",
                },
                "Ir al registro",
            ),
        ),
    )
