from app.repositories.lavadero_repository import (

    registrar_lavado_db,

    obtener_historial_lavados_db,

    obtener_metricas_lavadero_db,

    obtener_ultimos_lavados_db,

    obtener_estadisticas_responsables_db,

    obtener_lavado_por_id_db,

    actualizar_lavado_db,

    eliminar_lavado_db,

    contar_lavados_placa_db
)

from app.utils.validators import (

    validar_id,

    validar_placa,

    validar_tipo_vehiculo,

    validar_tipo_lavado,

    validar_valor,

    validar_responsable
)


# ==========================================
# REGISTRAR LAVADO
# ==========================================
def registrar_lavado(

    placa,

    vehiculo,

    tipo_lavado,

    valor,

    responsable,

    fecha
):

    placa = validar_placa(
        placa
    )

    if validar_lavado_gratis(
        placa
    ):

        valor = 0

    vehiculo = validar_tipo_vehiculo(
        vehiculo
    )

    tipo_lavado = validar_tipo_lavado(
        tipo_lavado
    )

    valor = validar_valor(
        valor
    )

    responsable = validar_responsable(
        responsable
    )

    gratis = False

    if validar_lavado_gratis(
        placa
    ):

        valor = 0

        gratis = True

    registrar_lavado_db(

        placa,

        vehiculo,

        tipo_lavado,

        valor,

        responsable,

        fecha
    )

    return {

        "gratis": gratis,

        "valor": valor
    }


# ==========================================
# LISTAR LAVADOS
# ==========================================
def listar_lavados():

    return obtener_ultimos_lavados_db()


# ==========================================
# HISTORIAL LAVADOS
# ==========================================
def obtener_historial_lavados(

    placa="",

    fecha_inicio="",

    fecha_fin="",

    responsable=""
):

    return obtener_historial_lavados_db(

        placa,

        fecha_inicio,

        fecha_fin,

        responsable
    )

# ==========================================
# METRICAS LAVADERO
# ==========================================
def obtener_metricas_lavadero():

    return obtener_metricas_lavadero_db()


# ==========================================
# ULTIMOS LAVADOS
# ==========================================
def obtener_ultimos_lavados():

    return obtener_ultimos_lavados_db()


# ==========================================
# ESTADISTICAS RESPONSABLES
# ==========================================
def obtener_estadisticas_responsables():

    return obtener_estadisticas_responsables_db()


# ==========================================
# OBTENER LAVADO POR ID
# ==========================================
def obtener_lavado_por_id(

    lavado_id
):

    lavado_id = validar_id(
        lavado_id
    )

    return obtener_lavado_por_id_db(
        lavado_id
    )


# ==========================================
# ACTUALIZAR LAVADO
# ==========================================
def actualizar_lavado(

    lavado_id,

    placa,

    vehiculo,

    tipo_lavado,

    valor,

    responsable
):

    lavado_id = validar_id(
        lavado_id
    )

    placa = validar_placa(
        placa
    )

    vehiculo = validar_tipo_vehiculo(
        vehiculo
    )

    tipo_lavado = validar_tipo_lavado(
        tipo_lavado
    )

    valor = validar_valor(
        valor
    )

    responsable = validar_responsable(
        responsable
    )

    actualizar_lavado_db(

        lavado_id,

        placa,

        vehiculo,

        tipo_lavado,

        valor,

        responsable
    )

# ==========================================
# ELIMINAR LAVADO
# ==========================================
def eliminar_lavado(
    lavado_id
):

    lavado_id = validar_id(
        lavado_id
    )

    eliminar_lavado_db(
        lavado_id
    )

# ==========================================
# VALIDAR LAVADO GRATIS
# ==========================================
def validar_lavado_gratis(
    placa
):

    cantidad = contar_lavados_placa_db(
        placa
    )

    siguiente = cantidad + 1

    return siguiente % 5 == 0

# ==========================================
# CONTAR LAVADOS PLACA
# ==========================================
def contar_lavados_placa(
    placa
):

    return contar_lavados_placa_db(
        placa
    )

# ==========================================
# FORMATEAR FECHAS LAVADOS
# ==========================================
from datetime import datetime


def formatear_fechas_lavados(
    lavados
):

    for lavado in lavados:

        try:

            fecha = lavado["fecha"]

            if isinstance(
                fecha,
                str
            ):

                fecha = datetime.fromisoformat(
                    fecha
                )

            lavado["fecha"] = fecha.strftime(

                "%d/%m/%Y %H:%M"

            )

        except Exception:

            pass

    return lavados

# ==========================================
# DASHBOARD PRINCIPAL
# ==========================================
def obtener_dashboard_principal():

    metricas = obtener_metricas_lavadero()

    lavados = formatear_fechas_lavados(

        listar_lavados()

    )

    return {

        "lavados_motos": metricas.get(

            "lavados_motos",

            0

        ),

        "lavados_carros": metricas.get(

            "lavados_carros",

            0

        ),

        "total_servicios": metricas.get(

            "dinero_generado",

            0

        ),

        "lavados": lavados

    }