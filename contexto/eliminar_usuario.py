from typing import Callable, TypedDict
from reactpy import Ref
from reactpy import create_context


class Contexto(TypedDict):
    abierto: bool
    set_abierto: Callable[[bool], None]
    usuario: Ref[str]


_default: Contexto = {
    "abierto": False,
    "set_abierto": lambda _: None,
    "usuario": Ref(""),
}

contexto_eliminar_usuario = create_context(_default)
