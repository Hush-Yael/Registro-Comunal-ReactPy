from flask import Flask
from reactpy import html, component, use_state
from reactpy.backend.flask import configure, Options
from reactpy_router import browser_router, route, navigate
from contexto.sesion import contexto_sesion

from constantes.db import Sesion
from vistas.registro_comunidad import RegistroComunidad
from vistas._404 import NoEncontrado
from vistas.login import Login
from vistas.registro_usuarios import RegistroUsuarios
from vistas.registros_comunidad import RegistrosComunidad
from vistas.lista_usuarios import Usuarios

from flaskwebgui import FlaskUI  # type: ignore

app = Flask(__name__)


# Raíz con las rutas de la aplicación
@component
def root():
    _sesion: Sesion = {"usuario": "", "rol": ""}
    sesion, set_sesion = use_state(_sesion)

    # si no ha iniciado sesión, se redirige siempre al login
    if not sesion["usuario"]:
        return contexto_sesion(
            browser_router(
                route("/registro", RegistroUsuarios()),
                route("{404:any}", Login()),
            ),
            value={"sesion": sesion, "set_sesion": set_sesion},
        )

    # si ha iniciado sesión, se activan todas las rutas de la aplicación, menos el login
    return contexto_sesion(
        browser_router(
            route("/", RegistroComunidad()),
            route("/login", navigate("/", replace=True)),
            route("/registro", navigate("/", replace=True)),
            route("/usuarios", Usuarios()),
            route("/registros", RegistrosComunidad()),
            route("{404:any}", NoEncontrado()),
        ),
        value={"sesion": sesion, "set_sesion": set_sesion},
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
            # Se añade la funcionalidad de los modales
            html.script({"src": "/static/js/modales.js"}),
        )
    ),
)

if __name__ == "__main__":
    # Para visualizar en el navegador:
    # app.run(debug=True)
    # Para visualizar en la webview:
    FlaskUI(app=app, server="flask", fullscreen=True).run()
