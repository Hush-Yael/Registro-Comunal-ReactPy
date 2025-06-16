from reactpy import component, html
from reactpy.types import VdomDict, VdomChildren


@component
def Input(
    label: str,
    desc: str | None = None,
    props: VdomDict = {},  # type: ignore
    error: str | None = None,
):
    id = props.get("id")

    return Contenedor(
        html.label(
            {"for": props.get("id")},
            Titulo(label),
            _input(props, id, desc, error),
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
    props: VdomDict = {},  # type: ignore
    id: str | None = None,
    desc: str | None = None,
    error: str | None = None,
):
    describedby = f"{id + '-desc' if id and desc else ''} {id + '-error' if id and error else ''}".strip()

    return html.input(
        {
            **props,
            "className": "w-full p-0.5 px-2 rounded border border-neutral-300 bg-neutral-100 aria-[invalid=true]:border-red-500 aria-[invalid=true]:outline-red-500 aria-[invalid=true]:text-red-500",
            "aria-invalid": bool(error),
            "aria-describedby": describedby or None,
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
