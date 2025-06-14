from flask import Flask
from reactpy import html, component
from reactpy.backend.flask import configure, Options
from reactpy_router import browser_router, route
from vistas.index import Inicio
from vistas._404 import NoEncontrado
from flaskwebgui import FlaskUI # type: ignore

from vistas.login import Login
from vistas.registro import Registro # type: ignore

app = Flask(__name__)

# Raíz con las rutas de la aplicación
@component
def root():
    return browser_router(
        route("/", Inicio()),
        route("/registro", Registro()),
        route("/login", Login()),
        route("{404:any}", NoEncontrado()),
    )
    
# Configuración de la aplicación para su funcionamiento
configure(
    # instancia de la aplicación de Flask
    app,
    # raíz de la aplicación
    root,
    Options(
        # Cambiar la cabecera de la página
        head=html.head(
            html.title("Mi aplicación"),
            # Meta para el viewport, de modo que se adapte al tamaño de la pantalla
            html.meta(
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ),
            # Importar la hoja de estilos
            html.link({"rel": "stylesheet", "href": "/static/css/index.css"}),
        )
    ),
)

if __name__ == "__main__":
    # Para visualizar en el navegador:
    # app.run(debug=True)
    # Para visualizar en la webview:
    FlaskUI(app=app, server="flask", width=800, height=700).run()
