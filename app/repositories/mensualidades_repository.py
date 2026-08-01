import os

from app.repositories.connection import conectar


POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# LISTAR MENSUALIDADES
# ==========================================
def obtener_mensualidades_db():


    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT

                id,
                placa,
                tipo,
                propietario,
                telefono,
                fecha_inicio,
                fecha_fin,
                estado

            FROM mensualidades

            ORDER BY placa

        """)

        return c.fetchall()
    
# ==========================================
# CREAR MENSUALIDAD
# ==========================================
def crear_mensualidad_db(

    placa,

    tipo,

    propietario,

    telefono,

    fecha_inicio,

    fecha_fin,

    estado
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                INSERT INTO mensualidades(

                    placa,
                    tipo,
                    propietario,
                    telefono,
                    fecha_inicio,
                    fecha_fin,
                    estado

                )

                VALUES(

                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s

                )

                RETURNING id

            """, (

                placa.upper(),
                tipo,
                propietario,
                telefono,
                fecha_inicio,
                fecha_fin,
                estado

            ))

            id_mensualidad = c.fetchone()["id"]

            conn.commit()

            return id_mensualidad

        else:

            c.execute("""

                INSERT INTO mensualidades(

                    placa,
                    tipo,
                    propietario,
                    telefono,
                    fecha_inicio,
                    fecha_fin,
                    estado

                )

                VALUES (?, ?, ?, ?, ?, ?, ?)

            """, (

                placa.upper(),
                tipo,
                propietario,
                telefono,
                fecha_inicio,
                fecha_fin,
                estado

            ))

            conn.commit()

            return c.lastrowid

# ==========================================
# OBTENER MENSUALIDAD
# ==========================================
def obtener_mensualidad_db(id):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT *

                FROM mensualidades

                WHERE id = %s

            """, (
                id,
            ))

        else:

            c.execute("""

                SELECT *

                FROM mensualidades

                WHERE id = ?

            """, (
                id,
            ))

        return c.fetchone()


# ==========================================
# ACTUALIZAR MENSUALIDAD
# ==========================================
def actualizar_mensualidad_db(

    id,

    placa,

    tipo,

    propietario,

    telefono,

    fecha_inicio,

    fecha_fin,

    estado
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                UPDATE mensualidades

                SET

                    placa = %s,
                    tipo = %s,
                    propietario = %s,
                    telefono = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    estado = %s

                WHERE id = %s

            """, (

                placa.upper(),

                tipo,

                propietario,

                telefono,

                fecha_inicio,

                fecha_fin,

                estado,

                id
            ))

        else:

            c.execute("""

                UPDATE mensualidades

                SET

                    placa = ?,
                    tipo = ?,
                    propietario = ?,
                    telefono = ?,
                    fecha_inicio = ?,
                    fecha_fin = ?,
                    estado = ?

                WHERE id = ?

            """, (

                placa.upper(),

                tipo,

                propietario,

                telefono,

                fecha_inicio,

                fecha_fin,

                estado,

                id
            ))

        conn.commit()

# ==========================================
# ELIMINAR MENSUALIDAD
# ==========================================
def eliminar_mensualidad_db(id):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                DELETE FROM mensualidades

                WHERE id = %s

            """, (
                id,
            ))

        else:

            c.execute("""

                DELETE FROM mensualidades

                WHERE id = ?

            """, (
                id,
            ))

        conn.commit()

# ==========================================
# BUSCAR MENSUALIDAD ACTIVA
# ==========================================
def buscar_mensualidad_activa_db(
    placa,
    hoy
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT *

                FROM mensualidades

                WHERE placa = %s
                AND estado = 'Activa'
                AND fecha_inicio <= %s
                AND fecha_fin >= %s

                ORDER BY fecha_fin DESC
                LIMIT 1

            """, (
                placa.upper(),
                hoy,
                hoy
            ))

        else:

            c.execute("""

                SELECT *

                FROM mensualidades

                WHERE placa = ?
                AND estado = 'Activa'
                AND fecha_inicio <= ?
                AND fecha_fin >= ?

                ORDER BY fecha_fin DESC
                LIMIT 1

            """, (
                placa.upper(),
                hoy,
                hoy
            ))

        return c.fetchone()
