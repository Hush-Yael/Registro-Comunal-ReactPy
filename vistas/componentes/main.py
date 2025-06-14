from reactpy import component, html
from reactpy.types import VdomChildren

@component
def Main(*children: VdomChildren):
    return html.main(
        {"class": "flex flex-col h-full p-4"},
        children
    )