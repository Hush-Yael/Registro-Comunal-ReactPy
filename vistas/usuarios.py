from reactpy import component, html, use_effect, use_state
from reactpy_router import link
from typing import Any, Callable

from lib.db.obtencion import obtener_usuarios
from lib.db.modificacion import cambiar_rol, eliminar_usuario
from constantes.db import Sesion

from .componentes.terminar_sesion import TerminarSesion
from .componentes.carga import Carga
from .componentes.tabla import Fila, Tabla
from .componentes.contenedor import Contenedor, Cabecera
from .componentes.main import Main
from .componentes.iconos import Iconos


@component
def Usuarios(sesion: Sesion, set_sesion: Callable[[Sesion], None]):
    return Main(
        Contenedor(
            Cabecera(
                "Lista de usuarios",
                html.div(
                    {"className": "flex flex-col gap-2"},
                    link(
                        {"to": "/", "class_name": "btn btn-primario"},
                        Iconos.FlechaAtras(),
                        "Ir al formulario",
                    ),
                    TerminarSesion(set_sesion),
                ),
            ),
            Tabla(
                [
                    {"label": "#", "tamaño": 3},
                    {"label": "Usuario", "tamaño": 25},
                    {"label": "Rol", "tamaño": 5},
                    {"label": "Acciones", "tamaño": 15, "pos": "right"},
                ],
                Datos(sesion),
            ),
        )
    )


def Datos(sesion: Sesion):
    ADMIN = sesion["rol"] == "admin"

    cargado, set_cargado = use_state(False)
    usuarios, set_usuarios = use_state([])

    async def obtencion():
        set_usuarios(await obtener_usuarios())
        set_cargado(True)

    # carga de usuarios
    use_effect(obtencion, [])

    def es_usuario_actual(nombre_usuario):
        return nombre_usuario == sesion["usuario"]

    async def _cambiar_rol(evento, usuario: str):
        rol = evento["target"]["value"]
        await cambiar_rol({"rol": rol, "usuario": usuario})

    if not cargado:
        return html.tr(
            html.td(
                {"colspan": "4"},
                html.p(
                    {
                        "className": "text-center items-center gap-2 m-auto py-4 bg-neutral-100 rounded-md",
                        "role": "status",
                    },
                    Carga({"className": "size-4 mr-2"}),
                    "Cargando...",
                ),
            ),
        )

    return (
        Fila(
            html.td({"className": "p-2 text-neutral-500"}, i + 1),
            html.td({"className": "p-2"}, [usuarios[i]["usuario"]]),
            html.td(
                {"className": "p-2"},
                Roles(_cambiar_rol, usuarios[i])
                if ADMIN and not es_usuario_actual(usuarios[i]["usuario"])
                else [usuarios[i]["rol"]],
            ),
            html.td(
                {"className": "p-2 text-right"},
                BtnEliminar(usuarios[i]["usuario"], set_usuarios)
                if not es_usuario_actual(usuarios[i]["usuario"])
                else html.i(
                    {
                        "className": "block text-neutral-500 text-right ml-auto",
                        "role": "status",
                    },
                    "Usuario actual",
                ),
            ),
        )
        for i in range(len(usuarios))
    )


def Roles(func: Callable, datos: Sesion):
    async def change(_):
        return await func(_, datos["usuario"])

    return html.select(
        {
            "default_value": datos["rol"],
            "on_change": change,
        },
        html.option("admin"),
        html.option("supervisor"),
    )


def BtnEliminar(usuario: str, set_usuarios: Callable[[Any], None]):
    async def eliminar(_):
        await eliminar_usuario(usuario)
        set_usuarios(
            lambda anteriores: list(
                filter(lambda u: u["usuario"] != usuario, anteriores)
            )
        )

    return html.button(
        {
            "className": "btn btn-peligro ml-auto px-1.25!",
            "on_click": eliminar,
        },
        Iconos.Eliminar(),
    )
