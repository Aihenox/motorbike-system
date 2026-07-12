import os

from datetime import datetime
from zoneinfo import ZoneInfo

from app.repositories.connection import conectar

from app.repositories.database_utils import (
    obtener_campo
)

# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)

# ==========================================
# REGISTRAR LAVADO
# ==========================================
def registrar_lavado_db(

    placa,

    vehiculo,

    tipo_lavado,

    valor,

    responsable,

    fecha
):

    with conectar() as conn:

        c = conn.cursor()

        # ==========================================
        # POSTGRESQL
        # ==========================================
        if POSTGRES:

            c.execute("""

                INSERT INTO lavados (

                    placa,
                    vehiculo,
                    tipo_lavado,
                    valor,
                    responsable,
                    fecha

                )

                VALUES (

                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s

                )

            """, (

                placa.upper(),

                vehiculo,

                tipo_lavado,

                valor,

                responsable,

                fecha
            ))

        # ==========================================
        # SQLITE
        # ==========================================
        else:

            c.execute("""

                INSERT INTO lavados (

                    placa,
                    vehiculo,
                    tipo_lavado,
                    valor,
                    responsable,
                    fecha

                )

                VALUES (

                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?

                )

            """, (

                placa.upper(),

                vehiculo,

                tipo_lavado,

                valor,

                responsable,

                fecha
            ))

        conn.commit()


# ==========================================
# OBTENER LAVADOS
# ==========================================
def obtener_lavados_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT
                id,
                placa,
                vehiculo,
                tipo_lavado,
                valor,
                responsable,
                fecha

            FROM lavados

            ORDER BY id DESC

        """)

        return c.fetchall()
    

# ==========================================
# HISTORIAL LAVADOS
# ==========================================
def obtener_historial_lavados_db(

    placa="",

    fecha_inicio="",

    fecha_fin="",

    responsable=""
):

    with conectar() as conn:

        c = conn.cursor()

        condiciones = []

        valores = []

        operador = "%s" if POSTGRES else "?"

        # ==========================================
        # FILTRO PLACA
        # ==========================================
        if placa:

            condiciones.append(
                f"placa LIKE {operador}"
            )

            valores.append(
                f"%{placa.upper()}%"
            )

        # ==========================================
        # FECHA INICIAL Y FINAL
        # ==========================================
        if fecha_inicio and fecha_fin:

            condiciones.append(
                f"DATE(fecha) BETWEEN {operador} AND {operador}"
            )

            valores.extend([
                fecha_inicio,
                fecha_fin
            ])

        elif fecha_inicio:

            condiciones.append(
                f"DATE(fecha) = {operador}"
            )

            valores.append(
                fecha_inicio
            )

        # ==========================================
        # FILTRO RESPONSABLE
        # ==========================================
        if responsable:

            condiciones.append(
                f"responsable = {operador}"
            )

            valores.append(
                responsable
            )

        query = """

            SELECT
                id,
                placa,
                vehiculo,
                tipo_lavado,
                valor,
                responsable,
                fecha

            FROM lavados

        """

        if condiciones:

            query += " WHERE " + " AND ".join(
                condiciones
            )

        query += """

            ORDER BY id DESC

        """

        c.execute(
            query,
            tuple(valores)
        )

        return c.fetchall()


# ==========================================
# METRICAS LAVADERO
# ==========================================
def obtener_metricas_lavadero_db():

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now(
            ZoneInfo(
                "America/Bogota"
        )
        ).strftime(
            "%Y-%m-%d"
        )

        operador = "%s" if POSTGRES else "?"

        c.execute(f"""

            SELECT

                COUNT(
                    CASE
                        WHEN vehiculo = 'Moto'
                        THEN 1
                    END
                ) as motos,

                COUNT(
                    CASE
                        WHEN vehiculo = 'Carro'
                        THEN 1
                    END
                ) as carros,

                COALESCE(
                    SUM(valor),
                    0
                ) as total

            FROM lavados

            WHERE fecha LIKE {operador}

        """, (
            f"{hoy}%",
        ))

        row = c.fetchone()

        motos = obtener_campo(
            row,
            0,
            "motos"
        )

        carros = obtener_campo(
            row,
            1,
            "carros"
        )

        total = obtener_campo(
            row,
            2,
            "total"
        )

        return {

            "lavados_motos":
                motos,

            "lavados_carros":
                carros,

            "total_lavados":
                motos + carros,

            "dinero_generado":
                total
        }
    
    
# ==========================================
# ULTIMOS LAVADOS
# ==========================================
def obtener_ultimos_lavados_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT
                id,
                placa,
                vehiculo,
                tipo_lavado,
                valor,
                responsable,
                fecha

            FROM lavados

            ORDER BY id DESC

            LIMIT 10

        """)

        return c.fetchall()


# ==========================================
# ESTADISTICAS RESPONSABLES
# ==========================================
def obtener_estadisticas_responsables_db():

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now(
            ZoneInfo(
                "America/Bogota"
        )
        ).strftime(
            "%Y-%m-%d"
        )

        operador = "%s" if POSTGRES else "?"

        c.execute(f"""

            SELECT

                responsable,

                COUNT(*) as cantidad,

                COALESCE(
                    SUM(valor),
                    0
                ) as total

            FROM lavados

            WHERE fecha LIKE {operador}

            GROUP BY responsable

            ORDER BY total DESC

        """, (
            f"{hoy}%",
        ))

        rows = c.fetchall()

        resultado = []

        for row in rows:

            resultado.append({

                "responsable": obtener_campo(
                    row,
                    0,
                    "responsable"
                ),

                "cantidad": obtener_campo(
                    row,
                    1,
                    "cantidad"
                ),

                "total": obtener_campo(
                    row,
                    2,
                    "total"
                )

            })

        return resultado
    

# ==========================================
# OBTENER LAVADO POR ID
# ==========================================
def obtener_lavado_por_id_db(
    lavado_id
):

    with conectar() as conn:

        c = conn.cursor()

        operador = "%s" if POSTGRES else "?"

        c.execute(f"""

            SELECT
                id,
                placa,
                vehiculo,
                tipo_lavado,
                valor,
                responsable,
                fecha

            FROM lavados

            WHERE id = {operador}

        """, (
            lavado_id,
        ))

        return c.fetchone()


# ==========================================
# ACTUALIZAR LAVADO
# ==========================================
def actualizar_lavado_db(

    lavado_id,

    placa,

    vehiculo,

    tipo_lavado,

    valor,

    responsable
):

    with conectar() as conn:

        c = conn.cursor()

        operador = "%s" if POSTGRES else "?"

        c.execute(f"""

            UPDATE lavados

            SET

                placa = {operador},
                vehiculo = {operador},
                tipo_lavado = {operador},
                valor = {operador},
                responsable = {operador}

            WHERE id = {operador}

        """, (

            placa.upper(),

            vehiculo,

            tipo_lavado,

            valor,

            responsable,

            lavado_id
        ))

        conn.commit()

# ==========================================
# ELIMINAR LAVADO
# ==========================================
def eliminar_lavado_db(
    lavado_id
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                DELETE FROM lavados

                WHERE id = %s

            """, (
                lavado_id,
            ))

        else:

            c.execute("""

                DELETE FROM lavados

                WHERE id = ?

            """, (
                lavado_id,
            ))

        conn.commit()

# ==========================================
# CONTAR LAVADOS POR PLACA
# ==========================================
def contar_lavados_placa_db(
    placa
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT COUNT(*)

                FROM lavados

                WHERE placa = %s

            """, (
                placa.upper(),
            ))

        else:

            c.execute("""

                SELECT COUNT(*)

                FROM lavados

                WHERE placa = ?

            """, (
                placa.upper(),
            ))

        resultado = c.fetchone()

        if resultado is None:

            return 0

        if resultado is None:

            return 0

        return obtener_campo(
            resultado,
            0,
            "count"
        )