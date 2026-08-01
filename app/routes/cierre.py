from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    flash,

    send_file,

    jsonify
)

from flask_login import (
    current_user,
    login_required
)

from app.security import admin_required

from datetime import datetime
from io import BytesIO
from zoneinfo import ZoneInfo

import pandas as pd

from app.services.cierre_service import (

    obtener_metricas_cierre,

    guardar_cierre,

    obtener_historial_cierres

)

from app.services.gastos_service import (

    agregar_gasto,

    eliminar_gasto,

    obtener_gasto_por_id,

    actualizar_gasto

)


cierre_bp = Blueprint(

    "cierre",

    __name__
)


# ==========================================
# CIERRE CAJA
# ==========================================
@cierre_bp.route(

    "/cierre-caja",

    methods=["GET", "POST"]
)
@login_required
@admin_required
def cierre_caja():

    metricas = obtener_metricas_cierre()

    # ==========================================
    # GUARDAR CIERRE
    # ==========================================
    if request.method == "POST":

        observaciones = request.form.get(

            "observaciones",

            ""
        )

        ahora = datetime.now(
            ZoneInfo("America/Bogota")
        )

        fecha = ahora.strftime(
            "%Y-%m-%d"
        )

        hora_cierre = ahora.strftime(
            "%H:%M:%S"
        )

        try:

            guardar_cierre(

                fecha,

                metricas["total_parqueadero"],

                metricas["total_lavadero"],

                observaciones,

                current_user.usuario or current_user.id,

                hora_cierre
            )
        except ValueError as error:

            flash(
                str(error),
                "danger"
            )

            return redirect(
                url_for("cierre.cierre_caja")
            )

        flash(
            "Cierre de caja guardado correctamente.",
            "success"
        )

        return redirect(
            url_for(
                "cierre.cierre_caja"
            )
        )

    return render_template(

        "cierre_caja.html",

        total_parqueadero=
            metricas[
                "total_parqueadero"
            ],

        total_lavadero=
            metricas[
                "total_lavadero"
            ],

        total_general=
            metricas[
                "total_general"
            ],

        gastos=
            metricas[
                "gastos"
            ],

        total_gastos=
            metricas[
                "total_gastos"
            ],

        utilidad=
            metricas[
                "utilidad"
            ],

        pagos_lavadores=
            metricas[
                "pagos_lavadores"
            ],

        total_pago_lavadores=
            metricas[
                "total_pago_lavadores"
            ],

        dinero_esperado=
            metricas[
                "dinero_esperado"
            ],

        saldo_inicial=
            metricas["saldo_inicial"],

        ingresos_dia=
            metricas["ingresos_dia"],

        egresos_dia=
            metricas["egresos_dia"],

        saldo_actual=
            metricas["saldo_actual"],

        detalle_ingresos=
            metricas[
                "detalle_ingresos"],

        detalle_egresos=
            metricas[
                "detalle_egresos"]
    )


# ==========================================
# HISTORIAL CIERRES
# ==========================================
@cierre_bp.route(
    "/historial-cierres"
)
@login_required
def historial_cierres():

    historial = obtener_historial_cierres()

    total_general = sum(

        item["total_general"]

        for item in historial
    )

    return render_template(

        "historial_cierres.html",

        historial=historial,

        total_general=total_general
    )


# ==========================================
# EXPORTAR EXCEL
# ==========================================
@cierre_bp.route(
    "/exportar-cierres-excel"
)
@login_required
def exportar_cierres_excel():

    historial = obtener_historial_cierres()

    df = pd.DataFrame(historial)

    # ==========================================
    # RENOMBRAR COLUMNAS
    # ==========================================
    df = df.rename(columns={

        "fecha":
            "Fecha",

        "total_parqueadero":
            "Parqueadero",

        "total_lavadero":
            "Lavadero",

        "total_general":
            "Total General",

        "usuario":
            "Usuario",

        "hora_cierre":
            "Hora Cierre",

        "observaciones":
            "Observaciones"
    })

    # ==========================================
    # ELIMINAR ID
    # ==========================================
    if "id" in df.columns:

        df = df.drop(
            columns=["id"]
        )

    archivo = BytesIO()

    df.to_excel(
        archivo,
        index=False
    )

    archivo.seek(0)

    # ==========================================
    # DESCARGAR
    # ==========================================
    return send_file(

        archivo,

        as_attachment=True,

        download_name="historial_cierres.xlsx",

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ==========================================
# AGREGAR GASTO
# ==========================================
@cierre_bp.route(

    "/gastos/agregar",

    methods=["POST"]

)
@login_required
@admin_required
def agregar_gasto_ajax():

    try:

        concepto = request.form.get(

            "concepto",

            ""

        )

        valor = request.form.get(

            "valor",

            0

        )

        ahora = datetime.now(

            ZoneInfo("America/Bogota")

        )

        agregar_gasto(

            fecha=ahora.strftime("%Y-%m-%d"),

            concepto=concepto,

            valor=valor,

            usuario=current_user.usuario,

            hora=ahora.strftime("%H:%M:%S")

        )

        return jsonify({

            "success": True,

            "message": "Gasto registrado correctamente."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

# ==========================================
# ELIMINAR GASTO
# ==========================================
@cierre_bp.route(

    "/gastos/eliminar",

    methods=["POST"]

)
@login_required
@admin_required
def eliminar_gasto_ajax():

    try:

        datos = request.get_json()

        gasto_id = datos.get(

            "id"

        )

        if not gasto_id:

            return jsonify({

                "success": False,

                "message":
                "Id inválido."

            }), 400

        eliminar_gasto(

            gasto_id

        )

        return jsonify({

            "success": True,

            "message":
            "Gasto eliminado correctamente."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500

# ==========================================
# OBTENER GASTO
# ==========================================
@cierre_bp.route(

    "/gastos/<int:gasto_id>"

)
@login_required
@admin_required
def obtener_gasto_ajax(

    gasto_id

):

    gasto = obtener_gasto_por_id(

        gasto_id

    )

    if not gasto:

        return jsonify({

            "success": False,

            "message": "Gasto no encontrado."

        }), 404

    return jsonify({

        "success": True,

        "gasto": gasto

    })

# ==========================================
# EDITAR GASTO
# ==========================================
@cierre_bp.route(

    "/gastos/editar",

    methods=["POST"]

)
@login_required
@admin_required
def editar_gasto_ajax():

    try:

        datos = request.get_json()

        actualizar_gasto(

            gasto_id=datos.get("id"),

            concepto=datos.get("concepto"),

            valor=datos.get("valor")

        )

        return jsonify({

            "success": True,

            "message": "Gasto actualizado correctamente."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400