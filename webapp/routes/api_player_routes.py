"""API routes for player management"""

from flask import Blueprint, request

from webapp.models.player import Player

api_players_bp = Blueprint('api_players', __name__)


@api_players_bp.route("/players/new", methods=["POST"])
def add():
    """
    Create a new player.
    
    Expected JSON payload:
    {
        "name": "Player Name",
        "player_type": "human" or "computer"
    }
    """
    response = {'status': None, 'data': []}
    player = None
    content_type = request.headers.get('Content-Type')
    
    if content_type == 'application/json':
        request_params = request.json
        name = request_params.get('name')
        player_type = request_params.get('player_type')
        
        if all([name, player_type]):
            player = Player(name=name, player_type=player_type)
    
    if player:
        response['status'] = 201  # Created
        response['data'] = player.to_dict()
    else:
        response['status'] = 400  # Bad request
    
    return response


@api_players_bp.route("/players/", methods=["GET"])
def get_all():
    """Get all players"""
    response_data = []
    players = Player.get_players()
    
    if players:
        response_data = [player.to_dict() for player in players]
    
    return {"status": 200, "data": response_data}


@api_players_bp.route("/players/<player_id>/", methods=["GET"])
def get_by_id(player_id: int):
    """Get a specific player by ID"""
    response = {'status': None, 'data': []}
    player = Player.get_player_by_id(player_id)
    
    if player:
        response['status'] = 200
        response['data'] = player.to_dict()
    else:
        response['status'] = 400  # Bad request
    
    return response



@api_players_bp.route("/players/<player_id>/", methods=["PUT"])
def update_by_id(player_id: int):
    """
    Update a player by ID.
    
    Expected JSON payload:
    {
        "name": "Updated Name",
        "player_type": "human" or "computer"
    }
    """
    response = {'status': None, 'data': []}
    content_type = request.headers.get('Content-Type')
    
    if content_type == 'application/json':
        params = request.json
        updated_player = Player.update_player_by_id(player_id, params)
        
        if updated_player:
            response['data'] = updated_player.to_dict()
    
    if response['data']:
        response['status'] = 200  # OK
    else:
        response['status'] = 400  # Bad request
    
    return response