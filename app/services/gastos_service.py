from app.repositories.gastos_repository import (

    agregar_gasto_db,

    obtener_gastos_dia_db,

    obtener_total_gastos_db,

    eliminar_gasto_db,

    obtener_gasto_por_id_db,

    actualizar_gasto_db

)

# ==========================================
# AGREGAR GASTO
# ==========================================
def agregar_gasto(

    fecha,

    concepto,

    valor,

    usuario,

    hora
):

    concepto = (

        concepto or ""

    ).strip()

    if not concepto:

        raise ValueError(

            "Debe ingresar un concepto."

        )

    if len(concepto) > 100:

        raise ValueError(

            "El concepto no puede superar los 100 caracteres."

        )

    try:

        valor = int(valor)

    except Exception:

        raise ValueError(

            "El valor del gasto no es válido."

        )

    if valor <= 0:

        raise ValueError(

            "El valor debe ser mayor que cero."

        )

    agregar_gasto_db(

        fecha,

        concepto,

        valor,

        usuario,

        hora

    )


# ==========================================
# OBTENER GASTOS DEL DÍA
# ==========================================
def obtener_gastos_dia(
    fecha
):

    return obtener_gastos_dia_db(
        fecha
    )


# ==========================================
# TOTAL GASTOS DEL DÍA
# ==========================================
def obtener_total_gastos(
    fecha
):

    return obtener_total_gastos_db(
        fecha
    )

# ==========================================
# ELIMINAR GASTO
# ==========================================
def eliminar_gasto(
    gasto_id
):

    eliminar_gasto_db(

        gasto_id

    )

# ==========================================
# OBTENER GASTO POR ID
# ==========================================
def obtener_gasto_por_id(
    gasto_id
):

    return obtener_gasto_por_id_db(

        gasto_id

    )


# ==========================================
# ACTUALIZAR GASTO
# ==========================================
def actualizar_gasto(

    gasto_id,

    concepto,

    valor

):

    concepto = (

        concepto or ""

    ).strip()

    if not concepto:

        raise ValueError(

            "Debe ingresar un concepto."

        )

    if len(concepto) > 100:

        raise ValueError(

            "El concepto no puede superar los 100 caracteres."

        )

    try:

        valor = int(valor)

    except Exception:

        raise ValueError(

            "El valor del gasto no es válido."

        )

    if valor <= 0:

        raise ValueError(

            "El valor debe ser mayor que cero."

        )

    actualizar_gasto_db(

        gasto_id,

        concepto,

        valor

    )