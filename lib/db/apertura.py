import aiosqlite
from constantes.db import NOMBRE_MÍNIMO, CONTRASEÑA_MÍNIMA


def nombres_check(nombre_columna: str):
    return f"CHECK(length(trim({nombre_columna})) >= {NOMBRE_MÍNIMO})"


async def abrir_db():
    conn = await aiosqlite.connect("db/comunidad.db")
    cursor = await conn.cursor()

    await cursor.execute(f"""--sql
        CREATE TABLE IF NOT EXISTS usuarios(
            nombre TEXT PRIMARY KEY NOT NULL UNIQUE {nombres_check("nombre")},
            rol TEXT NOT NULL CHECK(rol in ('admin', 'supervisor')),
            contraseña TEXT NOT NULL CHECK(length(trim(contraseña)) >= {CONTRASEÑA_MÍNIMA})
        )
    """)

    await cursor.execute(f"""--sql
        CREATE TABLE IF NOT EXISTS comunidad (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT NOT NULL {nombres_check("nombres")},
            apellidos TEXT NOT NULL {nombres_check("apellidos")},
            cedula INTEGER NOT NULL UNIQUE CHECK(cedula > 0),
            fecha_nacimiento TEXT,
            patologia TEXT,
            numero_casa INTEGER
        )
    """)
    return (conn, cursor)
