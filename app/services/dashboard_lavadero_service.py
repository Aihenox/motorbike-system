from app.repositories.dashboard_lavadero_repository import (

    obtener_resumen_dashboard_db,

    obtener_grafica_dashboard_db,

    obtener_proximas_cortesias_db

)

from datetime import datetime, timedelta
import calendar


# ==========================================
# DASHBOARD COMPLETO
# ==========================================
def obtener_dashboard(

    filtros

):

    resumen = obtener_resumen_dashboard_db(

        filtros

    )

    grafica = obtener_grafica_dashboard_db(

        filtros

    )

    return {

        "total": resumen["total"],

        "motos": resumen["motos"],

        "carros": resumen["carros"],

        "promedio": calcular_promedio(

            resumen["total"],

            filtros

        ),

        "grafica": grafica,

    }

# ==========================================
# CALCULAR PROMEDIO
# ==========================================
def calcular_promedio(
    total,
    filtros
):

    periodo = filtros.get(
        "periodo",
        "dia"
    )

    fecha_inicio = filtros.get(
        "fecha_inicio",
        ""
    )

    fecha_fin = filtros.get(
        "fecha_fin",
        ""
    )

    dias = 1

    # ==========================================
    # DIA
    # ==========================================
    if periodo == "dia":

        dias = 1

    # ==========================================
    # SEMANA
    # ==========================================
    elif periodo == "semana":

        dias = 7

    # ==========================================
    # MES
    # ==========================================
    elif periodo == "mes" and fecha_inicio:

        fecha = datetime.strptime(
            fecha_inicio,
            "%Y-%m-%d"
        )

        dias = calendar.monthrange(
            fecha.year,
            fecha.month
        )[1]

    # ==========================================
    # RANGO
    # ==========================================
    elif (

        periodo == "rango"

        and fecha_inicio

        and fecha_fin

    ):

        inicio = datetime.strptime(
            fecha_inicio,
            "%Y-%m-%d"
        )

        fin = datetime.strptime(
            fecha_fin,
            "%Y-%m-%d"
        )

        dias = (fin - inicio).days + 1

    if dias <= 0:

        dias = 1

    return round(

        total / dias,

        2

    )

# ==========================================
# PROXIMAS CORTESIAS
# ==========================================
def obtener_proximas_cortesias():

    cortesias = obtener_proximas_cortesias_db()

    resultado = []

    for item in cortesias:

        lavados_totales = item["lavados"]

        avance = lavados_totales % 5

        if avance == 0:

            avance = 5

        resultado.append({

            "placa": item["placa"],

            "lavados_totales": lavados_totales,

            "avance": avance,

            "faltan": 5 - avance,

            "progreso": round(

                (avance / 5) * 100

            )

        })

    return resultado