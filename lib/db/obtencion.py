from constantes.db import Sesion
from lib.db.apertura import abrir_db


async def obtener_usuarios() -> list[Sesion]:
    conn, cursor = await abrir_db()
    usuarios = await (
        await cursor.execute("SELECT nombre, rol FROM usuarios")
    ).fetchall()

    await conn.close()

    return list(
        map(lambda usuario: {"usuario": usuario[0], "rol": usuario[1]}, usuarios)
    )


async def obtener_datos_comunidad():
    conn, cursor = await abrir_db(True)
    datos = await (await cursor.execute("SELECT * FROM comunidad")).fetchall()

    await conn.close()

    return [dict(row) for row in datos]
