from reactpy import component, html
from reactpy.types import VdomDict


@component
def Input(label: str, desc: str = None, input_props: VdomDict = {}):  # type: ignore
    return html.div(
        {"className": "flex flex-col gap-1"},
        html.label(
            {"for": input_props.get("id")},
            html.p(
                {"className": "text-neutral-700"},
                label,
            ),
            html.input(
                {
                    "className": "w-full p-0.5 px-2 rounded border border-neutral-300 bg-neutral-100",
                    **input_props,
                }
            ),
        ),
        html.p(
            {"className": "text-xs", "id": input_props.get("aria-describedby")},
            desc,
        )
        if desc
        else None,
    )
