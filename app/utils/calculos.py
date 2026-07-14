from datetime import datetime
from zoneinfo import ZoneInfo

from app.utils.date_utils import (
    asegurar_zona_colombia,
    parsear_fecha
)

from app.services.tarifas_service import (
    obtener_tarifa_activa
)

from datetime import (
    datetime,
    timedelta,
    time
)

# ==========================================
# CALCULAR HORAS COBRO
# ==========================================
def calcular_horas_cobro(

    minutos,

    minutos_gracia

):

    horas = minutos // 60

    minutos_restantes = minutos % 60

    if minutos_restantes > minutos_gracia:

        horas += 1

    if horas <= 0:

        horas = 1

    return horas

# ==========================================
# CALCULAR TRAMOS PARQUEADERO
# ==========================================
def calcular_tramos(

    hora_ingreso,

    hora_salida,

    minutos_gracia

):

    paso_medianoche = (

        hora_salida.date()

        >

        hora_ingreso.date()

    )

    horas_antes = 0

    # ==========================================
    # HORAS ANTES DE LA NOCHE
    # ==========================================
    if paso_medianoche:

        inicio_noche = datetime.combine(

            hora_ingreso.date(),

            time(19, 0),

            tzinfo=hora_ingreso.tzinfo

        )

        # Solo si ingresó antes de las 7 pm
        if hora_ingreso < inicio_noche:

            diferencia = inicio_noche - hora_ingreso

            minutos = int(

                diferencia.total_seconds() // 60

            )

            horas_antes = calcular_horas_cobro(

                minutos,

                minutos_gracia

            )

    # ==========================================
    # HORAS DESPUES DE LA NOCHE
    # ==========================================
    horas_despues = 0

    if paso_medianoche:

        fin_noche = datetime.combine(

            hora_salida.date(),

            time(8, 0),

            tzinfo=hora_salida.tzinfo

        )

        # Solo si salió después de las 8:00 am
        if hora_salida > fin_noche:

            diferencia = hora_salida - fin_noche

            minutos = int(

                diferencia.total_seconds() // 60

            )

            horas_despues = calcular_horas_cobro(

                minutos,

                minutos_gracia

            )

    return {

        "paso_medianoche": paso_medianoche,

        "horas_antes": horas_antes,

        "noches": 1 if paso_medianoche else 0,

        "horas_despues": 0

    }

# ==========================================
# CALCULAR VALOR PARQUEADERO
# ==========================================
def calcular_valor(
    tipo,
    hora_ingreso,
    ahora=None
):

    hora_ingreso = asegurar_zona_colombia(
        parsear_fecha(
            hora_ingreso
        )
    )

    if ahora is None:

        ahora = datetime.now(
            ZoneInfo("America/Bogota")
        )

    ahora = asegurar_zona_colombia(
        ahora
    )

    diferencia = ahora - hora_ingreso

    total_segundos = int(
        diferencia.total_seconds()
    )

    if total_segundos < 0:

        raise ValueError(
            "La hora de ingreso no puede estar en el futuro"
        )

    total_minutos = total_segundos // 60

    horas = total_minutos // 60

    minutos = total_minutos % 60

    # ==========================================
    # CONFIGURACION
    # ==========================================
    tarifas = obtener_tarifa_activa()

    if not tarifas:

        raise RuntimeError(
            "No existe una configuración de tarifas activa"
        )

    
    minutos_gracia = tarifas.get(
        "minutos_gracia",
        10
    )

    # ==========================================
    # CALCULAR TRAMOS
    # ==========================================
    tramos = calcular_tramos(

        hora_ingreso,

        ahora,

        minutos_gracia

    )

    horas_cobro = horas

    if minutos > minutos_gracia:

        horas_cobro += 1

    if horas_cobro <= 0:

        horas_cobro = 1

    # ==========================================
    # TARIFA SEGUN VEHICULO
    # ==========================================
    if tipo == "Moto":

        tarifa_hora = tarifas.get(

            "hora_moto",

            1500

        )

        tarifa_noche = tarifas.get(

            "noche_moto",

            0

        )

    elif tipo == "Carro":

        tarifa_hora = tarifas.get(

            "hora_carro",

            3000

        )

        tarifa_noche = tarifas.get(

            "noche_carro",

            0

        )

    else:

        raise ValueError(

            "Tipo de vehículo inválido"

        )

    # ==========================================
    # CALCULO TOTAL
    # ==========================================
    if tramos["paso_medianoche"]:

        total = (

            tramos["horas_antes"] * tarifa_hora

            +

            tramos["noches"] * tarifa_noche

            +

            tramos["horas_despues"] * tarifa_hora

        )

    else:

        total = horas_cobro * tarifa_hora

    return total, ahora
