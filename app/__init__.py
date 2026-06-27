from datetime import datetime

from flask import Flask

from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    config_class.init_app(app)
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    @app.context_processor
    def inject_template_globals():
        return {"current_year": datetime.now().year}

    from .routes.main import main_bp
    from .routes.pdf import pdf_bp
    from .routes.image import image_bp
    from .routes.text import text_bp
    from .routes.dev import dev_bp
    from .routes.calc import calc_bp
    from .routes.catalog import catalog_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(pdf_bp, url_prefix="/pdf")
    app.register_blueprint(image_bp, url_prefix="/image")
    app.register_blueprint(text_bp, url_prefix="/text")
    app.register_blueprint(dev_bp, url_prefix="/dev")
    app.register_blueprint(calc_bp, url_prefix="/calculators")
    app.register_blueprint(catalog_bp)
    return app
