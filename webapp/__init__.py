from flask import Flask, render_template, request
from flask_migrate import Migrate

from webapp.csv_sync import PlayerCsv
from webapp.helpers import ApiEndpoint
from webapp.models import Player, Game, GameMove
from webapp.models import db


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    Migrate(app, db)

    player_csv = PlayerCsv('seed_data_players.csv')

    existing_data = Player.get_players()
    if not existing_data:
        player_csv.synchronize_players_from_file()

        # If the Data has any further updates, write these to the file:
        # Player.e_added.add_listener(player_csv.synchronize_players_to_file)
        # Player.e_updated.add_listener(player_csv.synchronize_players_to_file)

    app.jinja_env.globals.update(navigation_items=[
        {"label": "Home", "function": "root"},
        # {"label": "Start a new game", "function": "ui_start_game"},
        # {"label": "Resume/join a game", "function": "ui_join_game"},
        # {"label": "Statistics", "function": "ui_stats"},
        {"label": "API Index", "function": "api_index"}
    ])

    @app.route('/')  # define the first route, the home route
    def root():  # define the function that responds to the above route
        return render_template("index.html")

    @app.route('/game/new')
    def ui_start_game():  # put application's code here
        return '<a href="/">Return to menu</a>'

    @app.route('/game/join')
    def ui_join_game():  # put application's code here
        return '<a href="/">Return to menu</a>'

    @app.route('/stats')
    def ui_stats():  # put application's code here
        return '<a href="/">Return to menu</a>'

    @app.route('/api_index')
    def api_index():
        api_endpoint_list = [
            ApiEndpoint(model='player',
                        title='Get all Players',
                        handle='api_players_get_all',
                        method='GET',
                        template='api_players_get_all.html'
                        ),
            ApiEndpoint(model='player',
                        title='Get Player by id',
                        handle='api_players_get_by_id',
                        method='GET',
                        template='api_players_get_by_id.html',
                        default_params={'player_id': '.PLAYER_ID.'}
                        ),
            ApiEndpoint(model='player',
                        title='Add Player',
                        handle='api_players_add',
                        method='POST',
                        template='api_players_add.html'
                        ),
            ApiEndpoint(model='player',
                        title='Update Player',
                        handle='api_players_update_by_id',
                        method='PUT',
                        template='api_players_update_by_id.html',
                        default_params={'player_id': '.PLAYER_ID.'}
                        ),
            ApiEndpoint(model='game',
                        title='Get all Games',
                        handle='api_games_get_all',
                        method='GET',
                        template='api_games_get_all.html'
                        ),
            ApiEndpoint(model='game',
                        title='Add Game',
                        handle='api_games_add',
                        method='POST',
                        template='api_games_add.html'
                        ),
            ApiEndpoint(model='game',
                        title='Get Game by id',
                        handle='api_games_get_by_id',
                        method='GET',
                        template='api_games_get_by_id.html',
                        default_params={'game_id':'.GAME_ID.'}
                        ),
            ApiEndpoint(model='game move',
                        title='Add Game Move',
                        handle='api_games_moves_add',
                        method='PUT',
                        template='api_games_moves_add.html',
                        default_params={'game_id':'.GAME_ID.', 'move_sequence': '.MOVE_SEQUENCE.'}
                        ),
        ]
        return render_template("api_index.html", api_endpoint_list=api_endpoint_list)

    @app.route("/api/players/new", methods=["POST"])
    def api_players_add():
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

    @app.route("/api/players/", methods=["GET"])
    def api_players_get_all():
        response_data = []
        players = Player.get_players()
        if players:
            response_data = [player.to_dict() for player in players]
        return {"status": 200, "data": response_data}

    @app.route("/api/players/<player_id>/", methods=["GET"])
    def api_players_get_by_id(player_id):
        response = {'status': None, 'data': []}
        player = Player.get_player_by_id(player_id)
        if player:
            response['status'] = 200
            response['data'] = player.to_dict()
        else:
            response['status'] = 400  # Bad request
        return response

    @app.route("/api/players/<player_id>/", methods=["PUT"])
    def api_players_update_by_id(player_id):
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

    @app.route("/api/games/", methods=["GET"])
    def api_games_get_all():
        response = {'status': None, 'data': []}
        games = Game.get_games()
        if games:
            game: Game
            response['data'] = [game.to_dict(fullDetail=False) for game in games]
        response['status'] = 200  # OK
        return response

    @app.route("/api/games/new", methods=["POST"])
    def api_games_add():
        response = {'status': None, 'data': []}
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            request_params = request.json
            required_params = ['player_one_id', 'player_two_id']
            if all(param in required_params for param in request_params):
                try:
                    game = Game(
                        player_one_id=int(request_params['player_one_id']),
                        player_two_id=int(request_params['player_two_id'])
                    )
                    response['data'] = game.to_dict()
                except ValueError as err:
                    response['message'] = err.args[0]

        if response['data']:
            response['status'] = 201  # Created
        else:
            response['status'] = 400  # Bad request
        return response

    @app.route("/api/games/<game_id>/", methods=["GET"])
    def api_games_get_by_id(game_id):
        response = {'status': None, 'data': []}
        game = Game.get_game_by_id(game_id)
        if game:
            response['status'] = 200
            response['data'] = game.to_dict()
        else:
            response['status'] = 400  # Bad request
        return response

    @app.route("/api/games/<game_id>/<move_sequence>", methods=["PUT"])
    def api_games_moves_add(game_id:int, move_sequence:int):
        response = {'status': None, 'data': []}
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            request_params = request.json
            player_id = request_params.get('player_id')
            position = request_params.get('position')
            if all([game_id, move_sequence, player_id, position]):
                try:
                    game_id = int(game_id)
                    move_sequence = int(move_sequence)
                    player_id = int(player_id)
                    position = int(position)
                    game_move = GameMove(
                        game_id=game_id,
                        move_sequence=move_sequence,
                        player_id=player_id,
                        position=position
                    )
                    response['data'] = game_move.game.to_dict()
                except (ValueError, TypeError) as err:
                    response['message'] = err.args[0]
        if response['data']:
            response['status'] = 200  # OK
        else:
            response['status'] = 400  # Bad request
        return response
    return app
