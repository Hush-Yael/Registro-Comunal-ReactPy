from flask import Flask
from reactpy import html, component, use_state
from reactpy.backend.flask import configure, Options
from reactpy_router import browser_router, route

from vistas.formulario import Formulario
from vistas._404 import NoEncontrado
from vistas.login import Login
from vistas.registro import Registro

from flaskwebgui import FlaskUI  # type: ignore

app = Flask(__name__)


# Raíz con las rutas de la aplicación
@component
def root():
    autenticado, set_autenticado = use_state(False)

    # si no ha iniciado sesión, se redirige siempre al login
    if not autenticado:
        return browser_router(
            route("/registro", Registro()),
            route("{404:any}", Login(set_autenticado)),
        )

    # si ha iniciado sesión, se activan todas las rutas de la aplicación, menos el login
    return browser_router(
        route("/", Formulario()),
        route("/login", navigate("/", replace=True)),
        route("/registro", navigate("/", replace=True)),
        route("/registros", Registros()),
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
