from constantes.db import DatosComunidad, DatosUsuario, ErrorDeValidacion
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
                        "mensaje": "El nombre debe tener al menos 3 caracteres, sin espacios a los lados",
                    }
                )
            elif "contraseña" in error:
                raise ErrorDeValidacion(
                    {
                        "motivo": "contraseña-corta",
                        "mensaje": "La contraseña debe tener al menos 6 caracteres, sin espacios a los lados",
                    }
                )
        # error desconocido, no debería pasar
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


async def verificar_cedula_existente(cedula: int):
    conn, cursor = await abrir_db()

    cedula_db = (
        await (
            await cursor.execute(
                "SELECT cedula FROM comunidad WHERE cedula = ? LIMIT 1",
                (cedula,),
            )
        ).fetchone()
        or ()
    )

    await conn.close()

    if len(cedula_db) > 0:
        raise ErrorDeValidacion(
            {
                "motivo": "cedula-ya-existente",
                "mensaje": "Ya existe un registro con esa cédula",
            }
        )


async def añadir_datos_comunidad(datos: DatosComunidad):
    conn, cursor = await abrir_db()

    try:
        await cursor.execute(
            "INSERT INTO comunidad (nombres, apellidos, cedula, fecha_nacimiento, patologia, numero_casa) VALUES (?, ?, ?, ?, ?, ?)",
            (
                datos["nombres"],
                datos["apellidos"],
                datos["cedula"],
                datos["fecha_nacimiento"],
                datos["patologia"],
                datos["numero_casa"],
            ),
        )
        await conn.commit()
    except Exception as e:
        error = e.args[0]

        # el único campo único es la cédula
        if ERROR_UNICO in error:
            raise ErrorDeValidacion(
                {
                    "motivo": "cedula-ya-existente",
                    "mensaje": "Ya existe un registro con esa cédula",
                }
            )

        # errores de integridad de datos
        elif ERROR_DE_VERIFICACIÓN in error:
            if "nombre" in error or "apellidos" in error:
                str = "nombres" if "nombre" in error else "apellidos"

                raise ErrorDeValidacion(
                    {
                        "motivo": str + "-cortos",
                        "mensaje": f"Los {str} deben tener al menos 3 caracteres, sin espacios a los lados",
                    }
                )
            elif "cedula" in error:
                raise ErrorDeValidacion(
                    {
                        "motivo": "cedula-corta",
                        "mensaje": "La cédula debe ser mayor a 0",
                    }
                )
            # error desconocido, no debería pasar
            else:
                raise e
        # error desconocido, no debería pasar
        else:
            raise e
        return
    finally:
        await conn.close()
