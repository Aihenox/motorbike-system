from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask import jsonify
from app.services.mensualidades_service import (
    buscar_mensualidad_activa
)

from flask_login import (
    login_required
)

from app.security import admin_required

from app.services.mensualidades_service import (
    listar_mensualidades,
    crear_mensualidad,
    obtener_mensualidad,
    actualizar_mensualidad,
    eliminar_mensualidad
)


mensualidades_bp = Blueprint(
    "mensualidades",
    __name__
)


# ==========================================
# LISTADO MENSUALIDADES
# ==========================================
@mensualidades_bp.route(
    "/mensualidades"
)
@login_required
def mensualidades():

    registros = listar_mensualidades()

    imprimir = request.args.get(

        "imprimir",

        type=int

    )

    mensualidad_ticket = None

    if imprimir:

        mensualidad_ticket = obtener_mensualidad(

            imprimir

        )

    return render_template(

        "mensualidades.html",

        registros=registros,

        mensualidad_ticket=mensualidad_ticket

    )

# ==========================================
# NUEVA MENSUALIDAD
# ==========================================
@mensualidades_bp.route(
    "/mensualidades/nuevo",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def nueva_mensualidad():

    if request.method == "POST":

        try:

            id_mensualidad = crear_mensualidad(

                request.form["placa"],

                request.form["tipo"],

                request.form["propietario"],

                request.form["telefono"],

                request.form["fecha_inicio"],

                request.form["fecha_fin"],

                request.form["estado"]
            )

        except (KeyError, ValueError) as error:

            flash(
                str(error),
                "danger"
            )

            return redirect(
                url_for("mensualidades.nueva_mensualidad")
            )

        flash(
            "Mensualidad registrada correctamente",
            "success"
        )

        return redirect(

            url_for(

                "mensualidades.mensualidades",

                imprimir=id_mensualidad

            )

        )

    return render_template(
        "mensualidad_form.html"
    )

# ==========================================
# EDITAR MENSUALIDAD
# ==========================================
@mensualidades_bp.route(
    "/mensualidades/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def editar_mensualidad(id):

    mensualidad = obtener_mensualidad(
        id
    )

    if request.method == "POST":

        try:

            actualizar_mensualidad(

                id,

                request.form["placa"],

                request.form["tipo"],

                request.form["propietario"],

                request.form["telefono"],

                request.form["fecha_inicio"],

                request.form["fecha_fin"],

                request.form["estado"]
            )

        except (KeyError, ValueError) as error:

            flash(
                str(error),
                "danger"
            )

            return redirect(
                url_for(
                    "mensualidades.editar_mensualidad",
                    id=id
                )
            )

        flash(
            "Mensualidad actualizada correctamente"
        )

        return redirect(
            url_for(
                "mensualidades.mensualidades"
            )
        )

    return render_template(

        "mensualidad_form.html",

        mensualidad=mensualidad
    )

# ==========================================
# ELIMINAR MENSUALIDAD
# ==========================================
@mensualidades_bp.route(
    "/mensualidades/eliminar/<int:id>",
    methods=["POST"]
)
@login_required
@admin_required
def eliminar_mensualidad_route(id):

    eliminar_mensualidad(
        id
    )

    flash(
        "Mensualidad eliminada correctamente"
    )

    return redirect(
        url_for(
            "mensualidades.mensualidades"
        )
    )

# ==========================================
# CONSULTAR MENSUALIDAD AJAX
# ==========================================
@mensualidades_bp.route(
    "/api/mensualidad/<placa>"
)
@login_required
def consultar_mensualidad(
    placa
):

    mensualidad = buscar_mensualidad_activa(
        placa
    )

    return jsonify({

        "mensualidad": mensualidad is not None

    })

# ==========================================
# PRUEBA TICKET MENSUALIDAD
# ==========================================
@mensualidades_bp.route(
    "/mensualidades/test-ticket"
)
@login_required
def test_ticket_mensualidad():

    return render_template(
        "ticket_mensualidad_test.html"
    )

# ==========================================
# TICKET MENSUALIDAD
# ==========================================
@mensualidades_bp.route(
    "/mensualidades/ticket/<int:id>"
)
@login_required
def ticket_mensualidad(id):

    mensualidad = obtener_mensualidad(id)

    if not mensualidad:

        flash(
            "La mensualidad no existe.",
            "danger"
        )

        return redirect(
            url_for(
                "mensualidades.mensualidades"
            )
        )

    return render_template(

        "ticket_mensualidad.html",

        mensualidad=mensualidad

    )