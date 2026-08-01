from flask import (
    Blueprint,
    render_template,
    jsonify,
    request
)

from flask_login import (
    login_required,
    current_user
)
from app.services.nomina_service import (
    obtener_nomina,
    obtener_detalle,
    liquidar,
    registrar_descuento
)

from datetime import datetime


nomina_bp = Blueprint("nomina", __name__)

@nomina_bp.route("/nomina")
@login_required
def nomina():
    datos = obtener_nomina()

    return render_template(
        "nomina.html",
        resumen=datos["resumen"],
        empleados=datos["empleados"]
    )

@nomina_bp.route("/nomina/detalle/<responsable>")
@login_required
def detalle_nomina(responsable):

    datos = obtener_detalle(responsable)

    return jsonify(datos)

@nomina_bp.route("/nomina/liquidar", methods=["POST"])
@login_required
def liquidar_nomina():

    datos = request.get_json()

    ahora = datetime.now()

    resultado = liquidar(

        responsable=datos["responsable"],

        fecha_pago=ahora.strftime("%Y-%m-%d"),

        usuario=current_user.usuario,

        hora=ahora.strftime("%H:%M:%S")

    )

    return jsonify({

        "success": True,

        "resultado": resultado

    })

@nomina_bp.route("/nomina/descuento", methods=["POST"])
@login_required
def registrar_descuento_nomina():

    try:

        datos = request.get_json()

        responsable = datos.get("responsable")
        concepto = datos.get("concepto")
        valor = datos.get("valor")

        if not responsable:
            return jsonify({
                "success": False,
                "mensaje": "Responsable requerido."
            }), 400

        if not concepto:
            return jsonify({
                "success": False,
                "mensaje": "Debe ingresar un concepto."
            }), 400

        if not valor or int(valor) <= 0:
            return jsonify({
                "success": False,
                "mensaje": "El valor debe ser mayor que cero."
            }), 400

        resultado = registrar_descuento(
            responsable=responsable,
            concepto=concepto,
            valor=valor,
            usuario=current_user.usuario
        )

        return jsonify(resultado)

    except Exception as e:

        return jsonify({

            "success": False,

            "mensaje": str(e)

        }), 500