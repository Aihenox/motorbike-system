from app.repositories.nomina_repository import (
    obtener_resumen_nomina,
    obtener_detalle_nomina,
    obtener_descuentos_pendientes,
    obtener_ultimo_pago,
    liquidar_nomina,
    registrar_descuento_nomina
)

def obtener_nomina():

    empleados = obtener_resumen_nomina()

    resumen = {
        "empleados": len(empleados),
        "bruto": 0,
        "descuentos": 0,
        "neto": 0
    }

    for empleado in empleados:
        resumen["bruto"] += empleado["comision"]
        resumen["descuentos"] += empleado["descuentos"]
        resumen["neto"] += empleado["total"]

    return {
        "resumen": resumen,
        "empleados": empleados
    }

def obtener_detalle(responsable):

    detalle = obtener_detalle_nomina(responsable)

    descuentos = obtener_descuentos_pendientes(responsable)

    ultimo_pago = obtener_ultimo_pago(responsable)

    total_lavados = 0
    total_comision = 0
    total_servicios = 0
    total_descuentos = 0

    desde = None
    hasta = None

    for dia in detalle:

        total_lavados += dia["valor_lavados"]
        total_comision += dia["comision"]
        total_servicios += dia["vehiculos"]

        fecha = dia["fecha"]

        if desde is None or fecha < desde:
            desde = fecha

        if hasta is None or fecha > hasta:
            hasta = fecha

    for descuento in descuentos:

        total_descuentos += float(descuento["valor"] or 0)

    return {

        "resumen": {

            "responsable": responsable,
            "desde": desde or "",
            "hasta": hasta or "",
            "ultimo_pago": ultimo_pago or "Sin pagos",
            "dias": len(detalle),
            "lavados": total_servicios,
            "valor_lavados": total_lavados,
            "comision": total_comision,
            "descuentos": total_descuentos,
            "neto": total_comision - total_descuentos

        },

        "detalle": detalle,

        "descuentos": descuentos

    }

def liquidar(
    responsable,
    fecha_pago,
    usuario,
    hora
):

    return liquidar_nomina(

        responsable,

        fecha_pago,

        usuario,

        hora

    )

from datetime import datetime


def registrar_descuento(
    responsable,
    concepto,
    valor,
    usuario
):

    ahora = datetime.now()

    fecha = ahora.strftime("%Y-%m-%d")

    hora = ahora.strftime("%H:%M:%S")

    registrar_descuento_nomina(

        responsable=responsable,

        concepto=concepto.strip(),

        valor=int(valor),

        fecha=fecha,

        usuario=usuario,

        hora=hora

    )

    return {

        "success": True

    }