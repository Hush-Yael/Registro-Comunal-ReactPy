from reactpy import component, html, svg
from reactpy.types import VdomDict


class Iconos:
    @component
    def Casa(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {
                **p,
                "viewBox": "0 0 32 32",
                "xmlns": "http://www.w3.org/2000/svg",
            },
            svg.path(
                {
                    "d": "M30.854,16.548C30.523,17.43,29.703,18,28.764,18H28v11c0,0.552-0.448,1-1,1h-6v-7c0-2.757-2.243-5-5-5  s-5,2.243-5,5v7H5c-0.552,0-1-0.448-1-1V18H3.235c-0.939,0-1.759-0.569-2.09-1.451c-0.331-0.882-0.088-1.852,0.62-2.47L13.444,3.019  c1.434-1.357,3.679-1.357,5.112,0l11.707,11.086C30.941,14.696,31.185,15.666,30.854,16.548z"
                }
            ),
        )

    @component
    def Personas(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {**p, "viewBox": "0 0 96 96"},
            svg.circle(
                {
                    "cx": "24",
                    "cy": "30.8",
                    "r": "9",
                }
            ),
            svg.circle(
                {
                    "cx": "72",
                    "cy": "30.8",
                    "r": "9",
                }
            ),
            svg.path(
                {
                    "d": " M 66 74.2 L 66 65.2 C 66 63.8 65.4 62.4 64.2 61.6 C 61.8 59.6 58.6 58.2 55.4 57.4 C 53.2 56.8 50.6 56.2 48 56.2 C 45.6 56.2 43 56.6 40.6 57.4 C 37.4 58.2 34.4 59.8 31.8 61.6 C 30.6 62.6 30 63.8 30 65.2 L 30 74.2 L 66 74.2 Z"
                }
            ),
            svg.circle({"cx": "48", "cy": "44.8", "r": "9"}),
            svg.path(
                {
                    "d": " M 88.2 47.6 C 85.8 45.6 82.6 44.2 79.4 43.4 C 77.2 42.8 74.6 42.2 72 42.2 C 69.6 42.2 67 42.6 64.6 43.4 C 63.4 43.8 62.2 44.2 61 44.8 L 61 45 C 61 48.4 59.6 51.6 57.4 53.8 C 61.2 55 64.2 56.6 66.6 58.4 C 67.2 59 67.8 59.4 68.2 60.2 L 90 60.2 L 90 51.2 C 90 49.8 89.4 48.4 88.2 47.6 Z"
                }
            ),
            svg.path(
                {
                    "d": " M 29.4 58.4 L 29.4 58.4 C 32.2 56.4 35.4 54.8 38.6 53.8 C 36.4 51.4 35 48.4 35 45 C 35 44.8 35 44.8 35 44.6 C 33.8 44.2 32.6 43.6 31.4 43.4 C 29.2 42.8 26.6 42.2 24 42.2 C 21.6 42.2 19 42.6 16.6 43.4 C 13.4 44.4 10.4 45.8 7.8 47.6 C 6.6 48.4 6 49.8 6 51.2 L 6 60.2 L 27.6 60.2 C 28.2 59.4 28.6 59 29.4 58.4 Z"
                }
            ),
        )

    @component
    def N404(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {**p, "viewBox": "0 0 32 32"},
            svg.g(
                svg.circle(
                    {
                        "cx": "7.5",
                        "cy": "5.5",
                        "r": "0.5",
                    }
                ),
                svg.circle(
                    {
                        "cx": "5.5",
                        "cy": "5.5",
                        "r": "0.5",
                    }
                ),
                svg.circle(
                    {
                        "cx": "3.5",
                        "cy": "5.5",
                        "r": "0.5",
                    }
                ),
                svg.path(
                    {
                        "d": "M30.5,8h-29C1.224,8,1,7.776,1,7.5S1.224,7,1.5,7h29C30.776,7,31,7.224,31,7.5S30.776,8,30.5,8z"
                    }
                ),
                svg.path(
                    {
                        "d": "M29.5,29h-27C1.673,29,1,28.327,1,27.5v-23C1,3.673,1.673,3,2.5,3h27C30.327,3,31,3.673,31,4.5v23      C31,28.327,30.327,29,29.5,29z M2.5,4C2.224,4,2,4.225,2,4.5v23C2,27.775,2.224,28,2.5,28h27c0.276,0,0.5-0.225,0.5-0.5v-23      C30,4.225,29.776,4,29.5,4H2.5z"
                    }
                ),
            ),
            svg.g(
                svg.path(
                    {
                        "d": "M24.5,24c-0.276,0-0.5-0.224-0.5-0.5V21h-3.5c-0.163,0-0.315-0.079-0.409-0.212s-0.117-0.303-0.062-0.456    l2.5-7C22.6,13.133,22.789,13,23,13h1.5c0.276,0,0.5,0.224,0.5,0.5V20h0.5c0.276,0,0.5,0.224,0.5,0.5S25.776,21,25.5,21H25v2.5    C25,23.776,24.776,24,24.5,24z M21.209,20H24v-6h-0.647L21.209,20z"
                    }
                ),
                svg.path(
                    {
                        "d": "M10.5,24c-0.276,0-0.5-0.224-0.5-0.5V21H6.5c-0.163,0-0.315-0.079-0.409-0.212s-0.117-0.303-0.062-0.456    l2.5-7C8.6,13.133,8.789,13,9,13h1.5c0.276,0,0.5,0.224,0.5,0.5V20h0.5c0.276,0,0.5,0.224,0.5,0.5S11.776,21,11.5,21H11v2.5    C11,23.776,10.776,24,10.5,24z M7.209,20H10v-6H9.353L7.209,20z"
                    }
                ),
                svg.path(
                    {
                        "d": "M17.5,24h-3c-0.827,0-1.5-0.673-1.5-1.5v-8c0-0.827,0.673-1.5,1.5-1.5h3c0.827,0,1.5,0.673,1.5,1.5v8    C19,23.327,18.327,24,17.5,24z M14.5,14c-0.276,0-0.5,0.225-0.5,0.5v8c0,0.275,0.224,0.5,0.5,0.5h3c0.276,0,0.5-0.225,0.5-0.5v-8    c0-0.275-0.224-0.5-0.5-0.5H14.5z"
                    }
                ),
            ),
        )

    @component
    def Buscar(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "viewBox": "0 0 24 24",
                "fill": "none",
                "stroke-width": "2",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
            },
            svg.path({"d": "m21 21-4.34-4.34"}),
            svg.circle({"cx": "11", "cy": "11", "r": "8"}),
        )

    @component
    def Eliminar(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "viewBox": "0 0 24 24",
                "fill": "none",
                "stroke-width": "2",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
            },
            svg.path({"d": "M3 6h18"}),
            svg.path({"d": "M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"}),
            svg.path({"d": "M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"}),
            svg.line({"x1": "10", "x2": "10", "y1": "11", "y2": "17"}),
            svg.line({"x1": "14", "x2": "14", "y1": "11", "y2": "17"}),
        )

    @component
    def Añadir(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {"viewBox": "0 0 24 24"},
            svg.path({"d": "M0 0h24v24H0z", "fill": "none"}),
            svg.path(
                {
                    "d": "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm-1-11H7v2h4v4h2v-4h4v-2h-4V7h-2v4z"
                }
            ),
        )

    @component
    def Ver(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {
                **p,
                "viewBox": "0 0 24 24",
                "fill": "none",
                "stroke-width": "2",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
            },
            svg.path(
                {
                    "d": "M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"
                }
            ),
            svg.circle({"cx": "12", "cy": "12", "r": "3"}),
        )

    @component
    def Ocultar(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {
                **p,
                "viewBox": "0 0 24 24",
                "fill": "none",
                "stroke-width": "2",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
            },
            svg.path({"d": "m15 18-.722-3.25"}),
            svg.path({"d": "M2 8a10.645 10.645 0 0 0 20 0"}),
            svg.path({"d": "m20 15-1.726-2.05"}),
            svg.path({"d": "m4 15 1.726-2.05"}),
            svg.path({"d": "m9 18 .722-3.25"}),
        )

    @component
    def FlechaAtras(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {
                **p,
                "viewBox": "0 0 24 24",
                "fill": "none",
                "stroke-width": "2",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
            },
            svg.path({"d": "M9 14 4 9l5-5"}),
            svg.path({"d": "M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5a5.5 5.5 0 0 1-5.5 5.5H11"}),
        )

    @component
    def Salir(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {
                **p,
                "height": "24",
                "viewBox": "0 0 24 24",
                "width": "24",
                "xmlns": "http://www.w3.org/2000/svg",
            },
            svg.path(
                {
                    "d": "M8.51428 20H4.51428C3.40971 20 2.51428 19.1046 2.51428 18V6C2.51428 4.89543 3.40971 4 4.51428 4H8.51428V6H4.51428V18H8.51428V20Z"
                }
            ),
            svg.path(
                {
                    "d": "M13.8418 17.385L15.262 15.9768L11.3428 12.0242L20.4857 12.0242C21.038 12.0242 21.4857 11.5765 21.4857 11.0242C21.4857 10.4719 21.038 10.0242 20.4857 10.0242L11.3236 10.0242L15.304 6.0774L13.8958 4.6572L7.5049 10.9941L13.8418 17.385Z"
                }
            ),
        )

    @component
    def Check(p: VdomDict = {}):  # type: ignore
        return html.svg(
            {
                **p,
                "xmlns": "http://www.w3.org/2000/svg",
                "viewBox": "0 0 24 24",
            },
            svg.path({"stroke": "none", "d": "M0 0h24v24H0z", "fill": "none"}),
            svg.path(
                {
                    "d": "M17 3.34a10 10 0 1 1 -14.995 8.984l-.005 -.324l.005 -.324a10 10 0 0 1 14.995 -8.336zm-1.293 5.953a1 1 0 0 0 -1.32 -.083l-.094 .083l-3.293 3.292l-1.293 -1.292l-.094 -.083a1 1 0 0 0 -1.403 1.403l.083 .094l2 2l.094 .083a1 1 0 0 0 1.226 0l.094 -.083l4 -4l.083 -.094a1 1 0 0 0 -.083 -1.32z"
                }
            ),
        )
