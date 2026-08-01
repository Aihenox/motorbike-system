import os

from app.repositories.connection import conectar

POSTGRES = os.getenv(
    "DATABASE_URL"
)

def agregar_descuento_db(

    fecha,

    responsable,

    concepto,

    valor,

    usuario,

    hora

):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                INSERT INTO descuentos_lavadores(

                    fecha,

                    responsable,

                    concepto,

                    valor,

                    usuario,

                    hora

                )

                VALUES(%s,%s,%s,%s,%s,%s)

            """,(

                fecha,

                responsable,

                concepto,

                valor,

                usuario,

                hora

            ))

        else:

            c.execute("""

                INSERT INTO descuentos_lavadores(

                    fecha,

                    responsable,

                    concepto,

                    valor,

                    usuario,

                    hora

                )

                VALUES(?,?,?,?,?,?)

            """,(

                fecha,

                responsable,

                concepto,

                valor,

                usuario,

                hora

            ))

        conn.commit()

def obtener_descuentos_dia_db(fecha):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT

                    id,

                    responsable,

                    concepto,

                    valor,

                    usuario,

                    hora

                FROM descuentos_lavadores

                WHERE fecha=%s

                ORDER BY responsable,
                         id DESC

            """,(fecha,))

        else:

            c.execute("""

                SELECT

                    id,

                    responsable,

                    concepto,

                    valor,

                    usuario,

                    hora

                FROM descuentos_lavadores

                WHERE fecha=?

                ORDER BY responsable,
                         id DESC

            """,(fecha,))

        rows = c.fetchall()

        resultado = []

        for row in rows:

            if POSTGRES:

                resultado.append({

                    "id":row["id"],

                    "responsable":row["responsable"],

                    "concepto":row["concepto"],

                    "valor":row["valor"],

                    "usuario":row["usuario"],

                    "hora":row["hora"]

                })

            else:

                resultado.append({

                    "id":row[0],

                    "responsable":row[1],

                    "concepto":row[2],

                    "valor":row[3],

                    "usuario":row[4],

                    "hora":row[5]

                })

        return resultado

def obtener_total_descuentos_responsable_db(

    fecha,

    responsable

):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT

                    COALESCE(

                        SUM(valor),

                        0

                    )

                FROM descuentos_lavadores

                WHERE fecha=%s

                AND responsable=%s

            """,(

                fecha,

                responsable

            ))

        else:

            c.execute("""

                SELECT

                    COALESCE(

                        SUM(valor),

                        0

                    )

                FROM descuentos_lavadores

                WHERE fecha=?

                AND responsable=?

            """,(

                fecha,

                responsable

            ))

        row = c.fetchone()

        if POSTGRES:

            return list(row.values())[0] or 0

        return row[0] or 0

# ==========================================
# DESCUENTOS AGRUPADOS DEL DÍA
# ==========================================
def obtener_descuentos_agrupados_db(fecha):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT

                    responsable,

                    COALESCE(

                        SUM(valor),

                        0

                    ) AS total

                FROM descuentos_lavadores

                WHERE fecha=%s

                GROUP BY responsable

            """, (

                fecha,

            ))

        else:

            c.execute("""

                SELECT

                    responsable,

                    COALESCE(

                        SUM(valor),

                        0

                    ) AS total

                FROM descuentos_lavadores

                WHERE fecha=?

                GROUP BY responsable

            """, (

                fecha,

            ))

        rows = c.fetchall()

        descuentos = {}

        for row in rows:

            if POSTGRES:

                descuentos[row["responsable"]] = int(row["total"] or 0)

            else:

                descuentos[row[0]] = int(row[1] or 0)

        return descuentos