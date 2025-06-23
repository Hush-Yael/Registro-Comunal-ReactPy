from typing import Callable, TypedDict
from reactpy import create_context

from constantes.db import DatosComunidad


class Contexto(TypedDict):
    registros: list[DatosComunidad]
    set_registros: Callable[[list[DatosComunidad]], None]
    cantidad_registros_mostrados: int
    set_cantidad_registros_mostrados: Callable[[int], None]
    busqueda: str
    set_busqueda: Callable[[str], None]
    filtro: str
    set_filtro: Callable[[str], None]
    pagina: int
    set_pagina: Callable[[int], None]
    limite_registros: int
    set_limite_registros: Callable[[int], None]


contexto_registros = create_context(
    Contexto(
        {
            "registros": [],
            "set_registros": lambda _: None,
            "cantidad_registros_mostrados": 0,
            "set_cantidad_registros_mostrados": lambda _: None,
            "busqueda": "",
            "set_busqueda": lambda _: None,
            "filtro": "nombres",
            "set_filtro": lambda _: None,
            "pagina": 0,
            "set_pagina": lambda _: None,
            "limite_registros": 0,
            "set_limite_registros": lambda _: None,
        }
    )
)
