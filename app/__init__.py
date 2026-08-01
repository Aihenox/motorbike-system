import os

from flask import Flask

from flask_login import LoginManager

from config import config

from database import crear_bd

from app.services.auth_service import cargar_usuario

from app.errors import (
    register_error_handlers
)

from app.security import init_security


# ==========================================
# LOGIN MANAGER
# ==========================================
login_manager = LoginManager()

login_manager.login_view = "auth.login"

login_manager.login_message = (
    "Debe iniciar sesión para continuar."
)


# ==========================================
# USER LOADER
# ==========================================
@login_manager.user_loader
def load_user(user_id):

    return cargar_usuario(user_id)


# ==========================================
# CREAR APP
# ==========================================
def create_app():

    app = Flask(__name__)

    # ==========================================
    # CONFIGURACIÓN
    # ==========================================
    env = os.getenv(
        "FLASK_ENV",
        "development"
    )

    app.config.from_object(
        config.get(
            env,
            config["default"]
        )
    )

    if env == "production" and app.config["SECRET_KEY"] in {
        None,
        "",
        "dev-only-change-me",
        "motorbike-secret-key",
        "change-me"
    }:

        raise RuntimeError(
            "SECRET_KEY debe configurarse con un valor seguro en producción."
        )

    # ==========================================
    # LOGIN
    # ==========================================
    login_manager.init_app(app)

    init_security(app)

    # ==========================================
    # CREAR BASE DE DATOS
    # ==========================================
    with app.app_context():

        crear_bd()

    # ==========================================
    # IMPORTAR BLUEPRINTS
    # ==========================================
    from app.routes.auth import auth_bp

    from app.routes.dashboard import dashboard_bp

    from app.routes.ingreso import ingreso_bp

    from app.routes.salida import salida_bp

    from app.routes.activos import activos_bp

    from app.routes.editar import editar_bp

    from app.routes.eliminar import eliminar_bp

    from app.routes.historial import historial_bp

    from app.routes.lavadero import lavadero_bp

    from app.routes.parqueadero import parqueadero_bp

    from app.routes.cierre import cierre_bp

    from app.routes.recibos import recibos_bp

    from app.routes.tarifas import tarifas_bp

    from app.routes.mensualidades import mensualidades_bp

    from app.routes.cafeteria import cafeteria_bp

    from app.routes.nomina import nomina_bp

    # ==========================================
    # REGISTRAR BLUEPRINTS
    # ==========================================
    blueprints = [
        auth_bp,
        dashboard_bp,
        ingreso_bp,
        salida_bp,
        activos_bp,
        editar_bp,
        eliminar_bp,
        historial_bp,
        lavadero_bp,
        parqueadero_bp,
        cierre_bp,
        recibos_bp,
        tarifas_bp,
        mensualidades_bp,
        cafeteria_bp,
        nomina_bp
    ]

    for blueprint in blueprints:

        app.register_blueprint(
            blueprint
        )

    # ==========================================
    # MANEJO DE ERRORES
    # ==========================================
    register_error_handlers(app)

    return app
