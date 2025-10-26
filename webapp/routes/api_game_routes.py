"""API routes for game management"""

from flask import Blueprint, request

from webapp.services import GameService
from webapp.models.game import Game

api_games_bp = Blueprint('api_games', __name__)


@api_games_bp.route("/games/", methods=["GET"])
def get_all():
    """Get all games"""
    response = {'status': None, 'data': []}
    games = Game.get_games()
    
    if games:
        response['data'] = [game.to_dict(full_detail=False) for game in games]
    
    response['status'] = 200  # OK
    return response


@api_games_bp.route("/games/new", methods=["POST"])
def add():
    """
    Create a new game.
    
    Expected JSON payload:
    {
        "player_one_id": 1,
        "player_two_id": 2
    }
    """
    response = {'status': None, 'data': []}
    content_type = request.headers.get('Content-Type')
    
    if content_type == 'application/json':
        player_one_id = request.json.get('player_one_id')
        player_two_id = request.json.get('player_two_id')
        
        if all([player_one_id, player_two_id]):
            try:
                game_service = GameService(
                    player_one_id=int(player_one_id),
                    player_two_id=int(player_two_id)
                )
                game = game_service.create_game()
                response['data'] = game.to_dict()
            except ValueError as err:
                response['message'] = err.args[0]
    
    if response['data']:
        response['status'] = 201  # Created
    else:
        response['status'] = 400  # Bad request
    
    return response


@api_games_bp.route("/games/<game_id>/", methods=["GET"])
def get_by_id(game_id: int):
    """Get a specific game by ID"""
    response = {'status': None, 'data': []}
    game = Game.get_game_by_id(game_id)
    
    if game:
        response['status'] = 200
        response['data'] = game.to_dict()
    else:
        response['status'] = 400  # Bad request
    
    return response


@api_games_bp.route("/games/<game_id>/<move_sequence>", methods=["PUT"])
def moves_add(game_id: int, move_sequence: int):
    """
    Add a move to a game.
    
    Expected JSON payload:
    {
        "player_id": 1,
        "position": 5
    }
    """
    response = {'status': None, 'data': []}
    content_type = request.headers.get('Content-Type')
    
    if content_type == 'application/json':
        request_params = request.json
        player_id = request_params.get('player_id')
        position = request_params.get('position')
        
        if all([game_id, move_sequence, player_id, position]):
            try:
                game_service = GameService(game_id=game_id)
                game_service.append_game_move(
                    move_sequence=move_sequence,
                    player_id=player_id,
                    position=position
                )
                response['data'] = game_service.game.to_dict()
            except (ValueError, TypeError) as err:
                response['message'] = err.args[0]
    
    if response['data']:
        response['status'] = 200  # OK
    else:
        response['status'] = 400  # Bad request
    
    return response