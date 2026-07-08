from app.repositories.ingreso_repository import (
    obtener_ticket_activo_db,
    cerrar_ticket_db
)

from app.services.tarifas_service import (
    obtener_tarifa_activa
)

from app.utils.calculos import (
    calcular_valor
)

from app.utils.date_utils import (
    asegurar_zona_colombia,
    parsear_fecha
)


# ==========================================
# PROCESAR SALIDA
# ==========================================
def procesar_salida(ticket):

    data = obtener_ticket_activo_db(
        ticket
    )

    if not data:

        return {

            "success": False,

            "message": "Ticket inválido"
        }

    tipo = data["tipo"]

    placa = data["placa"]

    hora_ingreso = data["hora_ingreso"]

    ingreso_dt = asegurar_zona_colombia(
        parsear_fecha(
            hora_ingreso
        )
    )


    # ==========================================
    # CALCULAR VALOR SEGUN MODALIDAD
    # ==========================================
    try:

        modalidad = data["modalidad"]

    except Exception:

        modalidad = "Hora"

    tarifas = obtener_tarifa_activa()
    
    if modalidad == "Hora":

        valor, hora_salida = calcular_valor(

            tipo,

            ingreso_dt.isoformat()
        )

    else:

        from datetime import datetime
        from zoneinfo import ZoneInfo

        hora_salida = datetime.now(
            ZoneInfo("America/Bogota")
        )

        if modalidad == "Noche":

            from datetime import time
            
            # ==========================
            # TARIFA NOCHE BASE
            # ==========================
            if tipo == "Moto":

                valor = tarifas["noche_moto"]

                tarifa_hora = tarifas["hora_moto"]

            else:

                valor = tarifas["noche_carro"]

                tarifa_hora = tarifas["hora_carro"]

            # ==========================
            # DESPUES DE LAS 8:10 AM DEL DIA SIGUIENTE
            # ==========================
            from datetime import timedelta

            limite = ingreso_dt.replace(

                hour=8,

                minute=10,

                second=0,

                microsecond=0

            ) + timedelta(days=1)

            if hora_salida > limite:

                diferencia = hora_salida - limite

                minutos = int(

                    diferencia.total_seconds()

                    / 60
                )

                horas = minutos // 60

                minutos_restantes = minutos % 60

                horas_extra = horas

                minutos_gracia = tarifas.get(

                    "minutos_gracia",

                    10
                )

                if minutos_restantes > minutos_gracia:

                    horas_extra += 1

                if horas_extra <= 0:

                    horas_extra = 1

                valor += horas_extra * tarifa_hora

        else:

            valor = 0
            
    # ==========================================
    # ASEGURAR TZ EN SALIDA
    # ==========================================
    hora_salida = asegurar_zona_colombia(
        hora_salida
    )

    # ==========================================
    # DIFERENCIA TIEMPO
    # ==========================================
    diferencia = hora_salida - ingreso_dt

    dias = diferencia.days

    horas = diferencia.seconds // 3600

    minutos = (
        diferencia.seconds % 3600
    ) // 60

    tiempo = ""

    if dias > 0:

        tiempo += f"{dias}d "

    tiempo += f"{horas:02d}:{minutos:02d}"

    # ==========================================
    # CERRAR TICKET
    # ==========================================
    #cerrar_ticket_db(

        #ticket,

        #hora_salida.isoformat(),

        #valor
    #)

    return {

        "success": True,

        "ticket": ticket,

        "placa": placa,

        "tipo": tipo,

        "hora_ingreso": ingreso_dt.strftime(
            "%d/%m/%Y %I:%M %p"
        ),

        "hora_salida": hora_salida.strftime(
            "%d/%m/%Y %I:%M %p"
        ),

        "tiempo": tiempo,

        "valor": valor,

        "hora_salida_iso":
            hora_salida.isoformat()
    }

# ==========================================
# CONFIRMAR SALIDA
# ==========================================
def confirmar_salida(

    ticket

):

    salida = procesar_salida(
        ticket
    )

    if not salida["success"]:

        return salida

    actualizado = cerrar_ticket_db(

        ticket,

        salida["hora_salida_iso"],

        salida["valor"]

    )

    if not actualizado:

        raise ValueError(
            "El ticket ya fue procesado o no está activo"
        )

    return {

        "success": True,

        "valor": salida["valor"],

        "hora_salida": salida["hora_salida"]

    }
