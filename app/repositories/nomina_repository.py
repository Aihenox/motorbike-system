from app.repositories.connection import conectar


def obtener_resumen_nomina():

    with conectar() as conn:

        c = conn.cursor()

        placeholder = "%s" if conn.__class__.__module__.startswith("psycopg2") else "?"

        c.execute("""
            SELECT
                responsable,
                COUNT(*) AS servicios,
                COALESCE(SUM(valor_comision),0) AS facturado
            FROM lavados
            WHERE COALESCE(pagado,0)=0
            GROUP BY responsable
            ORDER BY responsable
        """)

        registros = c.fetchall()

        resultado = []

        for fila in registros:

            responsable = fila["responsable"]
            servicios = fila["servicios"]
            valor_comision = float(fila["facturado"] or 0)

            c.execute(
                f"""
                SELECT COALESCE(SUM(valor),0) AS total
                FROM descuentos_lavadores
                WHERE responsable={placeholder}
                  AND COALESCE(pagado,0)=0
                """,
                (responsable,)
            )

            descuento = c.fetchone()

            if descuento:
                total_descuentos = float(descuento["total"] or 0)
            else:
                total_descuentos = 0

            comision = valor_comision * 0.50

            resultado.append({
                "responsable": responsable,
                "servicios": servicios,
                "facturado": valor_comision,
                "comision": comision,
                "descuentos": total_descuentos,
                "total": comision - total_descuentos
            })

        return resultado


def obtener_detalle_nomina(responsable):

    with conectar() as conn:

        c = conn.cursor()

        placeholder = "%s" if conn.__class__.__module__.startswith("psycopg2") else "?"

        c.execute(
            f"""
            SELECT
                fecha,
                SUM(CASE WHEN LOWER(vehiculo)='moto' THEN 1 ELSE 0 END) AS motos,
                SUM(CASE WHEN LOWER(vehiculo)='carro' THEN 1 ELSE 0 END) AS carros,
                COUNT(*) AS vehiculos,
                COALESCE(SUM(valor_comision),0) AS valor_lavados
            FROM lavados
            WHERE responsable={placeholder}
              AND COALESCE(pagado,0)=0
            GROUP BY fecha
            ORDER BY fecha
            """,
            (responsable,)
        )

        registros = c.fetchall()

        resultado = []

        for fila in registros:

            valor = float(fila["valor_lavados"] or 0)

            resultado.append({

                "fecha": str(fila["fecha"])[:10],
                "motos": int(fila["motos"] or 0),
                "carros": int(fila["carros"] or 0),
                "vehiculos": int(fila["vehiculos"] or 0),
                "valor_lavados": valor,
                "comision": valor * 0.50

            })

        return resultado

def liquidar_nomina(
    responsable,
    fecha_pago,
    usuario,
    hora
):

    with conectar() as conn:

        c = conn.cursor()

        placeholder = "%s" if conn.__class__.__module__.startswith("psycopg2") else "?"

        # ==============================
        # Total lavados pendientes
        # ==============================

        c.execute(
            f"""
            SELECT COALESCE(SUM(valor_comision),0) AS total
            FROM lavados
            WHERE responsable={placeholder}
              AND COALESCE(pagado,0)=0
            """,
            (responsable,)
        )

        facturado = float(c.fetchone()["total"] or 0)

        bruto = facturado * 0.50
        # ==============================
        # Total descuentos pendientes
        # ==============================

        c.execute(
            f"""
            SELECT COALESCE(SUM(valor),0) AS total
            FROM descuentos_lavadores
            WHERE responsable={placeholder}
              AND COALESCE(pagado,0)=0
            """,
            (responsable,)
        )

        descuentos = float(c.fetchone()["total"] or 0)

        total_pagado = bruto - descuentos

        # ==============================
        # Registrar pago
        # ==============================

        if conn.__class__.__module__.startswith("psycopg2"):

            c.execute(
                """
                INSERT INTO pagos_lavadores(
                    responsable,
                    fecha_pago,
                    total_bruto,
                    total_descuentos,
                    total_pagado,
                    usuario,
                    hora
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    responsable,
                    fecha_pago,
                    bruto,
                    descuentos,
                    total_pagado,
                    usuario,
                    hora
                )
            )

        else:

            c.execute(
                """
                INSERT INTO pagos_lavadores(
                    responsable,
                    fecha_pago,
                    total_bruto,
                    total_descuentos,
                    total_pagado,
                    usuario,
                    hora
                )
                VALUES (?,?,?,?,?,?,?)
                """,
                (
                    responsable,
                    fecha_pago,
                    bruto,
                    descuentos,
                    total_pagado,
                    usuario,
                    hora
                )
            )

        # ==============================
        # Marcar lavados como pagados
        # ==============================

        c.execute(
            f"""
            UPDATE lavados
            SET pagado=1
            WHERE responsable={placeholder}
              AND COALESCE(pagado,0)=0
            """,
            (responsable,)
        )

        # ==============================
        # Marcar descuentos como pagados
        # ==============================

        c.execute(
            f"""
            UPDATE descuentos_lavadores
            SET pagado=1
            WHERE responsable={placeholder}
              AND COALESCE(pagado,0)=0
            """,
            (responsable,)
        )

        conn.commit()

        return {
            "bruto": bruto,
            "descuentos": descuentos,
            "total": total_pagado
        }

def obtener_descuentos_pendientes(responsable):

    with conectar() as conn:

        c = conn.cursor()

        placeholder = "%s" if conn.__class__.__module__.startswith("psycopg2") else "?"

        c.execute(
            f"""
            SELECT
                fecha,
                concepto,
                valor
            FROM descuentos_lavadores
            WHERE responsable={placeholder}
              AND COALESCE(pagado,0)=0
            ORDER BY fecha
            """,
            (responsable,)
        )

        filas = c.fetchall()

        columnas = [col[0] for col in c.description]

        return [
            dict(zip(columnas, fila))
            for fila in filas
        ]

def obtener_ultimo_pago(responsable):

    with conectar() as conn:

        c = conn.cursor()

        placeholder = "%s" if conn.__class__.__module__.startswith("psycopg2") else "?"

        c.execute(
            f"""
            SELECT fecha_pago
            FROM pagos_lavadores
            WHERE responsable={placeholder}
            ORDER BY fecha_pago DESC
            LIMIT 1
            """,
            (responsable,)
        )

        fila = c.fetchone()

        if fila:

            return fila["fecha_pago"]

        return None

def registrar_descuento_nomina(
    responsable,
    concepto,
    valor,
    fecha,
    usuario,
    hora
):

    with conectar() as conn:

        c = conn.cursor()

        if conn.__class__.__module__.startswith("psycopg2"):

            c.execute(

                """

                INSERT INTO descuentos_lavadores(

                    fecha,
                    responsable,
                    concepto,
                    valor,
                    usuario,
                    hora

                )

                VALUES(

                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s

                )

                """,

                (

                    fecha,

                    responsable,

                    concepto,

                    valor,

                    usuario,

                    hora

                )

            )

        else:

            c.execute(

                """

                INSERT INTO descuentos_lavadores(

                    fecha,
                    responsable,
                    concepto,
                    valor,
                    usuario,
                    hora

                )

                VALUES(

                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?

                )

                """,

                (

                    fecha,

                    responsable,

                    concepto,

                    valor,

                    usuario,

                    hora

                )

            )

        conn.commit()