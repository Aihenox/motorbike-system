import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import (
    login_required
)

from app.services.parqueadero_service import (
    registrar_ingreso
)

from app.utils.validators import (
    validar_placa,
    validar_tipo_vehiculo
)


logger = logging.getLogger(__name__)


ingreso_bp = Blueprint(
    "ingreso",
    __name__
)


# ==========================================
# VISTA INGRESO
# ==========================================
@ingreso_bp.route(
    "/ingreso",
    methods=["GET"]
)
@login_required
def ingreso():

    ahora = datetime.now(

        ZoneInfo(
            "America/Bogota"
        )
    )

    permitir_noche = (

        ahora.hour >= 19

        or

        ahora.hour < 8
    )

    return render_template(

        "ingreso.html",

        permitir_noche=
            permitir_noche
    )


# ==========================================
# REGISTRAR INGRESO AJAX
# ==========================================
@ingreso_bp.route(
    "/registrar_ingreso",
    methods=["POST"]
)
@login_required
def registrar_ingreso_ajax():

    try:

        placa = validar_placa(
            request.form.get("placa")
        )

        tipo = validar_tipo_vehiculo(
            request.form.get("tipo")
        )

        modalidad = request.form.get(
            "modalidad",
            "Hora"
        )

        puesto_casco = request.form.get(
            "puesto_casco"
        )

        cantidad_cascos = request.form.get(
            "cantidad_cascos",
            0
        )

        # ==========================
        # NORMALIZAR DATOS
        # ==========================
        if puesto_casco == "":

            puesto_casco = None

        if cantidad_cascos in (
            "",
            None
        ):

            cantidad_cascos = 0

        cantidad_cascos = int(
            cantidad_cascos
        )

        resultado = registrar_ingreso(

            placa,

            tipo,

            modalidad,

            puesto_casco,

            cantidad_cascos
        )

        return jsonify(
            resultado
        )

    except ValueError as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    except Exception:

        logger.exception(
            "Error registrando ingreso"
        )

        return jsonify({
            "success": False,
            "message": "Error interno del sistema"
        }), 500