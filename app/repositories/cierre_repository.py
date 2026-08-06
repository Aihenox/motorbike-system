import os

from datetime import datetime
from zoneinfo import ZoneInfo

from app.repositories.connection import conectar

from app.repositories.cafeteria_repository import (
    obtener_total_ventas_hoy_db
)

from app.repositories.gastos_repository import (
    obtener_total_gastos_db
)

from app.repositories.descuentos_lavadores_repository import (
    obtener_descuentos_agrupados_db
)


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# HELPER VALOR
# ==========================================
def obtener_valor(row):

    if not row:
        return 0

    # PostgreSQL
    if POSTGRES:
        return list(row.values())[0] or 0

    # SQLite
    return row[0] or 0


# ==========================================
# HELPER CIERRE
# ==========================================
def convertir_row_cierre(row):

    if POSTGRES:

        return {

            "id": row["id"],

            "fecha": row["fecha"],

            "saldo_inicial": row["saldo_inicial"],

            "ingresos_dia": row["ingresos_dia"],

            "egresos_dia": row["egresos_dia"],

            "saldo_final": row["saldo_final"],

            "total_parqueadero": row["total_parqueadero"],

            "total_lavadero": row["total_lavadero"],

            "total_general": row["total_general"],

            "observaciones": row["observaciones"],

            "usuario": row["usuario"],

            "hora_cierre": row["hora_cierre"]

        }

    return {

        "id": row[0],

        "fecha": row[1],

        "saldo_inicial": row[2],

        "ingresos_dia": row[3],

        "egresos_dia": row[4],

        "saldo_final": row[5],

        "total_parqueadero": row[6],

        "total_lavadero": row[7],

        "total_general": row[8],

        "observaciones": row[9],

        "usuario": row[10],

        "hora_cierre": row[11]

    }

# ==========================================
# MÉTRICAS CIERRE
# ==========================================
def obtener_metricas_cierre_db():

    with conectar() as conn:

        c = conn.cursor()

        ahora = datetime.now(
            ZoneInfo("America/Bogota")
        )

        hoy_iso = ahora.strftime(
            "%Y-%m-%d"
        )

        hoy_legacy = ahora.strftime(
            "%d/%m/%Y"
        )

        # ==========================================
        # PARQUEADERO
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM ingresos

                WHERE estado = 'Fuera'

                AND (
                    hora_salida LIKE %s
                    OR hora_salida LIKE %s
                )

            """, (
                f"{hoy_iso}%",
                f"{hoy_legacy}%"
            ))

        else:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM ingresos

                WHERE estado = 'Fuera'

                AND (
                    hora_salida LIKE ?
                    OR hora_salida LIKE ?
                )

            """, (
                f"{hoy_iso}%",
                f"{hoy_legacy}%"
            ))

        total_parqueadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # LAVADERO
        # ==========================================
        if POSTGRES:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM lavados

                WHERE fecha LIKE %s

            """, (f"{hoy_iso}%",))

        else:

            c.execute("""

                SELECT COALESCE(
                    SUM(valor),
                    0
                )

                FROM lavados

                WHERE fecha LIKE ?

            """, (f"{hoy_iso}%",))

        total_lavadero = obtener_valor(
            c.fetchone()
        )

        # ==========================================
        # CAFETERIA
        # ==========================================
        total_cafeteria = obtener_total_ventas_hoy_db()

        # ==========================================
        # TOTAL GENERAL
        # ==========================================
        saldo_inicial = obtener_saldo_inicial_db()

        # Aquí seguiremos agregando cafetería,
        # mensualidades y otros ingresos.
        ingresos_dia = total_parqueadero + total_lavadero + total_cafeteria

        # Nómina del día
        _, egresos_nomina = obtener_pago_lavadores_db()

        # Los gastos se agregan en el service
        egresos_dia = egresos_nomina

        saldo_actual = (

            saldo_inicial

            +

            ingresos_dia

            -

            egresos_dia

        )

        return {

            "saldo_inicial": saldo_inicial,

            "ingresos_dia": ingresos_dia,

            "egresos_dia": egresos_dia,

            "saldo_actual": saldo_actual,

            # Compatibilidad con el resto del sistema
            "total_parqueadero": total_parqueadero,

            "total_lavadero": total_lavadero,

            "total_general": ingresos_dia,

            "detalle_ingresos": {

                "parqueadero": total_parqueadero,

                "lavadero": total_lavadero,

                "cafeteria": total_cafeteria,

                "otros": 0

            },

            "detalle_egresos": {

                "nomina": egresos_nomina,

                "gastos": 0

            }

        }
    
# ==========================================
# SALDO INICIAL DEL DÍA
# ==========================================
def obtener_saldo_inicial_db():

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT saldo_final

                FROM cierres_caja

                ORDER BY id DESC

                LIMIT 1

            """)

        else:

            c.execute("""

                SELECT saldo_final

                FROM cierres_caja

                ORDER BY id DESC

                LIMIT 1

            """)

        fila = c.fetchone()

        if not fila:

            return 0

        return obtener_valor(fila)

# ==========================================
# GUARDAR CIERRE
# ==========================================
def guardar_cierre_db(

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
):

    with conectar() as conn:

        c = conn.cursor()

        fecha_legacy = datetime.strptime(
            fecha,
            "%Y-%m-%d"
        ).strftime(
            "%d/%m/%Y"
        )

        if POSTGRES:

            c.execute("""
                SELECT 1
                FROM cierres_caja
                WHERE fecha IN (%s, %s)
                LIMIT 1
            """, (fecha, fecha_legacy))

        else:

            c.execute("""
                SELECT 1
                FROM cierres_caja
                WHERE fecha IN (?, ?)
                LIMIT 1
            """, (fecha, fecha_legacy))

        if c.fetchone():

            raise ValueError(
                "Ya existe un cierre de caja para esta fecha"
            )

        if POSTGRES:

            c.execute("""

                INSERT INTO cierres_caja (

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

                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

            """, (
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
            ))

        else:

            c.execute("""

                INSERT INTO cierres_caja (

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

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            """, (

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

            ))

        conn.commit()


# ==========================================
# HISTORIAL CIERRES
# ==========================================
def obtener_historial_cierres_db():

    with conectar() as conn:

        c = conn.cursor()

        c.execute("""

            SELECT

                id,
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

                FROM cierres_caja

            ORDER BY id DESC

        """)

        rows = c.fetchall()

        resultado = []

        for row in rows:

            resultado.append(
                convertir_row_cierre(row)
            )

        return resultado

# ==========================================
# PAGO LAVADORES DEL DÍA
# ==========================================
def obtener_pago_lavadores_db():

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now(
            ZoneInfo("America/Bogota")
        ).strftime("%Y-%m-%d")

        if POSTGRES:

            c.execute(
                """
                SELECT
                    responsable,
                    total_bruto,
                    total_descuentos,
                    total_pagado
                FROM pagos_lavadores
                WHERE fecha_pago = %s
                ORDER BY responsable
                """,
                (hoy,)
            )

        else:

            c.execute(
                """
                SELECT
                    responsable,
                    total_bruto,
                    total_descuentos,
                    total_pagado
                FROM pagos_lavadores
                WHERE fecha_pago = ?
                ORDER BY responsable
                """,
                (hoy,)
            )

        rows = c.fetchall()

        resultado = []
        total_pago = 0

        for row in rows:

            if POSTGRES:

                item = {
                    "responsable": row["responsable"],
                    "cantidad": 0,
                    "total": int(row["total_bruto"]),
                    "pago": int(row["total_bruto"]),
                    "descuento": int(row["total_descuentos"]),
                    "neto": int(row["total_pagado"])
                }

            else:

                item = {
                    "responsable": row[0],
                    "cantidad": 0,
                    "total": int(row[1]),
                    "pago": int(row[1]),
                    "descuento": int(row[2]),
                    "neto": int(row[3])
                }

            total_pago += item["neto"]
            resultado.append(item)

        return resultado, total_pago

    with conectar() as conn:

        c = conn.cursor()

        hoy = datetime.now(

            ZoneInfo("America/Bogota")

        ).strftime(

            "%Y-%m-%d"

        )

        if POSTGRES:

            c.execute("""

                SELECT

                    responsable,

                    COUNT(*) AS cantidad,

                    SUM(valor) AS total,

                    SUM(valor) * 0.5 AS pago

                FROM lavados

                WHERE fecha LIKE %s

                GROUP BY responsable

                ORDER BY responsable

            """, (

                f"{hoy}%",

            ))

        else:

            c.execute("""

                SELECT

                    responsable,

                    COUNT(*) AS cantidad,

                    SUM(valor) AS total,

                    SUM(valor) * 0.5 AS pago

                FROM lavados

                WHERE fecha LIKE ?

                GROUP BY responsable

                ORDER BY responsable

            """, (

                f"{hoy}%",

            ))

        rows = c.fetchall()

        descuentos = obtener_descuentos_agrupados_db(

            hoy

        )

        resultado = []

        total_pago = 0

        for row in rows:

            if POSTGRES:

                item = {

                    "responsable": row["responsable"],

                    "cantidad": row["cantidad"],

                    "total": row["total"],

                    "pago": int(row["pago"])

                }

            else:

                item = {

                    "responsable": row[0],

                    "cantidad": row[1],

                    "total": row[2],

                    "pago": int(row[3])

                }

            descuento = descuentos.get(

                item["responsable"],

                0

            )

            item["descuento"] = int(descuento)

            item["neto"] = max(

                0,

                item["pago"] - item["descuento"]

            )

            total_pago += item["neto"]

            resultado.append(item)

        return resultado, total_pago