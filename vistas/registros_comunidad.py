from reactpy import component, html, use_effect, use_state, use_context
from math import ceil
from re import search, IGNORECASE


from contexto.registros_comunidad import contexto_registros
from lib.db.obtencion import obtener_datos_comunidad

from .componentes.carga import Carga
from .componentes.tabla import Tabla, Fila
from .componentes.main import Main
from .componentes.contenedor import Contenedor, Cabecera


@component
def RegistrosComunidad():
    registros, set_registros = use_state([])
    cantidad_registros_mostrados, set_cantidad_registros_mostrados = use_state(0)
    busqueda, set_busqueda = use_state("")
    filtro, set_filtro = use_state("nombres")
    pagina, set_pagina = use_state(0)
    limite_registros, set_limite_registros = use_state(10)

    return Main(
        Contenedor(
            Cabecera(
                "Lista de registros",
            ),
            contexto_registros(
                html.div(
                    {"className": "flex flex-col items-start gap-3 mt-8"},
                    Filtros(),
                    Tabla(
                        [
                            {"label": "#", "tamaño": 5},
                            {"label": "Nombres", "tamaño": 20},
                            {"label": "Apellidos", "tamaño": 20},
                            {"label": "Cédula", "tamaño": 10},
                            {
                                "label": html.span("Fecha de", html.br(), "nacimiento"),
                                "tamaño": 8,
                                "pos": "center",
                            },
                            {"label": "Patología / condición", "tamaño": 18},
                            {"label": "Dirección", "tamaño": 18},
                            {"label": "N° casa", "tamaño": 5},
                        ],
                        {"className": "max-h-[45vh]"},
                        Datos(),
                    ),
                    Paginacion(),
                ),
                value={
                    "registros": registros,
                    "set_registros": set_registros,
                    "cantidad_registros_mostrados": cantidad_registros_mostrados,
                    "set_cantidad_registros_mostrados": set_cantidad_registros_mostrados,
                    "busqueda": busqueda,
                    "set_busqueda": set_busqueda,
                    "filtro": filtro,
                    "set_filtro": set_filtro,
                    "pagina": pagina,
                    "set_pagina": set_pagina,
                    "limite_registros": limite_registros,
                    "set_limite_registros": set_limite_registros,
                },
                key="registros_comunidad",
            ),
        )
    )


@component
def Filtros():
    contexto = use_context(contexto_registros)
    set_busqueda, filtro, set_filtro, limite_registros, set_limite_registros = (
        contexto["set_busqueda"],
        contexto["filtro"],
        contexto["set_filtro"],
        contexto["limite_registros"],
        contexto["set_limite_registros"],
    )

    return html.header(
        {"className": "flex items-center justify-between gap-4 w-full"},
        html.div(
            {"className": "flex items-center gap-3"},
            html.label(
                {"className": "flex flex-col"},
                "Búsqueda:",
                html.input(
                    {
                        "type": "search",
                        "className": " p-1 px-2 border border-neutral-300 rounded bg-neutral-100",
                        "on_change": lambda e: set_busqueda(e["target"]["value"]),
                    }
                ),
            ),
            html.label(
                {"className": "flex flex-col"},
                "Filtro:",
                html.select(
                    {
                        "className": " p-1 px-1 border border-neutral-300 rounded bg-neutral-100",
                        "on_change": lambda e: set_filtro(e["target"]["value"]),
                        "value": filtro,
                    },
                    html.option({"value": "nombres"}, "Nombres"),
                    html.option({"value": "apellidos"}, "Apellidos"),
                    html.option({"value": "cedula"}, "Cédula"),
                    html.option({"value": "fecha_nacimiento"}, "Fecha de nacimiento"),
                    html.option({"value": "patologia"}, "Patología / condición"),
                    html.option({"value": "direccion"}, "Dirección"),
                    html.option({"value": "numero_casa"}, "N° casa"),
                ),
            ),
        ),
        html.label(
            {"className": "flex flex-col gap-1"},
            html.div(
                {"className": "flex gap-4"},
                "Límite de registros por página:",
                html.span(
                    {"className": "text-neutral-500"},
                    limite_registros,
                ),
            ),
            html.input(
                {
                    "className": "accent-neutral-900",
                    "type": "range",
                    "step": 10,
                    "min": 10,
                    "max": 100,
                    "value": limite_registros,
                    "on_change": lambda e: set_limite_registros(
                        int(e["target"]["value"])
                    ),
                }
            ),
        ),
    )


@component
def Datos():
    contexto = use_context(contexto_registros)
    (
        registros,
        set_registros,
        set_cantidad_registros_mostrados,
        filtro,
        busqueda,
        pagina,
    ) = (
        contexto["registros"],
        contexto["set_registros"],
        contexto["set_cantidad_registros_mostrados"],
        contexto["filtro"],
        contexto["busqueda"],
        contexto["pagina"],
    )
    registros_paginados, set_registros_paginados = use_state([])
    cargado, set_cargado = use_state(False)

    async def obtencion():
        set_registros(await obtener_datos_comunidad())  # type: ignore
        set_cargado(True)

    # carga de usuarios
    use_effect(obtencion, [])

    def filtrar_registros():
        if len(registros) > 0:
            _registros = (
                registros
                if busqueda.strip() == ""
                else list(
                    filter(
                        lambda registro: search(
                            busqueda, str(registro[filtro]), IGNORECASE
                        ),
                        registros,
                    )
                )
            )

            set_cantidad_registros_mostrados(len(_registros))

            set_registros_paginados(
                _registros[
                    pagina * contexto["limite_registros"] : (pagina + 1)
                    * contexto["limite_registros"]
                ]
            )
        else:
            set_registros_paginados([])
            set_cantidad_registros_mostrados(0)

    # filtrado y paginado
    use_effect(
        filtrar_registros,
        [registros, busqueda, pagina],
    )

    if not cargado:
        return html.tr(
            html.td(
                {"colspan": "8"},
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
    elif len(registros) == 0:
        return html.tr(
            html.td(
                {"colspan": "8"},
                html.p(
                    {
                        "className": "text-center items-center gap-2 m-auto py-4 bg-neutral-100 rounded-md",
                        "role": "status",
                    },
                    "No se encontraron registros",
                ),
            ),
        )

    return html._(
        Fila(
            (
                html.td({"className": "p-2", "key": f"{key}-{i}"}, text)
                for key, text in registros_paginados[i].items()
            ),
            props={"key": f"tr-{i}"},
        )
        for i in range(len(registros_paginados))
    )


btn_class = "min-w-[2rem] p-1 px-2 rounded-md not-aria-[current=page]:bg-neutral-200"


@component
def Paginacion():
    contexto = use_context(contexto_registros)
    cantidad_registros_mostrados, pagina, set_pagina, limite_registros = (
        contexto["cantidad_registros_mostrados"],
        contexto["pagina"],
        contexto["set_pagina"],
        contexto["limite_registros"],
    )

    numero_paginas = ceil(cantidad_registros_mostrados / limite_registros)

    use_effect(
        lambda: set_pagina(numero_paginas - 1)
        if numero_paginas >= 1 and pagina > numero_paginas - 1
        else None,
        [pagina, cantidad_registros_mostrados, limite_registros],
    )

    if numero_paginas > 1:
        return html.nav(
            {"className": "w-full max-w-[90vw] m-auto mt-3 overflow-auto"},
            html.ul(
                {
                    "className": "flex items-center gap-2",
                },
                html.li(
                    html.button(
                        {
                            "className": btn_class,
                            "on_click": lambda _: set_pagina(pagina - 1),
                            "disabled": pagina == 0,
                        },
                        "<",
                    )
                ),
                (
                    html.li(
                        html.button(
                            {
                                "aria-current": "page" if i == pagina else None,
                                "className": btn_class
                                + " aria-[current=page]:bg-neutral-900 aria-[current=page]:text-white aria-[current=page]:font-bold",
                                "value": i,
                                "on_click": lambda evento: set_pagina(
                                    int(evento["target"]["value"])
                                ),
                                "key": f"{i}-pagina-btn",
                            },
                            i + 1,
                        ),
                    )
                    for i in range(numero_paginas)
                ),
                html.li(
                    html.button(
                        {
                            "className": btn_class,
                            "on_click": lambda _: set_pagina(pagina + 1),
                            "disabled": pagina == numero_paginas - 1,
                        },
                        ">",
                    )
                ),
            ),
        )
