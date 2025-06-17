from typing import Callable
from reactpy import component, html, event, use_state
from reactpy_router import link, navigate

from lib.db.subida import iniciar_sesion
from constantes.db import (
    Sesion,
    NOMBRE_MÍNIMO,
    CONTRASEÑA_MÍNIMA,
    DatosUsuario,
    ErrorDeValidacion,
)

from .componentes.alerta import Alerta
from .componentes.main import Main
from .componentes.formulario.input import Input
from .componentes.contenedor import Contenedor, Cabecera


@component
def Login(set_sesion: Callable[[Sesion], None]):
    datos_iniciales: DatosUsuario = {"nombre": "", "contraseña": ""}
    datos, set_datos = use_state(datos_iniciales)

    respuesta, set_respuesta = use_state(
        {"estado": "", "error": {"mensaje": "", "motivo": ""}}
    )

    @event(prevent_default=True)
    async def subir(_):
        set_respuesta({"estado": "subiendo", "error": {"mensaje": "", "motivo": ""}})
        try:
            rol = await iniciar_sesion(datos)
            set_sesion({"usuario": datos["nombre"], "rol": rol})
            set_respuesta({"estado": "éxito"})
        except ErrorDeValidacion as e:
            datos_error = e.args[0]
            set_respuesta({"estado": "error", "error": datos_error})

    return Main(
        Contenedor(
            Cabecera(
                "Inicio de sesión",
            ),
            navigate("/") if respuesta["estado"] == "éxito" else None,
            html.form(
                {
                    "className": "flex flex-col mt-16 gap-6",
                    "id": "login-form",
                    "on_submit": subir,
                },
                Input(
                    label="Nombre de usuario",
                    error=respuesta["error"]["mensaje"]  # type: ignore
                    if respuesta["error"]["motivo"] == "no-encontrado"  # type: ignore
                    else None,
                    props={
                        "type": "text",
                        "id": "nombre",
                        "required": True,
                        "min_length": NOMBRE_MÍNIMO,
                        "value": datos["nombre"],
                        "on_change": lambda evento: set_datos(
                            lambda valor_actual: {
                                **valor_actual,
                                "nombre": evento["target"]["value"],
                            }
                        ),
                    },
                ),
                Input(
                    label="Ingrese la contraseña",
                    error=respuesta["error"]["mensaje"]  # type: ignore
                    if respuesta["error"]["motivo"]  # type: ignore
                    == "contraseña-incorrecta"
                    else None,
                    props={
                        "type": "password",
                        "id": "contraseña",
                        "required": True,
                        "min_length": CONTRASEÑA_MÍNIMA,
                        "value": datos["contraseña"],
                        "on_change": lambda evento: set_datos(
                            lambda valor_actual: {
                                **valor_actual,
                                "contraseña": evento["target"]["value"],
                            }
                        ),
                    },
                ),
                Alerta(
                    "Verificando datos...",
                    "carga",
                    visible=respuesta["estado"] == "subiendo",
                ),
                html.div(
                    {"className": "flex flex-col gap-1.5"},
                    html.button(
                        {
                            "className": "btn btn-primario",
                            "form": "login-form",
                            "disabled": respuesta["estado"] == "subiendo",
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
            ),
        ),
    )
