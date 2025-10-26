"""Routes package for organizing Flask blueprints"""

from webapp.routes.ui_routes import ui_bp
from webapp.routes.api_player_routes import api_players_bp
from webapp.routes.api_game_routes import api_games_bp
from webapp.routes.api_index_routes import api_index_bp

__all__ = [
    'ui_bp',
    'api_players_bp',
    'api_games_bp',
    'api_index_bp',
]