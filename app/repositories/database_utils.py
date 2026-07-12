# ==========================================
# OBTENER CAMPO
# ==========================================
def obtener_campo(
    fila,
    indice,
    nombre
):
    """
    Obtiene un valor de una fila compatible con
    SQLite (tuple) y PostgreSQL (dict).
    """

    if isinstance(
        fila,
        dict
    ):

        return fila[nombre]

    return fila[indice]

