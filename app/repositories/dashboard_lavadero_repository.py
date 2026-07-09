import os

from app.repositories.connection import conectar


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
    # FECHAS
    # ==========================================
    if (

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

    elif (

        periodo == "rango"

        and fecha_inicio

    ):

        where.append(

            f"DATE(fecha) = {operador}"

        )

        parametros.append(

            fecha_inicio

        )
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

        grupo = construir_group_dashboard(
            filtros
        )

        query = f"""

            SELECT

                {grupo["campo"]} AS fecha,

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

        query += f"""

            GROUP BY

                {grupo["campo"]},

                vehiculo

            ORDER BY

                {grupo["campo"]}

        """
        
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
    
# ==========================================
# AGRUPAR DASHBOARD
# ==========================================
def construir_group_dashboard(
    filtros
):

    periodo = filtros.get(
        "periodo",
        "dia"
    )

    # ==========================================
    # DIA Y RANGO
    # ==========================================
    if periodo in (
        "dia",
        "rango"
    ):

        return {

            "campo": "DATE(fecha)"

        }

    # ==========================================
    # SEMANA
    # ==========================================
    elif periodo == "semana":

        return {

            "campo": "strftime('%Y-%W', fecha)"

        }

    # ==========================================
    # MES
    # ==========================================
    elif periodo == "mes":

        return {

            "campo": "strftime('%Y-%m', fecha)"

        }

    return {

        "campo": "DATE(fecha)"

    }