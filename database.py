import os

from app.repositories.connection import conectar

from app.services.auth_service import (
    crear_admin_default
)


# ==========================================
# CREAR BASE DE DATOS
# ==========================================
def crear_bd():

    with conectar() as conn:

        c = conn.cursor()

        postgres = os.getenv(
            "DATABASE_URL"
        )

        id_type = (
            "SERIAL PRIMARY KEY"
            if postgres
            else "INTEGER PRIMARY KEY AUTOINCREMENT"
        )

        crear_tabla_ingresos(
            c,
            id_type
        )

        crear_tabla_usuarios(
            c,
            id_type
        )

        crear_tabla_lavados(
            c,
            id_type
        )

        crear_tabla_cierres(
            c,
            id_type
        )

        crear_tabla_gastos(
            c,
            id_type
        )

        crear_tabla_tarifas(
            c,
            id_type
        )

        crear_tabla_descuentos_lavadores(
            c,
            id_type
        )

        crear_tabla_pagos_lavadores(
            c,
            id_type
        )

        crear_tabla_mensualidades(
            c,
            id_type
        )

        crear_tabla_productos_cafeteria(
            c,
            id_type
        )

        crear_tabla_ventas_cafeteria(
            c,
            id_type
        )

        actualizar_tabla_ingresos(c)

        actualizar_tablas_nomina(c)

        actualizar_tabla_cierres(c)

        crear_indices(c)

        insertar_tarifas_default(c)

        conn.commit()

    crear_admin_default()


# ==========================================
# INGRESOS
# ==========================================
def crear_tabla_ingresos(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS ingresos(

            id {id_type},

            placa TEXT NOT NULL,

            tipo TEXT NOT NULL,

            hora_ingreso TEXT NOT NULL,

            hora_salida TEXT,

            valor INTEGER,

            estado TEXT NOT NULL

        )

    """)


# ==========================================
# USUARIOS
# ==========================================
def crear_tabla_usuarios(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS usuarios(

            id {id_type},

            usuario TEXT UNIQUE,

            password TEXT,

            rol TEXT

        )

    """)


def crear_tabla_lavados(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS lavados(

            id {id_type},

            placa TEXT NOT NULL,

            vehiculo TEXT NOT NULL,

            tipo_lavado TEXT NOT NULL,

            valor INTEGER NOT NULL,

            valor_comision INTEGER NOT NULL,

            responsable TEXT NOT NULL,

            fecha TEXT NOT NULL,

            cortesia INTEGER DEFAULT 0

        )

    """)
    
# ==========================================
# CIERRES
# ==========================================
def crear_tabla_cierres(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS cierres_caja(

            id {id_type},

            fecha TEXT NOT NULL,

            saldo_inicial INTEGER NOT NULL DEFAULT 0,

            ingresos_dia INTEGER NOT NULL DEFAULT 0,

            egresos_dia INTEGER NOT NULL DEFAULT 0,

            saldo_final INTEGER NOT NULL DEFAULT 0,

            total_parqueadero INTEGER NOT NULL,

            total_lavadero INTEGER NOT NULL,

            total_general INTEGER NOT NULL,

            observaciones TEXT,

            usuario TEXT NOT NULL,

            hora_cierre TEXT NOT NULL

        )

    """)

# ==========================================
# GASTOS
# ==========================================
def crear_tabla_gastos(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS gastos(

            id {id_type},

            fecha TEXT NOT NULL,

            concepto TEXT NOT NULL,

            valor INTEGER NOT NULL,

            usuario TEXT NOT NULL,

            hora TEXT NOT NULL

        )

    """)

# ==========================================
# DESCUENTOS LAVADORES
# ==========================================
def crear_tabla_descuentos_lavadores(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS descuentos_lavadores(

            id {id_type},

            fecha TEXT NOT NULL,

            responsable TEXT NOT NULL,

            concepto TEXT NOT NULL,

            valor INTEGER NOT NULL,

            usuario TEXT NOT NULL,

            hora TEXT NOT NULL

        )

    """)

# ==========================================
# PAGOS LAVADORES
# ==========================================
def crear_tabla_pagos_lavadores(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS pagos_lavadores(

            id {id_type},

            responsable TEXT NOT NULL,

            fecha_pago TEXT NOT NULL,

            total_bruto INTEGER NOT NULL,

            total_descuentos INTEGER NOT NULL,

            total_pagado INTEGER NOT NULL,

            usuario TEXT NOT NULL,

            hora TEXT NOT NULL

        )

    """)

# ==========================================
# CONFIGURACION TARIFAS
# ==========================================
def crear_tabla_tarifas(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS configuracion_tarifas(

            id {id_type},

            hora_moto INTEGER,

            hora_carro INTEGER,

            fraccion_moto INTEGER,

            fraccion_carro INTEGER,

            dia_moto INTEGER,

            dia_carro INTEGER,

            noche_moto INTEGER,

            noche_carro INTEGER,

            mensualidad_moto INTEGER,

            mensualidad_carro INTEGER,

            minutos_gracia INTEGER

        )

    """)


# ==========================================
# MENSUALIDADES
# ==========================================
def crear_tabla_mensualidades(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS mensualidades(

            id {id_type},

            placa TEXT NOT NULL,

            tipo TEXT NOT NULL,

            propietario TEXT,

            telefono TEXT,

            fecha_inicio TEXT,

            fecha_fin TEXT,

            estado TEXT NOT NULL

        )

    """)

# ==========================================
# PRODUCTOS CAFETERIA
# ==========================================
def crear_tabla_productos_cafeteria(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS productos_cafeteria(

            id {id_type},

            nombre TEXT NOT NULL,

            precio INTEGER NOT NULL,

            inventario INTEGER NOT NULL DEFAULT 0,

            stock_minimo INTEGER NOT NULL DEFAULT 5,

            estado TEXT NOT NULL DEFAULT 'Activo'

        )

    """)

# ==========================================
# VENTAS CAFETERIA
# ==========================================
def crear_tabla_ventas_cafeteria(
    c,
    id_type
):

    c.execute(f"""

        CREATE TABLE IF NOT EXISTS ventas_cafeteria(

            id {id_type},

            venta_id TEXT,

            fecha TEXT NOT NULL,

            producto_id INTEGER NOT NULL,

            producto TEXT NOT NULL,

            cantidad INTEGER NOT NULL,

            valor_unitario INTEGER NOT NULL,

            total INTEGER NOT NULL,

            placa TEXT,

            usuario TEXT

        )

    """)

# ==========================================
# MIGRACION INGRESOS
# ==========================================
def actualizar_tabla_ingresos(c):

    postgres = os.getenv(
        "DATABASE_URL"
    )

    columnas = [

        (
            "modalidad",
            "TEXT DEFAULT 'Hora'"
        ),

        (
            "puesto_casco",
            "INTEGER"
        ),

        (
            "cantidad_cascos",
            "INTEGER DEFAULT 0"
        )
    ]

    for nombre, tipo in columnas:

        if postgres:

            c.execute("""

                SELECT column_name

                FROM information_schema.columns

                WHERE table_name = 'ingresos'
                AND column_name = %s

            """, (
                nombre,
            ))

            existe = c.fetchone()

            if not existe:

                c.execute(
                    f"""
                    ALTER TABLE ingresos
                    ADD COLUMN {nombre} {tipo}
                    """
                )

        else:

            try:

                c.execute(
                    f"""
                    ALTER TABLE ingresos
                    ADD COLUMN {nombre} {tipo}
                    """
                )

            except Exception:

                pass

# ==========================================
# MIGRACION NOMINA
# ==========================================
def actualizar_tablas_nomina(c):

    postgres = os.getenv(
        "DATABASE_URL"
    )

    tablas = [

        (
            "lavados",
            "pagado",
            "INTEGER DEFAULT 0"
        ),

        (
            "lavados",
            "valor_comision",
            "INTEGER DEFAULT 0"
        ),

        (
            "lavados",
            "cortesia",
            "INTEGER DEFAULT 0"
        ),

        (
            "descuentos_lavadores",
            "pagado",
            "INTEGER DEFAULT 0"
        )
        

    ]

    for tabla, columna, tipo in tablas:

        if postgres:

            c.execute("""

                SELECT column_name

                FROM information_schema.columns

                WHERE table_name=%s

                AND column_name=%s

            """, (

                tabla,

                columna

            ))

            existe = c.fetchone()

            if not existe:

                c.execute(

                    f"""

                    ALTER TABLE {tabla}

                    ADD COLUMN {columna} {tipo}

                    """

                )

        else:

            try:

                c.execute(

                    f"""

                    ALTER TABLE {tabla}

                    ADD COLUMN {columna} {tipo}

                    """

                )

            except Exception:

                pass

    # ==========================================
    # INICIALIZAR VALOR COMISION
    # ==========================================

    try:

        c.execute("""

            UPDATE lavados

            SET valor_comision = valor

            WHERE valor_comision = 0
              AND valor > 0

        """)

    except Exception:

        pass       

# ==========================================
# MIGRACION CIERRES
# ==========================================
def actualizar_tabla_cierres(c):

    postgres = os.getenv("DATABASE_URL")

    columnas = [

        ("saldo_inicial", "INTEGER DEFAULT 0"),

        ("ingresos_dia", "INTEGER DEFAULT 0"),

        ("egresos_dia", "INTEGER DEFAULT 0"),

        ("saldo_final", "INTEGER DEFAULT 0")

    ]

    for nombre, tipo in columnas:

        if postgres:

            c.execute("""

                SELECT column_name

                FROM information_schema.columns

                WHERE table_name=%s

                AND column_name=%s

            """, (

                "cierres_caja",

                nombre

            ))

            existe = c.fetchone()

            if not existe:

                c.execute(

                    f"""

                    ALTER TABLE cierres_caja

                    ADD COLUMN {nombre} {tipo}

                    """

                )

        else:

            try:

                c.execute(

                    f"""

                    ALTER TABLE cierres_caja

                    ADD COLUMN {nombre} {tipo}

                    """

                )

            except Exception:

                pass

# ==========================================
# TARIFAS POR DEFECTO
# ==========================================
def insertar_tarifas_default(c):

    try:

        c.execute("""
            SELECT COUNT(*)
            FROM configuracion_tarifas
        """)

        resultado = c.fetchone()

        cantidad = (
            resultado[0]
            if not isinstance(
                resultado,
                dict
            )
            else list(
                resultado.values()
            )[0]
        )

        if cantidad == 0:

            c.execute("""

                INSERT INTO configuracion_tarifas(

                    hora_moto,
                    hora_carro,

                    fraccion_moto,
                    fraccion_carro,

                    dia_moto,
                    dia_carro,

                    noche_moto,
                    noche_carro,

                    mensualidad_moto,
                    mensualidad_carro,

                    minutos_gracia

                )

                VALUES (

                    1500,
                    3000,

                    500,
                    1000,

                    10000,
                    20000,

                    5000,
                    10000,

                    50000,
                    100000,

                    10

                )

            """)

    except Exception:

        pass


# ==========================================
# INDICES
# ==========================================
def crear_indices(c):

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_placa
        ON ingresos(placa)
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_estado
        ON ingresos(estado)
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_ingresos_estado_placa
        ON ingresos(estado, placa)
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_ingresos_estado_hora
        ON ingresos(estado, hora_ingreso)
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_hora_ingreso
        ON ingresos(hora_ingreso)
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_lavados_fecha
        ON lavados(fecha)
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_lavados_responsable
        ON lavados(responsable)
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_lavados_placa
        ON lavados(placa)
    """)