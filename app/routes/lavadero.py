from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    send_file,

    jsonify
)


import openpyxl

from io import BytesIO

from datetime import (
    datetime
)
from zoneinfo import ZoneInfo

from flask_login import (
    login_required
)

from flask import current_app

from app.security import admin_required

from app.services.lavadero_service import (

    registrar_lavado,

    listar_lavados,

    obtener_historial_lavados,

    obtener_metricas_lavadero,

    obtener_estadisticas_responsables,

    obtener_lavado_por_id,

    actualizar_lavado,

    eliminar_lavado,

    contar_lavados_placa_db
)

from app.services.dashboard_lavadero_service import (
    obtener_dashboard
)

from app.services.historial_lavadero_service import (

    listar_historial_lavadero,

    obtener_total_lavadero
)

from werkzeug.security import (
    check_password_hash
)

from app.repositories.auth_repository import (
    obtener_usuario_por_username
)

from app.utils.validators import (
    validar_placa,
    validar_tipo_vehiculo,
    validar_tipo_lavado,
    validar_valor,
    validar_responsable
)

lavadero_bp = Blueprint(
    "lavadero",
    __name__
)


# ==========================================
# DASHBOARD LAVADERO
# ==========================================
@lavadero_bp.route(
    "/dashboard/lavadero"
)
@login_required
def dashboard_lavadero():

    metricas = obtener_metricas_lavadero()

    lavados = listar_lavados()

    # ==========================================
    # FORMATEAR FECHAS
    # ==========================================
    for lavado in lavados:

        try:

            fecha = lavado["fecha"]

            if isinstance(
                fecha,
                str
            ):

                fecha = datetime.fromisoformat(
                    fecha
                )

            lavado["fecha"] = fecha.strftime(
                "%d/%m/%Y %H:%M"
            )

        except:

            pass

    return render_template(

        "dashboard_lavadero.html",

        lavados_motos=metricas.get(
            "lavados_motos",
            0
        ),

        lavados_carros=metricas.get(
            "lavados_carros",
            0
        ),

        total_servicios=metricas.get(
            "dinero_generado",
            0
        ),

        lavados=lavados
    )


# ==========================================
# FORMULARIO LAVADERO
# ==========================================
@lavadero_bp.route(
    "/lavadero"
)
@login_required
def lavadero():

    lavados = listar_lavados()

    return render_template(

        "lavadero.html",

        lavados=lavados
    )


# ==========================================
# REGISTRAR LAVADO AJAX
# ==========================================

@lavadero_bp.route(
    "/registrar_lavado",
    methods=["POST"]
)
@login_required
def registrar_lavado_ajax():

    try:

        placa = validar_placa(
            request.form.get("placa")
        )

        vehiculo = validar_tipo_vehiculo(
            request.form.get("vehiculo")
        )

        tipo_lavado = validar_tipo_lavado(
            request.form.get("tipo_lavado")
        )

        valor = validar_valor(
            request.form.get("valor")
        )

        responsable = validar_responsable(
            request.form.get("responsable")
        )

        ahora = datetime.now(
            ZoneInfo("America/Bogota")
        )

        fecha_db = ahora.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        
        resultado = registrar_lavado(

            placa,

            vehiculo,

            tipo_lavado,

            valor,

            responsable,

            fecha_db
        )

        fecha_ticket = ahora.strftime(
            "%d/%m/%Y %H:%M"
        )

        return {

            "success": True,

            "gratis": resultado["gratis"],

            "placa": placa,

            "vehiculo": vehiculo,

            "tipo_lavado": tipo_lavado,

            "responsable": responsable,

            "valor": f"{int(resultado['valor']):,}",

            "fecha": fecha_ticket
        }

    except ValueError as e:

        return {
            "success": False,
            "message": str(e)
        }, 400

    except Exception:

        return {
            "success": False,
            "message": "Error interno del sistema"
        }, 500


# ==========================================
# HISTORIAL LAVADERO
# ==========================================
@lavadero_bp.route(
    "/historial/lavadero"
)
@login_required
def historial_lavadero():

    placa = request.args.get(
        "placa",
        ""
    )

    fecha_inicio = request.args.get(
        "fecha_inicio",
        ""
    )

    fecha_fin = request.args.get(
        "fecha_fin",
        ""
    )

    responsable = request.args.get(
        "responsable",
        ""
    )

    historial = listar_historial_lavadero(

        placa,

        fecha_inicio,

        fecha_fin,

        responsable
    )

    total = obtener_total_lavadero(

        placa,

        fecha_inicio,

        fecha_fin,

        responsable
    )

    return render_template(

        "historial_lavadero.html",

        historial=historial,

        total=total,

        placa=placa,

        fecha_inicio=fecha_inicio,

        fecha_fin=fecha_fin,

        responsable=responsable
    )


# ==========================================
# EXPORTAR EXCEL HISTORIAL LAVADERO
# ==========================================
@lavadero_bp.route(
    "/historial/lavadero/excel"
)
@login_required
def exportar_excel_lavadero():

    placa = request.args.get(
        "placa",
        ""
    )

    fecha_inicio = request.args.get(
        "fecha_inicio",
        ""
    )

    fecha_fin = request.args.get(
        "fecha_fin",
        ""
    )

    responsable = request.args.get(
        "responsable",
        ""
    )

    historial = obtener_historial_lavados(

        placa,

        fecha_inicio,

        fecha_fin,

        responsable
    )

    wb = openpyxl.Workbook()

    ws = wb.active

    ws.title = "Historial Lavadero"

    encabezados = [

        "Fecha",

        "Vehículo",

        "Placa",

        "Responsable",

        "Tipo lavado",

        "Valor"
    ]

    ws.append(
        encabezados
    )

    for item in historial:

        ws.append([

            item["fecha"],

            item["vehiculo"],

            item["placa"],

            item["responsable"],

            item["tipo_lavado"],

            item["valor"]
        ])

    for columna in ws.columns:

        longitud = 0

        columna_letra = columna[0].column_letter

        for celda in columna:

            try:

                if len(str(celda.value)) > longitud:

                    longitud = len(
                        str(celda.value)
                    )

            except:

                pass

        ws.column_dimensions[
            columna_letra
        ].width = longitud + 5

    archivo = BytesIO()

    wb.save(archivo)

    archivo.seek(0)

    return send_file(

        archivo,

        as_attachment=True,

        download_name=
        "historial_lavadero.xlsx",

        mimetype=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ==========================================
# OBTENER LAVADO AJAX
# ==========================================
@lavadero_bp.route(
    "/lavadero/obtener/<int:lavado_id>"
)
@login_required
def obtener_lavado_ajax(
    lavado_id
):

    try:

        lavado = obtener_lavado_por_id(
            lavado_id
        )

        if not lavado:

            return jsonify({

                "success": False,

                "message":
                    "Lavado no encontrado"

            }), 404

        # PostgreSQL
        if isinstance(
            lavado,
            dict
        ):

            datos = {

                "id":
                    lavado["id"],

                "placa":
                    lavado["placa"],

                "vehiculo":
                    lavado["vehiculo"],

                "tipo_lavado":
                    lavado["tipo_lavado"],

                "valor":
                    lavado["valor"],

                "responsable":
                    lavado["responsable"]
            }

        # SQLite
        else:

            datos = {

                "id":
                    lavado[0],

                "placa":
                    lavado[1],

                "vehiculo":
                    lavado[2],

                "tipo_lavado":
                    lavado[3],

                "valor":
                    lavado[4],

                "responsable":
                    lavado[5]
            }

        return jsonify({

            "success": True,

            "lavado": datos
        })

    except Exception:

        current_app.logger.exception(
            "Error obteniendo lavado"
        )

        return jsonify({

            "success": False,

            "message":
                "Error interno"

        }), 500
    
# ==========================================
# ACTUALIZAR LAVADO AJAX
# ==========================================
@lavadero_bp.route(
    "/lavadero/actualizar/<int:lavado_id>",
    methods=["POST"]
)
@login_required
@admin_required
def actualizar_lavado_ajax(
    lavado_id
):

    try:

        datos = request.get_json()

        placa = validar_placa(
            datos.get("placa")
        )

        vehiculo = validar_tipo_vehiculo(
            datos.get("vehiculo")
        )

        tipo_lavado = validar_tipo_lavado(
            datos.get("tipo_lavado")
        )

        valor = validar_valor(
            datos.get("valor")
        )

        responsable = validar_responsable(
            datos.get("responsable")
        )

        actualizar_lavado(

            lavado_id,

            placa,

            vehiculo,

            tipo_lavado,

            valor,

            responsable
        )

        return jsonify({

            "success": True,

            "message":
                "Lavado actualizado"

        })

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception:

        current_app.logger.exception(
            "Error actualizando lavado"
        )

        return jsonify({

            "success": False,

            "message":
                "Error interno"

        }), 500
    


# ==========================================
# ELIMINAR LAVADO
# ==========================================
@lavadero_bp.route(
    "/eliminar-lavado/<int:lavado_id>",
    methods=["POST"]
)
@login_required
@admin_required
def eliminar_lavado_route(
    lavado_id
):

    try:

        eliminar_lavado(
            lavado_id
        )

        return jsonify({

            "success": True
        })

    except Exception as e:

        current_app.logger.exception(
            "Error eliminando registro de lavadero"
        )

        return jsonify({

            "success": False,

            "message": "Error interno del sistema"
        }), 500
    
# ==========================================
# CONSULTAR LAVADO GRATIS
# ==========================================
@lavadero_bp.route(
    "/api/lavado-gratis/<placa>"
)
@login_required
def consultar_lavado_gratis(
    placa
):

    cantidad = contar_lavados_placa_db(
        placa
    )

    siguiente = cantidad + 1

    return jsonify({

        "cantidad": cantidad,

        "gratis": (
            siguiente % 5 == 0
        )

    })

# ==========================================
# VALIDAR ADMINISTRADOR
# ==========================================
@lavadero_bp.route(
    "/lavadero/validar_admin",
    methods=["POST"]
)
@login_required
def validar_admin():

    try:

        datos = request.get_json()

        password = datos.get(
            "password",
            ""
        )

        admin = obtener_usuario_por_username(
            "admin"
        )

        print("\n========== ADMIN ==========")
        print(admin)
        print(type(admin))
        print("===========================\n")

        if not admin:

            return jsonify({

                "success": False,

                "message":
                "Administrador no encontrado"

            }), 404


        # PostgreSQL
        if isinstance(admin, dict):

            password_hash = (
                admin["password"]
            )

        # SQLite
        else:

            password_hash = (
                admin[2]
            )

        if check_password_hash(
            password_hash,
            password
        ):

            return jsonify({

                "success": True

            })

        return jsonify({

            "success": False,

            "message":
            "Contraseña incorrecta"

        }), 401

    except Exception:

        current_app.logger.exception(
            "Error validando administrador"
        )

        return jsonify({

            "success": False,

            "message":
            "Error interno"

        }), 500
    

# ==========================================
# DASHBOARD LAVADERO AJAX
# ==========================================
@lavadero_bp.route(
    "/lavadero/dashboard",
    methods=["POST"]
)
@login_required
def dashboard_lavadero_ajax():

    datos = request.get_json()

    dashboard = obtener_dashboard(

        datos

    )

    return jsonify({

        "success": True,

        **dashboard

    })