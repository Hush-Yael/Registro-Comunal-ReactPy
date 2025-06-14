Esta es una pequeña aplicación web fullstack desarrollada con Python.

El backend está basado en la librería `Flask`, mientras que el frontend se basa en `ReactPy` y su enrutador `ReactPy Router`. A su vez, se adaptó para que use la webview del sistema para mejorar la experiencia de usuario y hacerla más parecida a una aplicación nativa a través de la librería `flaskwebgui`.

> [!IMPORTANT]
> Se debe usar un `entorno virtual`, ya que se deben hacer modificaciones al código fuente de algunas librerías para poder compilar.

> [!IMPORTANT]
> Para poder compilar la aplicación y que corra correctamente, es necesario modificar el código fuente de la librería ReactPy y ReactPy Router; más específicamente los archivos:
+ `logging.py` _ubicado en `venv/Lib/site-packages/reactpy/`_
+ `components.py` _ubicado en `venv/Lib/site-packages/reactpy_router/`_
+ `_common.py` _ubicado en `venv/Lib/site-packages/reactpy/backend/`_

Esto es debido a que el primero causa un error inexplicable y los otros dos necesitan enviar ciertos archivos al navegador para poder mostrar el frontend, y no está adaptado a un archivo compilado.

#### Las modificaciones en esencia se aseguran de que puedan encontrar los archivos necesarios, y son las siguientes:

## logging.py
Se intenta usar `colorlog` para el logging, pero por alguna razón falla al momento de usar el ejecutable aunque la librería esté instalada, por lo que lo mejor es directamente comentar o borrar esa línea
```diff
"formatters": {
   "generic": {
         "format": "%(asctime)s | %(log_color)s%(levelname)s%(reset)s | %(message)s",
         "datefmt": r"%Y-%m-%dT%H:%M:%S%z",
-          "class": "colorlog.ColoredFormatter",
   }
},
```

## _common.py
Este archivo se encarga de enviar el `index.html` y un `<script>` al cliente, pero al momento de haberse compilado no lo puede encontrar, por lo que se debe adaptar para incluirlo en una carpeta especifica en el bundle.
```diff
- CLIENT_BUILD_DIR = Path(_reactpy_file_path).parent / "_static"

+ if getattr(sys, "frozen", False):
+     CLIENT_BUILD_DIR = (
+         Path(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))))
+         / "reactpy-static"
+     )
+ else:
+     CLIENT_BUILD_DIR = Path(_reactpy_file_path).parent / "_static"
```

## Components.py
Este archivo se encarga de enviar al cliente la lógica de los componentes específicos del enrutador. Al igual que el anterior, se debe adaptar para que pueda habiendo ya compilado.
```diff
+   if getattr(sys, "frozen", False):
+      static_path = Path(
+         getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
+      )
+
+      bundle = static_path / "reactpy_router-static" / "bundle.js"
+      link_js_content = static_path / "reactpy_router-static" / "link.js"
+   else:
+      static_path = Path(__file__).parent
+
+      bundle = static_path / "static" / "bundle.js"
+      link_js_content = static_path / "static" / "link.js"
+
   History = export(
-      module_from_file("reactpy-router", file=Path(__file__).parent / "static" / "bundle.js"),
+      module_from_file("reactpy-router", file=bundle),
      ("History"),
   )
   """Client-side portion of history handling"""

   Link = export(
-      module_from_file("reactpy-router", file=Path(__file__).parent / "static" / "bundle.js"),
+      module_from_file("reactpy-router", file=bundle),
      ("Link"),
   )
   """Client-side portion of link handling"""

   Navigate = export(
-      module_from_file("reactpy-router", file=Path(__file__).parent / "static" / "bundle.js"),
+      module_from_file("reactpy-router", file=bundle),
      ("Navigate"),
   )
   """Client-side portion of the navigate component"""

   FirstLoad = export(
-      module_from_file("reactpy-router", file=Path(__file__).parent / "static" / "bundle.js"),
+      module_from_file("reactpy-router", file=bundle),
      ("FirstLoad"),
   )

-   link_js_content = (Path(__file__).parent / "static" / "link.js").read_text(encoding="utf-8")
+   link_js_content = (link_js_content).read_text(encoding="utf-8")
```