from app.repositories.descuentos_lavadores_repository import (

    agregar_descuento_db,

    obtener_descuentos_dia_db,

    obtener_total_descuentos_responsable_db,

    obtener_descuentos_agrupados_db

)

# ==========================================
# AGREGAR DESCUENTO
# ==========================================
def agregar_descuento(

    fecha,

    responsable,

    concepto,

    valor,

    usuario,

    hora

):

    responsable = (responsable or "").strip()

    concepto = (concepto or "").strip()

    if not responsable:

        raise ValueError(

            "Debe seleccionar un responsable."

        )

    if not concepto:

        raise ValueError(

            "Debe ingresar un concepto."

        )

    valor = int(valor)

    if valor <= 0:

        raise ValueError(

            "El valor debe ser mayor que cero."

        )

    agregar_descuento_db(

        fecha,

        responsable,

        concepto,

        valor,

        usuario,

        hora

    )

# ==========================================
# DESCUENTOS DEL DÍA
# ==========================================
def obtener_descuentos_dia(

    fecha

):

    return obtener_descuentos_dia_db(

        fecha

    )

# ==========================================
# TOTAL DESCUENTOS
# ==========================================
def obtener_total_descuentos_responsable(

    fecha,

    responsable

):

    return obtener_total_descuentos_responsable_db(

        fecha,

        responsable

    )

