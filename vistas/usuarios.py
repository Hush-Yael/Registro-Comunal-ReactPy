from reactpy import (
    component,
    html,
    use_context,
    use_effect,
    use_state,
    use_ref,
)
from reactpy_router import link
from typing import Callable

from lib.db.obtencion import obtener_usuarios
from lib.db.modificacion import cambiar_rol, eliminar_usuario
from constantes.db import Sesion
from contexto.sesion import contexto_sesion
from contexto.eliminar_usuario import contexto_eliminar_usuario

from .componentes.terminar_sesion import TerminarSesion
from .componentes.carga import Carga
from .componentes.tabla import Fila, Tabla
from .componentes.contenedor import Contenedor, Cabecera
from .componentes.main import Main
from .componentes.iconos import Iconos
from .componentes.modal import Modal


@component
def Usuarios():
    abierto, set_abierto = use_state(False)
    usuarios, set_usuarios = use_state([])
    usuario_a_eliminar = use_ref("")

    async def eliminar(_):
        nombre = usuario_a_eliminar.current
        await eliminar_usuario(nombre)
        set_usuarios(
            lambda anteriores: list(
                filter(lambda u: u["usuario"] != nombre, anteriores)
            )
        )
        usuario_a_eliminar.current = ""

    return contexto_eliminar_usuario(
        Main(
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
                        TerminarSesion(),
                    ),
                ),
                Tabla(
                    [
                        {"label": "#", "tamaño": 3},
                        {"label": "Usuario", "tamaño": 25},
                        {"label": "Rol", "tamaño": 5},
                        {"label": "Acciones", "tamaño": 15, "pos": "right"},
                    ],
                    Datos(usuarios, set_usuarios),
                ),
            )
        ),
        Modal(
            html.div(
                {"className": "flex flex-col gap-2"},
                html.h1({"className": "font-bold"}, "Eliminar usuario"),
                html.p(
                    {"className": "text-neutral-500"},
                    "¿Realmente quieres eliminar el usuario?",
                ),
            ),
            abierto=abierto,
            set_abierto=set_abierto,
            confirmar=eliminar,
            confirmar_txt="Eliminar",
        ),
        value={
            "abierto": abierto,
            "set_abierto": set_abierto,
            "usuario": usuario_a_eliminar,
        },
    )


def Datos(
    usuarios: list[Sesion] = [],
    set_usuarios: Callable[[Callable[[list[Sesion]], list[Sesion]]], None] = None,  # type: ignore
):
    sesion = use_context(contexto_sesion)["sesion"]

    ADMIN = sesion["rol"] == "admin"

    cargado, set_cargado = use_state(False)

    async def obtencion():
        set_usuarios(await obtener_usuarios())  # type: ignore
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
                BtnEliminar(usuarios[i]["usuario"])
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


def BtnEliminar(usuario: str):
    contexto = use_context(contexto_eliminar_usuario)
    set_abierto = contexto["set_abierto"]
    usuario_a_eliminar = contexto["usuario"]

    sesion = use_context(contexto_sesion)["sesion"]

    async def eliminar(_):
        if sesion["rol"] != "admin":
            return

        set_abierto(True)
        usuario_a_eliminar.current = usuario

    return html.button(
        {
            "className": "btn btn-peligro ml-auto px-1.25!",
            "on_click": eliminar,
            "disabled": sesion["rol"] != "admin",
        },
        Iconos.Eliminar(),
    )
