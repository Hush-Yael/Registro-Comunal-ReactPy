from constantes.db import Sesion
from lib.db.apertura import abrir_db


async def cambiar_rol(datos: Sesion):
    conn, cursor = await abrir_db()

    await cursor.execute(
        "UPDATE usuarios SET rol = ? WHERE nombre = ?",
        (datos["rol"], datos["usuario"]),
    )

    await conn.commit()
    await conn.close()
    return


async def eliminar_usuario(usuario: str):
    conn, cursor = await abrir_db()

    await cursor.execute(
        "DELETE FROM usuarios WHERE nombre = ?",
        (usuario,),
    )

    await conn.commit()
    await conn.close()
