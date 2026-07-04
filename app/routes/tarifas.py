from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from flask_login import (
    login_required
)

from app.security import admin_required

from app.services.tarifas_service import (
    obtener_tarifas,
    actualizar_tarifas
)


tarifas_bp = Blueprint(
    "tarifas",
    __name__
)


# ==========================================
# CONFIGURACION TARIFAS
# ==========================================
@tarifas_bp.route(
    "/tarifas",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def tarifas():

    if request.method == "POST":

        try:

            actualizar_tarifas(

                int(request.form["hora_moto"]),
                int(request.form["hora_carro"]),

                int(request.form["noche_moto"]),
                int(request.form["noche_carro"]),

                int(request.form["mensualidad_moto"]),
                int(request.form["mensualidad_carro"]),

                int(request.form["minutos_gracia"])
            )

        except (KeyError, TypeError, ValueError) as error:

            flash(
                str(error),
                "danger"
            )

            return redirect(
                "/tarifas"
            )

        flash(
            "Tarifas actualizadas correctamente",
            "success"
        )

        return redirect(
            "/tarifas"
        )

    tarifas = obtener_tarifas()

    if tarifas:

        tarifas = dict(
            tarifas
        )

    return render_template(

        "tarifas.html",

        tarifas=tarifas
    )
