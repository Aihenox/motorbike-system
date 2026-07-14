from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask import current_app

from flask_login import login_required

from app.services.salida_service import (
    procesar_salida,
    confirmar_salida
)

from app.utils.validators import (
    validar_id
)

salida_bp = Blueprint(
    "salida",
    __name__
)


# ==========================================
# VISTA SALIDA
# ==========================================
@salida_bp.route(
    "/salida",
    methods=["GET"]
)
@login_required
def salida():

    return render_template(
        "salida.html"
    )


# ==========================================
# PROCESAR SALIDA AJAX
# ==========================================
@salida_bp.route(
    "/procesar_salida",
    methods=["POST"]
)
@login_required
def procesar_salida_ajax():

    try:

        ticket = validar_id(
            request.form.get("ticket")
        )

        resultado = procesar_salida(
            ticket
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

        return jsonify({

            "success": False,

            "message": "Error interno del sistema"

        }), 500

# ==========================================
# CONFIRMAR SALIDA AJAX
# ==========================================
@salida_bp.route(
    "/confirmar_salida",
    methods=["POST"]
)
@login_required
def confirmar_salida_ajax():

    try:

        ticket = validar_id(
            request.form.get(
                "ticket"
            )
        )

        tarifa_especial = (

            request.form.get(

                "tarifa_especial"

            ) == "true"

        )

        valor_especial = request.form.get(

            "valor_especial"

        )

        resultado = confirmar_salida(

            ticket,

            tarifa_especial,

            valor_especial

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

        current_app.logger.exception(
            "Error confirmando salida"
        )

        return jsonify({

            "success": False,

            "message": "Error interno del sistema"

        }), 500