import os

from dotenv import dotenv_values
from flask import Flask
import structlog

from constants import APP_LOGGER, STATE_NAME
from helpers import remove_flask_logging
from project_config import ProjectConfig
from routes import (ashirt, dev)
from services import AShirtRequestsService
from services import set_service, svc
from actions.ocr import test_vision_api


def create_app() -> Flask:
    app = Flask(__name__)

    full_env = {
        **dotenv_values(".env"),
        **os.environ
    }
    cfg = ProjectConfig.from_dict(full_env)
    app.config[STATE_NAME] = cfg
    app.config[APP_LOGGER] = structlog.get_logger()

    set_service(
        AShirtRequestsService(cfg.backend_url, cfg.access_key, cfg.secret_key_b64)
    )

    # Test connection to AShirt backend
    try:
        svc().check_connection()
        app.config[APP_LOGGER].msg("AShirt backend connection successful", backend_url=cfg.backend_url)
    except Exception as e:
        app.config[APP_LOGGER].error("Failed to connect to AShirt backend",
                                     backend_url=cfg.backend_url,
                                     error=str(e))

    # Test Google Cloud Vision API credentials
    try:
        test_vision_api()
        app.config[APP_LOGGER].msg("Google Cloud Vision API credentials verified")
    except Exception as e:
        app.config[APP_LOGGER].error("Failed to verify Google Cloud Vision API credentials",
                                     error=str(e))

    app.register_blueprint(ashirt.bp) # Add normal routes
    if cfg.dev_mode:
        app.config[APP_LOGGER].msg("Adding dev routes")
        app.register_blueprint(dev.bp) # Add dev routes

    # tweak logging settings
    remove_flask_logging(app)
    return app


if __name__ == "__main__":
    app = create_app()
    try:
        app.config[APP_LOGGER].msg("App Starting")
        app.run(host="0.0.0.0", port=app.config[STATE_NAME].port)
    finally:
        app.config[APP_LOGGER].msg("App Exiting")
