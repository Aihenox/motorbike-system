from app.repositories.tarifas_repository import (
    obtener_tarifas_db,
    actualizar_tarifas_db,
    obtener_tarifa_activa_db
)

# ==========================================
# OBTENER TARIFAS
# ==========================================
def obtener_tarifas():

    return obtener_tarifas_db()


# ==========================================
# ACTUALIZAR TARIFAS
# ==========================================
def actualizar_tarifas(

    hora_moto,
    hora_carro,

    noche_moto,
    noche_carro,

    mensualidad_moto,
    mensualidad_carro,

    minutos_gracia
):

    valores = {
        "hora_moto": hora_moto,
        "hora_carro": hora_carro,
        "noche_moto": noche_moto,
        "noche_carro": noche_carro,
        "mensualidad_moto": mensualidad_moto,
        "mensualidad_carro": mensualidad_carro
    }

    if any(
        not isinstance(valor, int) or valor <= 0
        for valor in valores.values()
    ):

        raise ValueError(
            "Todas las tarifas deben ser números enteros mayores que cero"
        )

    if (
        not isinstance(minutos_gracia, int)
        or minutos_gracia < 0
        or minutos_gracia > 59
    ):

        raise ValueError(
            "Los minutos de gracia deben estar entre 0 y 59"
        )

    actualizar_tarifas_db(

        hora_moto,
        hora_carro,

        noche_moto,
        noche_carro,

        mensualidad_moto,
        mensualidad_carro,

        minutos_gracia
    )

# ==========================================
# TARIFA ACTIVA
# ==========================================
def obtener_tarifa_activa():

    tarifa = obtener_tarifa_activa_db()

    if tarifa:

        return dict(tarifa)

    return None
