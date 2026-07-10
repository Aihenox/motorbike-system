from flask import jsonify
from flask import current_app
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import send_file
from openpyxl import Workbook
from io import BytesIO

from flask_login import current_user

from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    flash

)

from flask_login import (
    login_required
)

from app.security import admin_required

from app.services.cafeteria_service import (

    listar_productos_cafeteria,

    crear_producto_cafeteria,

    obtener_producto_cafeteria,

    actualizar_producto_cafeteria,

    eliminar_producto_cafeteria,

    obtener_inventario_actual,

    obtener_total_ventas_hoy,

    obtener_productos_vendidos_hoy,

    registrar_venta_cafeteria,

    obtener_resumen_ventas_hoy,

    obtener_historial_ventas_cafeteria,

    obtener_detalle_venta_cafeteria,

    obtener_historial_cafeteria_fechas

)


cafeteria_bp = Blueprint(

    "cafeteria",

    __name__

)

# ==========================================
# DASHBOARD CAFETERIA
# ==========================================
@cafeteria_bp.route(
    "/dashboard/cafeteria"
)
@login_required
def dashboard_cafeteria():

    inventario = obtener_inventario_actual()

    vendidos_hoy = obtener_productos_vendidos_hoy()

    total_ventas_hoy = obtener_total_ventas_hoy()

    productos = listar_productos_cafeteria()

    ultimas_ventas = (
        obtener_resumen_ventas_hoy()
    )

    return render_template(

        "cafeteria.html",

        inventario=inventario,

        vendidos_hoy=vendidos_hoy,

        total_ventas_hoy=total_ventas_hoy,

        productos=productos,

        ultimas_ventas=ultimas_ventas

    )

# ==========================================
# LISTADO PRODUCTOS
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/configuracion"
)
@login_required
@admin_required
def configuracion_cafeteria():

    productos = listar_productos_cafeteria()

    return render_template(

        "cafeteria_configuracion.html",

        productos=productos
    )


# ==========================================
# REGISTRAR VENTA AJAX
# ==========================================
@cafeteria_bp.route(
    "/registrar_venta",
    methods=["POST"]
)
@login_required
def registrar_venta_ajax():

    try:

        import json

        productos = json.loads(

            request.form.get(
                "productos",
                "[]"
            )

        )

        placa = request.form.get(
            "placa",
            ""
        ).strip().upper()

        ahora = datetime.now(
            ZoneInfo(
                "America/Bogota"
            )
        )

        fecha_db = ahora.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        resultado = registrar_venta_cafeteria(

            productos,

            placa,

            current_user.id,

            fecha_db
        )

        return jsonify({

            "success": True,

            "message":
                "Venta registrada correctamente"

        })

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception as e:

        current_app.logger.exception(
            "Error registrando venta de cafetería"
        )

        return jsonify({

            "success": False,

            "message": "Error interno del sistema"

        }), 500
    
# ==========================================
# CREAR PRODUCTO AJAX
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/api/crear",
    methods=["POST"]
)
@login_required
@admin_required
def crear_producto_ajax():

    try:

        crear_producto_cafeteria(

            request.form["nombre"],

            request.form["precio"],

            request.form["inventario"],

            request.form["stock_minimo"],

            request.form["estado"]

        )

        return jsonify({

            "success": True

        })

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception:

        return jsonify({

            "success": False,

            "message": "Error interno"

        }), 500
    
# ==========================================
# OBTENER PRODUCTO AJAX
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/api/producto/<int:producto_id>"
)
@login_required
def obtener_producto_ajax(
    producto_id
):

    producto = obtener_producto_cafeteria(
        producto_id
    )

    if not producto:

        return jsonify({

            "success": False

        }), 404

    if isinstance(
        producto,
        dict
    ):

        data = producto

    else:

        data = dict(producto)

    return jsonify({

        "success": True,

        "producto": data

    })

# ==========================================
# ACTUALIZAR PRODUCTO AJAX
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/api/editar",
    methods=["POST"]
)
@login_required
@admin_required
def editar_producto_ajax():

    try:

        actualizar_producto_cafeteria(

            request.form["producto_id"],

            request.form["nombre"],

            request.form["precio"],

            request.form["inventario"],

            request.form["stock_minimo"],

            request.form["estado"]

        )

        return jsonify({

            "success": True

        })

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception:

        return jsonify({

            "success": False,

            "message": "Error interno"

        }), 500
    
# ==========================================
# ELIMINAR PRODUCTO AJAX
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/api/eliminar/<int:producto_id>",
    methods=["DELETE"]
)
@login_required
@admin_required
def eliminar_producto_ajax(
    producto_id
):

    try:

        eliminar_producto_cafeteria(
            producto_id
        )

        return jsonify({

            "success": True

        })

    except Exception as e:

        current_app.logger.exception(
            "Error eliminando producto de cafetería"
        )

        return jsonify({

            "success": False,

            "message": "Error interno del sistema"

        }), 500
    
# ==========================================
# HISTORIAL VENTAS CAFETERIA
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/historial"
)
@login_required
def historial_cafeteria():

    ventas = (
        obtener_historial_ventas_cafeteria()
    )

    return render_template(

        "cafeteria_historial.html",

        ventas=ventas

    )

# ==========================================
# BUSCAR HISTORIAL CAFETERIA
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/buscar"
)
@login_required
def buscar_historial_cafeteria():

    fecha_inicio = request.args.get(
        "fecha_inicio"
    )

    fecha_fin = request.args.get(
        "fecha_fin"
    )

    ventas = (

        obtener_historial_cafeteria_fechas(

            fecha_inicio,

            fecha_fin

        )

    )

    return render_template(

        "cafeteria_historial.html",

        ventas=ventas

    )

# ==========================================
# DETALLE VENTA CAFETERIA
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/api/detalle_venta/<venta_id>"
)
@login_required
def detalle_venta_cafeteria(
    venta_id
):

    try:

        detalle = (
            obtener_detalle_venta_cafeteria(
                venta_id
            )
        )

        detalle_json = []

        for item in detalle:

            detalle_json.append({

                "producto": item["producto"],

                "cantidad": item["cantidad"],

                "valor_unitario": item["valor_unitario"],

                "total": item["total"]

            })

        return jsonify({

            "success": True,

            "detalle": detalle_json

        })

    except Exception as e:

        current_app.logger.exception(
            "Error consultando detalle de venta"
        )

        return jsonify({

            "success": False,

            "message": "Error interno del sistema"

        }), 500
    
# ==========================================
# EXPORTAR EXCEL CAFETERIA
# ==========================================
@cafeteria_bp.route(
    "/cafeteria/exportar_excel"
)
@login_required
def exportar_excel_cafeteria():

    ventas = (
        obtener_historial_ventas_cafeteria()
    )

    wb = Workbook()

    ws = wb.active

    ws.title = "Historial Cafeteria"

    # ======================================
    # ENCABEZADOS
    # ======================================
    ws.append([

        "Fecha",

        "Venta",

        "Productos",

        "Total",

        "Usuario"

    ])

    # ======================================
    # DATOS
    # ======================================
    for venta in ventas:

        ws.append([

            venta["fecha"],

            venta["placa"],

            venta["productos"],

            venta["total"],

            venta["usuario"]

        ])

    archivo = BytesIO()

    wb.save(
        archivo
    )

    archivo.seek(
        0
    )

    return send_file(

        archivo,

        as_attachment=True,

        download_name=
            "Historial_Cafeteria.xlsx",

        mimetype=
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
