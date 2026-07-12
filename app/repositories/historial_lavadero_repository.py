import os

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
# CONSTRUIR FILTROS HISTORIAL
# ==========================================
def construir_filtros_historial(

    placa,

    fecha_inicio,

    fecha_fin,

    responsable

):

    operador = "%s" if POSTGRES else "?"

    filtros = ""

    parametros = []

    # ==========================================
    # PLACA
    # ==========================================
    if placa:

        filtros += f"""

            AND placa LIKE {operador}

        """

        parametros.append(

            f"%{placa}%"

        )

    # ==========================================
    # RESPONSABLE
    # ==========================================
    if responsable:

        filtros += f"""

            AND responsable LIKE {operador}

        """

        parametros.append(

            f"%{responsable}%"

        )

    # ==========================================
    # FECHAS
    # ==========================================
    if fecha_inicio and fecha_fin:

        filtros += f"""

            AND DATE(fecha)

            BETWEEN {operador}

            AND {operador}

        """

        parametros.extend([

            fecha_inicio,

            fecha_fin

        ])

    elif fecha_inicio:

        filtros += f"""

            AND DATE(fecha)

            = {operador}

        """

        parametros.append(

            fecha_inicio

        )

    return filtros, parametros


# ==========================================
# LISTAR HISTORIAL LAVADERO
# ==========================================
def obtener_historial_lavadero_db(

    placa="",

    fecha_inicio="",

    fecha_fin="",

    responsable=""
):

    with conectar() as conn:

        c = conn.cursor()

        operador = "%s" if POSTGRES else "?"

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

            WHERE 1=1

        """

        filtros, parametros = construir_filtros_historial(

            placa,

            fecha_inicio,

            fecha_fin,

            responsable

        )

        query += filtros

        query += """

            ORDER BY id DESC

        """

        c.execute(
            query,
            tuple(parametros)
        )

        return c.fetchall()


# ==========================================
# TOTAL LAVADERO
# ==========================================
def obtener_total_lavadero_db(

    placa="",

    fecha_inicio="",

    fecha_fin="",

    responsable=""

):

    with conectar() as conn:

        c = conn.cursor()

        query = """

            SELECT

                COALESCE(

                    SUM(valor),

                    0

                ) AS total

            FROM lavados

            WHERE 1=1

        """

        # ==========================================
        # FILTROS
        # ==========================================
        filtros, parametros = construir_filtros_historial(

            placa,

            fecha_inicio,

            fecha_fin,

            responsable

        )

        query += filtros

        # ==========================================
        # SIN FILTROS
        # ==========================================
        if (

            not fecha_inicio

            and not fecha_fin

            and not placa

            and not responsable

        ):

            operador = "%s" if POSTGRES else "?"

            query += f"""

                AND DATE(fecha)
                = {operador}

            """

            from datetime import date

            parametros.append(

                date.today().isoformat()

            )

        c.execute(

            query,

            tuple(parametros)

        )

        row = c.fetchone()

        return obtener_campo(

            row,

            0,

            "total"

        ) or 0