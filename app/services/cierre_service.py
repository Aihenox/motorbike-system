from app.repositories.cierre_repository import (

    obtener_metricas_cierre_db,

    guardar_cierre_db,

    obtener_pago_lavadores_db

)

from app.services.gastos_service import (

    obtener_gastos_dia,

    obtener_total_gastos

)

from datetime import datetime

from zoneinfo import ZoneInfo

# ==========================================
# OBTENER MÉTRICAS
# ==========================================
def obtener_metricas_cierre():

    metricas = obtener_metricas_cierre_db()

    hoy = datetime.now(

        ZoneInfo("America/Bogota")

    ).strftime(

        "%Y-%m-%d"

    )

    gastos = obtener_gastos_dia(

        hoy

    )

    total_gastos = obtener_total_gastos(

        hoy

    )

    pagos_lavadores, total_pago_lavadores = (

        obtener_pago_lavadores_db()

    )

    metricas["gastos"] = gastos

    metricas["total_gastos"] = total_gastos

    metricas["detalle_egresos"]["gastos"] = total_gastos

    metricas["pagos_lavadores"] = pagos_lavadores

    metricas["total_pago_lavadores"] = total_pago_lavadores

    # Los egresos incluyen gastos y pago de lavadores
    metricas["egresos_dia"] = (

        total_gastos

        + total_pago_lavadores

    )

    # Recalcular el saldo actual
    metricas["saldo_actual"] = (

        metricas["saldo_inicial"]

        + metricas["ingresos_dia"]

        - metricas["egresos_dia"]

    )

    # Compatibilidad temporal con la vista actual
    metricas["dinero_esperado"] = metricas["saldo_actual"]

    metricas["utilidad"] = metricas["saldo_actual"]

    return metricas

# ==========================================
# GUARDAR CIERRE
# ==========================================
def guardar_cierre(

    fecha,

    total_parqueadero,

    total_lavadero,

    observaciones,

    usuario,

    hora_cierre

):

    total_parqueadero = int(
        total_parqueadero
    )

    total_lavadero = int(
        total_lavadero
    )

    if total_parqueadero < 0 or total_lavadero < 0:

        raise ValueError(
            "Los totales del cierre no pueden ser negativos"
        )

    metricas = obtener_metricas_cierre_db()

    saldo_inicial = metricas["saldo_inicial"]

    ingresos_dia = metricas["ingresos_dia"]

    hoy = datetime.now(

        ZoneInfo("America/Bogota")

    ).strftime("%Y-%m-%d")

    egresos_dia = (

        obtener_total_gastos(hoy)

        +

        obtener_pago_lavadores_db()[1]

    )

    saldo_final = (

        saldo_inicial

        +

        ingresos_dia

        -

        egresos_dia

    )

    observaciones = (
        observaciones or ""
    ).strip()

    if len(observaciones) > 500:

        raise ValueError(
            "Las observaciones no pueden superar 500 caracteres"
        )

    total_general = total_parqueadero + total_lavadero
    guardar_cierre_db(

        fecha,

        saldo_inicial,

        ingresos_dia,

        egresos_dia,

        saldo_final,

        total_parqueadero,

        total_lavadero,

        total_general,

        observaciones,

        usuario,

        hora_cierre

    )

# ==========================================
# HISTORIAL CIERRES
# ==========================================
from app.repositories.cierre_repository import (
    obtener_historial_cierres_db
)


def obtener_historial_cierres():

    return obtener_historial_cierres_db()
