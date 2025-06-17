from reactpy import component, event, html, use_state
from reactpy_router import link

from lib.db.subida import registrar_usuario
from constantes.db import (
    NOMBRE_MÍNIMO,
    CONTRASEÑA_MÍNIMA,
    DatosUsuario,
    ErrorDeValidacion,
)

from .componentes.alerta import Alerta
from .componentes.main import Main
from .componentes.formulario.input import Input
from .componentes.formulario.contraseña import Contraseña
from .componentes.contenedor import Cabecera, Contenedor


@component
def Registro():
    datos_iniciales: DatosUsuario = {
        "nombre": "",
        "contraseña": "",
    }

    datos, set_datos = use_state(datos_iniciales)
    respuesta, set_respuesta = use_state(
        {"estado": "", "error": {"mensaje": "", "motivo": ""}}
    )

    @event(prevent_default=True)
    async def subir(_):
        set_respuesta({"estado": "subiendo", "error": {"mensaje": "", "motivo": ""}})
        try:
            await registrar_usuario(datos)
            set_respuesta({"estado": "éxito", "error": {"mensaje": "", "motivo": ""}})
            set_datos({"nombre": "", "contraseña": ""})
        except ErrorDeValidacion as e:
            datos_error = e.args[0]
            set_respuesta({"estado": "error", "error": datos_error})

    return Main(
        Contenedor(
            Cabecera(
                "Registrar nuevo usuario",
            ),
            html.form(
                {
                    "className": "flex flex-col gap-6 mt-16 ma max-w-sm",
                    "id": "registro-form",
                    "on_submit": subir,
                },
                html.div(
                    {"className": "flex flex-col gap-6"},
                    Input(
                        label="Nombre de usuario",
                        error=respuesta["error"]["mensaje"]  # type: ignore
                        if respuesta["error"]["motivo"].startswith("nombre")  # type: ignore
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
                                    "nombre": evento["target"]["value"].strip(),
                                }
                            ),
                        },
                    ),
                    Contraseña(
                        error=respuesta["error"]["mensaje"]  # type: ignore
                        if respuesta["error"]["motivo"].startswith("contraseña")  # type: ignore
                        else None,
                        props={
                            "required": True,
                            "min_length": CONTRASEÑA_MÍNIMA,
                            "value": datos["contraseña"],
                            "id": "contraseña",
                            "on_change": lambda evento: set_datos(
                                lambda valor_actual: {
                                    **valor_actual,
                                    "contraseña": evento["target"]["value"],
                                }
                            ),
                        },
                    ),
                ),
                Alerta(
                    "Registrando...",
                    "carga",
                    visible=respuesta["estado"] == "subiendo",
                ),
                Alerta(
                    "Usuario registrado con éxito",
                    "éxito",
                    respuesta["estado"] == "éxito",
                ),
                html.div(
                    {"className": "flex flex-col gap-1.5 w-full"},
                    html.button(
                        {
                            "className": "btn btn-primario",
                            "disabled": respuesta["estado"] == "subiendo"
                            or respuesta["estado"] == "éxito",
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
            ),
        ),
    )
