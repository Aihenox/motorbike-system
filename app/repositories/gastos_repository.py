import os

from app.repositories.connection import conectar


# ==========================================
# MOTOR DATABASE
# ==========================================
POSTGRES = os.getenv(
    "DATABASE_URL"
)


# ==========================================
# AGREGAR GASTO
# ==========================================
def agregar_gasto_db(

    fecha,

    concepto,

    valor,

    usuario,

    hora
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                INSERT INTO gastos(

                    fecha,

                    concepto,

                    valor,

                    usuario,

                    hora

                )

                VALUES (%s,%s,%s,%s,%s)

            """, (

                fecha,

                concepto,

                valor,

                usuario,

                hora

            ))

        else:

            c.execute("""

                INSERT INTO gastos(

                    fecha,

                    concepto,

                    valor,

                    usuario,

                    hora

                )

                VALUES (?,?,?,?,?)

            """, (

                fecha,

                concepto,

                valor,

                usuario,

                hora

            ))

        conn.commit()


# ==========================================
# OBTENER GASTOS DEL DIA
# ==========================================
def obtener_gastos_dia_db(
    fecha
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT

                    id,

                    concepto,

                    valor,

                    usuario,

                    hora

                FROM gastos

                WHERE fecha=%s

                ORDER BY id DESC

            """, (

                fecha,

            ))

        else:

            c.execute("""

                SELECT

                    id,

                    concepto,

                    valor,

                    usuario,

                    hora

                FROM gastos

                WHERE fecha=?

                ORDER BY id DESC

            """, (

                fecha,

            ))

        rows = c.fetchall()

        resultado = []

        for row in rows:

            if POSTGRES:

                resultado.append({

                    "id": row["id"],

                    "concepto": row["concepto"],

                    "valor": row["valor"],

                    "usuario": row["usuario"],

                    "hora": row["hora"]

                })

            else:

                resultado.append({

                    "id": row[0],

                    "concepto": row[1],

                    "valor": row[2],

                    "usuario": row[3],

                    "hora": row[4]

                })

        return resultado


# ==========================================
# TOTAL GASTOS DEL DIA
# ==========================================
def obtener_total_gastos_db(
    fecha
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

                FROM gastos

                WHERE fecha=%s

            """, (

                fecha,

            ))

            row = c.fetchone()

            return list(row.values())[0]

        else:

            c.execute("""

                SELECT

                    COALESCE(

                        SUM(valor),

                        0

                    )

                FROM gastos

                WHERE fecha=?

            """, (

                fecha,

            ))

            row = c.fetchone()

            return row[0]

# ==========================================
# ELIMINAR GASTO
# ==========================================
def eliminar_gasto_db(
    gasto_id
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                DELETE FROM gastos

                WHERE id=%s

            """, (

                gasto_id,

            ))

        else:

            c.execute("""

                DELETE FROM gastos

                WHERE id=?

            """, (

                gasto_id,

            ))

        conn.commit()

# ==========================================
# OBTENER GASTO POR ID
# ==========================================
def obtener_gasto_por_id_db(
    gasto_id
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                SELECT

                    id,

                    concepto,

                    valor

                FROM gastos

                WHERE id=%s

            """, (

                gasto_id,

            ))

        else:

            c.execute("""

                SELECT

                    id,

                    concepto,

                    valor

                FROM gastos

                WHERE id=?

            """, (

                gasto_id,

            ))

        row = c.fetchone()

        if not row:

            return None

        if POSTGRES:

            return {

                "id": row["id"],
                "concepto": row["concepto"],
                "valor": row["valor"]

            }

        return {

            "id": row[0],
            "concepto": row[1],
            "valor": row[2]

        }


# ==========================================
# ACTUALIZAR GASTO
# ==========================================
def actualizar_gasto_db(
    gasto_id,
    concepto,
    valor
):

    with conectar() as conn:

        c = conn.cursor()

        if POSTGRES:

            c.execute("""

                UPDATE gastos

                SET

                    concepto=%s,

                    valor=%s

                WHERE id=%s

            """, (

                concepto,
                valor,
                gasto_id

            ))

        else:

            c.execute("""

                UPDATE gastos

                SET

                    concepto=?,

                    valor=?

                WHERE id=?

            """, (

                concepto,
                valor,
                gasto_id

            ))

        conn.commit()