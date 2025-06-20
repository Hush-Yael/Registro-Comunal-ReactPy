from reactpy import component, event, html, use_context, use_ref
from reactpy.types import VdomAttributes, VdomChildren

from vistas.componentes.formulario.index import contexto_formulario


@component
def Input(
    label: str,
    campo: str,
    desc: str | None = None,
    props: VdomAttributes = {},
):
    errores = use_context(contexto_formulario)["errores"]
    error = errores[campo]

    id = props.get("id")

    return Contenedor(
        html.label(
            {"for": id},
            Titulo(label),
            _input(
                campo,
                id,
                desc,
                error,
                props,
            ),
        ),
        Descripcion(desc, id),
        MensajeError(error, id),
    )


@component
def Contenedor(*children: VdomChildren):
    return html.div(
        {"className": "flex flex-col gap-1.5"},
        *children,
    )


@component
def _input(
    campo: str,
    id: str,
    desc: str | None = None,
    error: str | None = None,
    props: VdomAttributes = {},
):
    contexto = use_context(contexto_formulario)
    datos, set_datos = contexto["datos"], contexto["set_datos"]
    errores, set_errores = contexto["errores"], contexto["set_errores"]

    valor_anterior = use_ref(datos[campo])

    # se guarda el último valor ingresado para compararlo al cambiarlo
    def focus(evento):
        valor_anterior.current = datos[campo]
        if "on_focus" in props:
            props["on_focus"](evento)  # type: ignore

    # se guarda el último valor ingresado para compararlo al cambiarlo
    def blur(evento):
        valor_anterior.current = datos[campo]
        if "on_blur" in props:
            props["on_blur"](evento)  # type: ignore

    @event
    async def change(evento):
        valor = evento["target"]["value"]

        # se eliminan los errores cuando se cambia el valor que provoca el error
        if errores[campo] and valor != valor_anterior.current:
            set_errores(lambda _: {**_, campo: ""})  # type: ignore

        set_datos(
            lambda valor_actual: {**valor_actual, campo: valor}  # type: ignore
        )
        if "on_change" in props:
            await props["on_change"](evento)

    return html.input(
        {
            **props,
            "className": "w-full p-0.5 px-2 rounded border border-neutral-300 bg-neutral-100 aria-[invalid=true]:border-red-500 aria-[invalid=true]:outline-red-500 aria-[invalid=true]:text-red-500",
            "value": datos[campo],
            "on_focus": focus,
            "on_blur": blur,
            "on_change": change,
            "aria-invalid": bool(error),
            "aria-describedby": id + "-desc" if id and desc else None,
            "aria-errormessage": id + "-error" if id and error else None,
        }
    )


@component
def Titulo(texto: str):
    return html.p({"className": "text-neutral-700"}, texto)


@component
def Descripcion(texto: str, id: str | None = None):
    if texto:
        return html.p(
            {
                "className": "ml-0.5 text-xs text-neutral-500",
                "id": id + "-desc" if id else None,
            },
            texto,
        )


@component
def MensajeError(texto: str, id: str | None = None):
    if texto:
        return html.p(
            {"className": "text-xs text-red-500", "id": id + "-error" if id else None},
            texto,
        )
