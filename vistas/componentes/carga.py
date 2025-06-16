from reactpy import component, html, svg
from reactpy.types import VdomDict


@component
def Carga(p: VdomDict = {}):  # type: ignore
    return html.svg(
        {
            **p,
            "className": f"carga {p.get('className', '')}",
            "viewBox": "0 0 40 40",
            "height": "40",
            "width": "40",
            "fill": "none",
        },
        svg.circle(
            {
                "className": "track",
                "cx": "20",
                "cy": "20",
                "r": "17.5",
                "pathlength": "100",
                "stroke-width": "5px",
                "fill": "none",
            }
        ),
        svg.circle(
            {
                "className": "car",
                "cx": "20",
                "cy": "20",
                "r": "17.5",
                "pathlength": "100",
                "stroke-width": "5px",
                "fill": "none",
            }
        ),
    )
