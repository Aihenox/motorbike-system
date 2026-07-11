import os

from app.repositories.connection import conectar
from datetime import datetime, timedelta

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

    print("Periodo:", periodo)
    print("Fecha inicio:", fecha_inicio)
    print("Fecha fin:", fecha_fin)

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

                "EXTRACT(YEAR FROM fecha) = %s"

            )

            where.append(

                "EXTRACT(MONTH FROM fecha) = %s"

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

        print("\n========== QUERY ==========")
        print(query)
        print("PARAMETROS:", parametros)
        print("===========================\n")

        c.execute(

            query,

            tuple(parametros)

        )

        row = c.fetchone()

        if POSTGRES:

            return {

                "total": row["total"] or 0,

                "motos": row["motos"] or 0,

                "carros": row["carros"] or 0

            }

        return {

            "total": row[0] or 0,

            "motos": row[1] or 0,

            "carros": row[2] or 0

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

                vehiculo

            ORDER BY

                DATE(fecha)

        """
        
        print("\n========== QUERY ==========")
        print(query)
        print("PARAMETROS:", parametros)
        print("===========================\n")

        c.execute(

            query,

            tuple(parametros)

        )

        rows = c.fetchall()

        resultado = []

        for row in rows:

            if POSTGRES:

                resultado.append({

                    "fecha": str(row["fecha"]),

                    "vehiculo": row["vehiculo"],

                    "cantidad": row["cantidad"]

                })

            else:

                resultado.append({

                    "fecha": row[0],

                    "vehiculo": row[1],

                    "cantidad": row[2]

                })
            
        return resultado
    
