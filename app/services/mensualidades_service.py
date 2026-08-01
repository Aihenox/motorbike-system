from app.repositories.mensualidades_repository import (
    obtener_mensualidades_db,
    crear_mensualidad_db,
    obtener_mensualidad_db,
    actualizar_mensualidad_db,
    eliminar_mensualidad_db,
    buscar_mensualidad_activa_db
)

from datetime import datetime
from zoneinfo import ZoneInfo

from app.utils.validators import (
    validar_placa,
    validar_rango_fechas,
    validar_tipo_vehiculo
)


def _hoy_colombia():

    return datetime.now(
        ZoneInfo("America/Bogota")
    ).date()


def _validar_datos_mensualidad(
    placa,
    tipo,
    fecha_inicio,
    fecha_fin,
    estado
):

    placa = validar_placa(
        placa
    )

    tipo = validar_tipo_vehiculo(
        tipo
    )

    fecha_inicio, fecha_fin = validar_rango_fechas(
        fecha_inicio,
        fecha_fin
    )

    if estado not in {"Activa", "Inactiva"}:

        raise ValueError(
            "Estado de mensualidad inválido"
        )

    return placa, tipo, fecha_inicio, fecha_fin, estado


# ==========================================
# LISTAR MENSUALIDADES
# ==========================================
def listar_mensualidades():

    registros = obtener_mensualidades_db()

    hoy = _hoy_colombia()

    resultado = []

    for item in registros:

        data = dict(item)

        try:

            # ==========================
            # ESTADO INACTIVO
            # ==========================
            if data["estado"] != "Activa":

                data["vigencia"] = "Inactiva"

            else:

                fecha_fin = datetime.strptime(

                    data["fecha_fin"],

                    "%Y-%m-%d"

                ).date()

                dias = (

                    fecha_fin - hoy

                ).days

                # ==========================
                # VIGENCIA
                # ==========================
                if dias < 0:

                    data["vigencia"] = "Vencida"

                elif dias <= 3:

                    data["vigencia"] = (
                        "Próxima a vencer"
                    )

                else:

                    data["vigencia"] = "Vigente"

        except Exception:

            data["vigencia"] = (
                "Sin fecha"
            )

        resultado.append(
            data
        )

    return resultado

# ==========================================
# CREAR MENSUALIDAD
# ==========================================
def crear_mensualidad(

    placa,

    tipo,

    propietario,

    telefono,

    fecha_inicio,

    fecha_fin,

    estado
):

    placa, tipo, fecha_inicio, fecha_fin, estado = (
        _validar_datos_mensualidad(
            placa,
            tipo,
            fecha_inicio,
            fecha_fin,
            estado
        )
    )

    return crear_mensualidad_db(

        placa,

        tipo,

        propietario,

        telefono,

        fecha_inicio,

        fecha_fin,

        estado
    )

# ==========================================
# OBTENER MENSUALIDAD
# ==========================================
def obtener_mensualidad(id):

    return obtener_mensualidad_db(
        id
    )


# ==========================================
# ACTUALIZAR MENSUALIDAD
# ==========================================
def actualizar_mensualidad(

    id,

    placa,

    tipo,

    propietario,

    telefono,

    fecha_inicio,

    fecha_fin,

    estado
):

    placa, tipo, fecha_inicio, fecha_fin, estado = (
        _validar_datos_mensualidad(
            placa,
            tipo,
            fecha_inicio,
            fecha_fin,
            estado
        )
    )

    actualizar_mensualidad_db(

        id,

        placa,

        tipo,

        propietario,

        telefono,

        fecha_inicio,

        fecha_fin,

        estado
    )

# ==========================================
# ELIMINAR MENSUALIDAD
# ==========================================
def eliminar_mensualidad(id):

    eliminar_mensualidad_db(
        id
    )

# ==========================================
# BUSCAR MENSUALIDAD ACTIVA
# ==========================================
def buscar_mensualidad_activa(
    placa
):

    placa = validar_placa(
        placa
    )

    return buscar_mensualidad_activa_db(
        placa,
        _hoy_colombia().isoformat()
    )

# ==========================================
# ACTUALIZAR MENSUALIDADES VENCIDAS
# ==========================================
def actualizar_mensualidades_vencidas():

    registros = obtener_mensualidades_db()

    hoy = _hoy_colombia()

    for item in registros:

        try:

            data = dict(item)

            if data["estado"] != "Activa":

                continue

            fecha_fin = datetime.strptime(

                data["fecha_fin"],

                "%Y-%m-%d"

            ).date()

            if fecha_fin < hoy:

                actualizar_mensualidad(

                    data["id"],

                    data["placa"],

                    data["tipo"],

                    data["propietario"],

                    data["telefono"],

                    data["fecha_inicio"],

                    data["fecha_fin"],

                    "Inactiva"
                )

        except Exception:

            pass
