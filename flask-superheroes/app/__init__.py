from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'
    
    # Initialize database
    db.init_app(app)
    
    from . import models
    
    # Import and register blueprints
    from .routes.heroes import heroes_bp
    from .routes.powers import powers_bp
    from .routes.hero_powers import hero_powers_bp
    
    app.register_blueprint(heroes_bp)
    app.register_blueprint(powers_bp)
    app.register_blueprint(hero_powers_bp)
    
    # Add a test route to verify server is working
    @app.route('/')
    def index():
        return {'message': 'Flask Superheroes API is running!', 'endpoints': [
            '/heroes',
            '/heroes/<id>',
            '/powers',
            '/powers/<id>',
            '/hero_powers'
        ]}
    
    return app