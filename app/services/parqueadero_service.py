from datetime import datetime

from flask import current_app

from zoneinfo import ZoneInfo

from app.repositories.ingreso_repository import (
    placa_activa_db,
    insertar_ingreso_db,
    puesto_casco_ocupado_db
)

from app.repositories.activos_repository import (
    obtener_vehiculo_db,
    actualizar_vehiculo_db,
    eliminar_vehiculo_db
)

from app.utils.validators import (
    validar_placa,
    validar_tipo_vehiculo
)

from app.services.mensualidades_service import (
    buscar_mensualidad_activa
)

# ==========================================
# FECHA ACTUAL COLOMBIA
# ==========================================
def obtener_fecha_actual():

    timezone = current_app.config.get(
        "TIMEZONE",
        "America/Bogota"
    )

    return datetime.now(
        ZoneInfo(timezone)
    )


# ==========================================
# REGISTRAR INGRESO
# ==========================================
def registrar_ingreso(
    placa,
    tipo,
    modalidad="Hora",
    puesto_casco=None,
    cantidad_cascos=0
):

    placa = validar_placa(
        placa
    )

    tipo = validar_tipo_vehiculo(
        tipo
    )

    # ==========================================
    # DETECTAR MENSUALIDAD
    # ==========================================
    mensualidad = buscar_mensualidad_activa(
        placa
    )

    if mensualidad:

        modalidad = "Mensualidad"

    if placa_activa_db(placa):

        return {
            "success": False,
            "message": "Vehículo ya está dentro"
        }

    # ==========================================
    # VALIDAR PUESTO CASCO
    # ==========================================
    if puesto_casco:

        if puesto_casco_ocupado_db(
            puesto_casco
        ):

            return {
                "success": False,
                "message": (
                    f"El puesto de casco "
                    f"{puesto_casco} "
                    f"ya está ocupado"
                )
            }

    hora_actual = obtener_fecha_actual()

    # ==========================================
    # VALIDAR TARIFA NOCHE
    # ==========================================
    if modalidad == "Noche":

        hora = hora_actual.time()

        permitido = (

            hora.hour >= 19

            or

            hora.hour < 8
        )

        if not permitido:

            return {

                "success": False,

                "message":
                (
                    "La tarifa noche "
                    "solo puede registrarse "
                    "entre las 7:00 PM "
                    "y las 8:00 AM"
                )
            }

    ticket = insertar_ingreso_db(

        placa,

        tipo,

        hora_actual.isoformat(),

        modalidad,

        puesto_casco,

        cantidad_cascos
    )

    return {

        "success": True,

        "ticket": ticket,

        "placa": placa,

        "tipo": tipo,

        "modalidad": modalidad,

        "puesto_casco": puesto_casco,

        "cantidad_cascos": cantidad_cascos,

        "hora": hora_actual.strftime(
            "%d/%m/%Y %I:%M %p"
        )
    }


# ==========================================
# OBTENER VEHÍCULO
# ==========================================
def obtener_vehiculo(id):

    return obtener_vehiculo_db(id)


# ==========================================
# EDITAR VEHÍCULO
# ==========================================
def editar_vehiculo(
    id,
    placa,
    tipo
):

    placa = validar_placa(
        placa
    )

    tipo = validar_tipo_vehiculo(
        tipo
    )

    actualizar_vehiculo_db(

        id,

        placa,

        tipo
    )


# ==========================================
# ELIMINAR VEHÍCULO
# ==========================================
def eliminar_vehiculo(id):

    eliminar_vehiculo_db(id)


# ==========================================
# COMPATIBILIDAD LEGACY
# ==========================================
def borrar_vehiculo(id):

    eliminar_vehiculo(id)