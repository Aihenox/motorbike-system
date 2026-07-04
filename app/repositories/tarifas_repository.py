import os

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# OBTENER TARIFAS
# ==========================================
def obtener_tarifas_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT *

            FROM configuracion_tarifas

            ORDER BY id

            LIMIT 1

        """)

        return c.fetchone()


# ==========================================
# ACTUALIZAR TARIFAS
# ==========================================
def actualizar_tarifas_db(

    hora_moto,
    hora_carro,

    noche_moto,
    noche_carro,

    mensualidad_moto,
    mensualidad_carro,

    minutos_gracia
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                UPDATE configuracion_tarifas

                SET

                    hora_moto = %s,
                    hora_carro = %s,

                    noche_moto = %s,
                    noche_carro = %s,

                    mensualidad_moto = %s,
                    mensualidad_carro = %s,

                    minutos_gracia = %s

                WHERE id = 1

            """, (

                hora_moto,
                hora_carro,

                noche_moto,
                noche_carro,

                mensualidad_moto,
                mensualidad_carro,

                minutos_gracia
            ))

        else:

            c.execute("""

                UPDATE configuracion_tarifas

                SET

                    hora_moto = ?,
                    hora_carro = ?,

                    noche_moto = ?,
                    noche_carro = ?,

                    mensualidad_moto = ?,
                    mensualidad_carro = ?,

                    minutos_gracia = ?

                WHERE id = 1

            """, (

                hora_moto,
                hora_carro,

                noche_moto,
                noche_carro,

                mensualidad_moto,
                mensualidad_carro,

                minutos_gracia
            ))

        conn.commit()

# ==========================================
# OBTENER TARIFA ACTIVA
# ==========================================
def obtener_tarifa_activa_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT *

            FROM configuracion_tarifas

            ORDER BY id

            LIMIT 1

        """)

        return c.fetchone()