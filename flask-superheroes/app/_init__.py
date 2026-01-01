from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import and register blueprints
    from .routes.heroes import heroes_bp
    from .routes.powers import powers_bp
    from .routes.hero_powers import hero_powers_bp
    
    app.register_blueprint(heroes_bp)
    app.register_blueprint(powers_bp)
    app.register_blueprint(hero_powers_bp)
    
    return app