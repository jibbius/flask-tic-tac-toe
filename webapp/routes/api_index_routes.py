"""API index/documentation routes"""

from flask import Blueprint, render_template

from webapp.helpers import ApiEndpoint

api_index_bp = Blueprint('api_index', __name__)


@api_index_bp.route('/api_index')
def index():
    """API documentation index page"""
    api_endpoint_list = [
        # Player endpoints
        ApiEndpoint(
            model='player',
            title='Get all Players',
            handle='api_players.get_all',
            method='GET',
            template='api_players_get_all.html'
        ),
        ApiEndpoint(
            model='player',
            title='Get Player by id',
            handle='api_players.get_by_id',
            method='GET',
            template='api_players_get_by_id.html',
            default_params={'player_id': '.PLAYER_ID.'}
        ),
        ApiEndpoint(
            model='player',
            title='Add Player',
            handle='api_players.add',
            method='POST',
            template='api_players_add.html'
        ),
        ApiEndpoint(
            model='player',
            title='Update Player',
            handle='api_players.update_by_id',
            method='PUT',
            template='api_players_update_by_id.html',
            default_params={'player_id': '.PLAYER_ID.'}
        ),
        # Game endpoints
        ApiEndpoint(
            model='game',
            title='Get all Games',
            handle='api_games.get_all',
            method='GET',
            template='api_games_get_all.html'
        ),
        ApiEndpoint(
            model='game',
            title='Add Game',
            handle='api_games.add',
            method='POST',
            template='api_games_add.html'
        ),
        ApiEndpoint(
            model='game',
            title='Get Game by id',
            handle='api_games.get_by_id',
            method='GET',
            template='api_games_get_by_id.html',
            default_params={'game_id': '.GAME_ID.'}
        ),
        ApiEndpoint(
            model='game move',
            title='Add Game Move',
            handle='api_games.moves_add',
            method='PUT',
            template='api_games_moves_add.html',
            default_params={'game_id': '.GAME_ID.', 'move_sequence': '.MOVE_SEQUENCE.'}
        ),
    ]
    
    return render_template("api_index.html", api_endpoint_list=api_endpoint_list)