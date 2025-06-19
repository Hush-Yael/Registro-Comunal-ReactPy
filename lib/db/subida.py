from constantes.db import DatosUsuario, ErrorDeValidacion
from lib.db.apertura import abrir_db

ERROR_UNICO = "UNIQUE constraint failed"
ERROR_DE_VERIFICACIÓN = "CHECK constraint failed"


async def registrar_usuario(datos: DatosUsuario):
    conn, cursor = await abrir_db()

    cantidad_usuarios = (
        await (
            await cursor.execute("SELECT COUNT(nombre) FROM usuarios LIMIT 1")
        ).fetchone()
        or []
    )
    cantidad_usuarios = cantidad_usuarios[0]

    try:
        await cursor.execute(
            "INSERT INTO usuarios (nombre, contraseña, rol) VALUES (?, ?, ?)",
            (
                datos["nombre"],
                datos["contraseña"],
                # solo el primero usuario es admin, los demás son supervisores
                "admin" if cantidad_usuarios < 1 else "supervisor",
            ),
        )

        await conn.commit()
    except Exception as e:
        print(e)
        error = e.args[0]

        # el único campo único es el nombre
        if ERROR_UNICO in error:
            raise ErrorDeValidacion(
                {
                    "motivo": "nombre-ya-existe",
                    "mensaje": "Ya existe un usuario con ese nombre",
                }
            )
        # errores de integridad de datos
        elif ERROR_DE_VERIFICACIÓN in error:
            if "nombre" in error:
                raise ErrorDeValidacion(
                    {
                        "motivo": "nombre-corto",
                        "mensaje": "El nombre debe tener al menos 3 caracteres, sin espacios a la izquierda ni a la derecha",
                    }
                )
            elif "contraseña" in error:
                raise ErrorDeValidacion(
                    {
                        "motivo": "contraseña-corta",
                        "mensaje": "La contraseña debe tener al menos 6 caracteres, sin espacios a la izquierda ni a la derecha",
                    }
                )
        else:
            raise e
    finally:
        await conn.close()


async def iniciar_sesion(datos: DatosUsuario) -> str:
    conn, cursor = await abrir_db()

    datos_db = (
        await (
            await cursor.execute(
                "SELECT contraseña, rol FROM usuarios WHERE nombre = ? LIMIT 1",
                (datos["nombre"],),
            )
        ).fetchone()
        or ()
    )

    await conn.close()

    if len(datos_db) == 0:
        raise ErrorDeValidacion(
            {
                "motivo": "no-encontrado",
                "mensaje": "No existe un usuario con los datos ingresados",
            }
        )

    if datos_db[0] != datos["contraseña"]:
        raise ErrorDeValidacion(
            {
                "motivo": "contraseña-incorrecta",
                "mensaje": "La contraseña ingresada es incorrecta",
            }
        )

    return datos_db[1]
