import os

from app.repositories.connection import conectar
from datetime import datetime, timedelta

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
# CONSTRUIR FILTROS DASHBOARD
# ==========================================
def construir_where_dashboard(
    filtros
):

    operador = "%s" if POSTGRES else "?"

    where = []

    parametros = []

    vehiculos = filtros.get(
        "vehiculos",
        []
    )

    responsables = filtros.get(
        "responsables",
        []
    )

    fecha_inicio = filtros.get(
        "fecha_inicio",
        ""
    )

    fecha_fin = filtros.get(
        "fecha_fin",
        ""
    )

    periodo = filtros.get(
        "periodo",
        "dia"
    )

    # ==========================================
    # VEHICULOS
    # ==========================================
    if vehiculos:

        placeholders = ",".join(

            [operador] * len(vehiculos)

        )

        where.append(

            f"vehiculo IN ({placeholders})"

        )

        parametros.extend(
            vehiculos
        )

    # ==========================================
    # RESPONSABLES
    # ==========================================
    if responsables:

        placeholders = ",".join(

            [operador] * len(responsables)

        )

        where.append(

            f"responsable IN ({placeholders})"

        )

        parametros.extend(
            responsables
        )

    # ==========================================
    # FILTRO POR PERIODO
    # ==========================================

    # --------------------------
    # DIA
    # --------------------------
    if (

        periodo == "dia"

        and fecha_inicio

    ):

        where.append(

            f"DATE(fecha) = {operador}"

        )

        parametros.append(

            fecha_inicio

        )

    # --------------------------
    # SEMANA
    # --------------------------
    elif (

        periodo == "semana"

        and fecha_inicio

    ):

        fecha_fin = datetime.strptime(

            fecha_inicio,

            "%Y-%m-%d"

        )

        fecha_inicio_semana = (

            fecha_fin - timedelta(days=6)

        ).strftime("%Y-%m-%d")

        where.append(

            f"DATE(fecha) BETWEEN {operador} AND {operador}"

        )

        parametros.extend([

            fecha_inicio_semana,

            fecha_fin.strftime("%Y-%m-%d")

        ])

    # --------------------------
    # MES
    # --------------------------
    elif (

        periodo == "mes"

        and fecha_inicio

    ):

        anio = fecha_inicio[:4]

        mes = fecha_inicio[5:7]

        if POSTGRES:

            where.append(

                "EXTRACT(YEAR FROM CAST(fecha AS TIMESTAMP)) = %s"

            )

            where.append(

                "EXTRACT(MONTH FROM CAST(fecha AS TIMESTAMP)) = %s"

            )

        else:

            where.append(

                "strftime('%Y', fecha) = ?"

            )

            where.append(

                "strftime('%m', fecha) = ?"

            )

        parametros.extend([

            anio,

            mes

        ])

    # --------------------------
    # RANGO
    # --------------------------
    elif (

        periodo == "rango"

        and fecha_inicio

        and fecha_fin

    ):

        where.append(

            f"DATE(fecha) BETWEEN {operador} AND {operador}"

        )

        parametros.extend([

            fecha_inicio,

            fecha_fin

        ])
    return where, parametros

# ==========================================
# RESUMEN DASHBOARD
# ==========================================
def obtener_resumen_dashboard_db(
    filtros
):

    with conectar() as conn:

        c = conn.cursor()

        where, parametros = construir_where_dashboard(
            filtros
        )

        
        query = """

            SELECT

                COUNT(*) AS total,

                SUM(

                    CASE

                        WHEN vehiculo='Moto'

                        THEN 1

                        ELSE 0

                    END

                ) AS motos,

                SUM(

                    CASE

                        WHEN vehiculo='Carro'

                        THEN 1

                        ELSE 0

                    END

                ) AS carros

            FROM lavados

            WHERE 1=1

        """

        if where:

            query += " AND "

            query += " AND ".join(

                where

            )

        c.execute(

            query,

            tuple(parametros)

        )

        row = c.fetchone()

        return {

            "total": obtener_campo(
                row,
                0,
                "total"
            ) or 0,

            "motos": obtener_campo(
                row,
                1,
                "motos"
            ) or 0,

            "carros": obtener_campo(
                row,
                2,
                "carros"
            ) or 0

        }
    
# ==========================================
# GRAFICA DASHBOARD
# ==========================================
def obtener_grafica_dashboard_db(
    filtros
):

    with conectar() as conn:

        c = conn.cursor()

        where, parametros = construir_where_dashboard(
            filtros
        )

        query = """

            SELECT

                DATE(fecha) AS fecha,

                vehiculo,

                responsable,

                COUNT(*) AS cantidad

            FROM lavados

            WHERE 1=1

        """

        if where:

            query += " AND "

            query += " AND ".join(
                where
            )

        query += """

            GROUP BY

                DATE(fecha),

                vehiculo,

                responsable

            ORDER BY

                DATE(fecha)

        """
        
        c.execute(

            query,

            tuple(parametros)

        )

        rows = c.fetchall()

        resultado = []

        for row in rows:

            resultado.append({

                "fecha": str(

                    obtener_campo(
                        row,
                        0,
                        "fecha"
                    )

                ),

                "vehiculo": obtener_campo(
                    row,
                    1,
                    "vehiculo"
                ),

                "responsable": obtener_campo(
                    row,
                    2,
                    "responsable"
                ),

                "cantidad": obtener_campo(
                    row,
                    3,
                    "cantidad"
                )

            })
            
        return resultado
    
# ==========================================
# PROXIMOS LAVADOS DE CORTESIA
# ==========================================
def obtener_proximas_cortesias_db():

    with conectar() as conn:

        c = conn.cursor()

        query = """

            SELECT

                placa,

                COUNT(*) AS lavados

            FROM lavados

            GROUP BY placa

            ORDER BY lavados DESC,
                     placa

        """

        c.execute(query)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            lavados = obtener_campo(

                row,

                1,

                "lavados"

            )

            avance = lavados % 5

            if avance == 4:

                resultado.append({

                    "placa": obtener_campo(

                        row,

                        0,

                        "placa"

                    ),

                    "lavados": lavados

                })

        return resultado