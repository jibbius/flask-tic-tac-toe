"""Flask application factory"""
import os
from flask import Flask
from flask_migrate import Migrate

from webapp.models.base import db
from webapp.models.player import Player
from webapp.csv_sync import PlayerCsv


def create_app(config):
    """
    Create and configure the Flask application.
    
    Args:
        config: Configuration object for the app
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Initialize database
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    Migrate(app, db)
    
    # Initialize player data from CSV if needed
    _initialize_player_data()
    
    # Set up navigation
    _setup_navigation(app)
    
    # Register blueprints
    _register_blueprints(app)
    
    return app


def _initialize_player_data():
    """Initialize player data from CSV file if database is empty"""
    csv_filename = 'seed_data_players.csv'
    csv_path = os.path.join(os.path.dirname(__file__), csv_filename)
    player_csv = PlayerCsv(csv_path)
    existing_data = Player.get_players()
    
    if not existing_data:
        player_csv.synchronize_players_from_file()
        
        # If the Data has any further updates, write these to the file:
        # Player.e_added.add_listener(player_csv.synchronize_players_to_file)
        # Player.e_updated.add_listener(player_csv.synchronize_players_to_file)


def _setup_navigation(app):
    """Configure navigation items for Jinja templates"""
    app.jinja_env.globals.update(navigation_items=[
        {"label": "Home", "function": "ui.root"},
        {"label": "New game", "function": "ui.games_new"},
        {"label": "Existing games", "function": "ui.games_get_all"},
        # {"label": "Statistics", "function": "ui.stats"},
        {"label": "About", "function": "ui.about"},
        {"label": "API Index", "function": "api_index.index"}
    ])


def _register_blueprints(app):
    """Register all application blueprints"""
    from webapp.routes.ui_routes import ui_bp
    from webapp.routes.api_player_routes import api_players_bp
    from webapp.routes.api_game_routes import api_games_bp
    from webapp.routes.api_index_routes import api_index_bp
    
    app.register_blueprint(ui_bp)
    app.register_blueprint(api_players_bp, url_prefix='/api')
    app.register_blueprint(api_games_bp, url_prefix='/api')
    app.register_blueprint(api_index_bp)