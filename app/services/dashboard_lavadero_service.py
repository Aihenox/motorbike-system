from app.repositories.dashboard_lavadero_repository import (

    obtener_resumen_dashboard_db,

    obtener_grafica_dashboard_db

)


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

        "promedio": 0,

        "grafica": grafica

    }