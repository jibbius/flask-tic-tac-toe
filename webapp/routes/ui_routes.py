"""UI routes for web interface"""

from flask import Blueprint, render_template, request, url_for, flash, Markup

from webapp.services import GameService
from webapp.helpers import GameStatus
from webapp.models.player import Player
from webapp.models.game import Game

ui_bp = Blueprint('ui', __name__)


@ui_bp.route('/')
def root():
    """Home page"""
    return render_template("index.html")

@ui_bp.route("/about/", methods=["GET"])
def about():
    """About page"""
    return render_template("ui_about.html")

@ui_bp.route('/game/new')
def games_new():
    """New game page"""
    return render_template("ui_games_new.html", player_list=Player.get_players())


@ui_bp.route("/games/", methods=["POST"])
def games_add():
    """Create a new game"""
    error_message = None
    game = None
    player_one_id = request.values.get('player_one_id')
    player_two_id = request.values.get('player_two_id')
    
    if all([player_one_id, player_two_id]):
        try:
            game_service = GameService(
                player_one_id=int(player_one_id),
                player_two_id=int(player_two_id)
            )
            game = game_service.create_game()
            game_url = url_for('ui.games_get_by_id', game_id=game.id)
            flash(Markup(f"Game created successfully: <a href='{game_url}'>Join game</a>"), 'success')
        except ValueError as err:
            error_message = err.args[0]
    
    if not game:
        if not error_message:
            error_message = "Unexpected Error"
        flash(f"{error_message}", 'error')
    
    return render_template("ui_games_get_all.html", all_games=Game.get_games())


@ui_bp.route("/games/", methods=["GET"])
def games_get_all():
    """List all games"""
    return render_template("ui_games_get_all.html", all_games=Game.get_games())


@ui_bp.route("/games/<int:game_id>/", methods=["GET"])
def games_get_by_id(game_id: int):
    """View a specific game"""
    response = {'status': None, 'data': []}
    game_service = GameService(game_id=game_id)
    
    if game_service.game:
        response['status'] = 200
        response['data'] = game_service.game.to_dict()
        all_moves = []
        for move in game_service.game.moves:
            all_moves.append(move.position.value)

        return render_template(
            "ui_games_get_by_id.html",
            game=game_service.game,
            player_one=game_service.player_one,
            player_two=game_service.player_two,
            board=list(game_service.game.board_state),
            enumGameStatus=GameStatus,
            last_move_position=game_service.get_last_move_position(),
            all_moves=list(all_moves)
        )
    else:
        response['status'] = 400  # Bad request
        return response


@ui_bp.route("/games/<int:game_id>/", methods=["POST"])
def games_moves_add(game_id: int):
    """Add a move to a game"""
    player_id = request.values.get('player_id')
    position = request.values.get('position')
    move_sequence = request.values.get('move_sequence')
    
    if all([game_id, move_sequence, player_id, position]):
        try:
            game_service = GameService(game_id=game_id)
            game_service.append_game_move(
                move_sequence=move_sequence,
                player_id=player_id,
                position=position
            )
            return render_template(
                "ui_games_get_by_id.html",
                game=game_service.game,
                player_one=game_service.player_one,
                player_two=game_service.player_two,
                board=list(game_service.game.board_state),
                enumGameStatus=GameStatus,
                last_move_position=game_service.get_last_move_position()
            )
        except (ValueError, TypeError) as err:
            return err.args[0]
    
    return "Unexpected error"


# @ui_bp.route('/game/join')
# def join_game():
#     """Join game page (placeholder)"""
#     return '<a href="/">Return to menu</a>'
#
#
# @ui_bp.route('/stats')
# def stats():
#     """Statistics page (placeholder)"""
#     return '<a href="/">Return to menu</a>'
