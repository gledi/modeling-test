from __future__ import annotations

from typing import Any

from flask import Flask

from modeling import db
from modeling.blueprints.core import core


def create_app(settings_override: dict[str, Any] = None) -> Flask:
    app = Flask(__name__)

    app.config.from_object("modeling.config")
    if settings_override:
        app.config.update(settings_override)

    db.init_app(app)

    app.register_blueprint(core)

    return app
