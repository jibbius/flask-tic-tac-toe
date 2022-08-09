import models.Player

from flask import Flask, render_template, request
from models.ApiEndpoint import ApiEndpoint
from Config import Config
# from models.Player import Player
from models.PlayerCsv import PlayerCsv

if __name__ in ['__main__', 'app']:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.jinja_env.globals.update(navigation_items=[
        {"label": "Home", "function": "root"},
        # {"label": "Start a new game", "function": "ui_start_game"},
        # {"label": "Resume/join a game", "function": "ui_join_game"},
        # {"label": "Statistics", "function": "ui_stats"},
        {"label": "API Index", "function": "api_index"}
    ])
    player_csv = PlayerCsv('seed_data_players.csv')
    player_csv.synchronize_players('from_file')


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
            ApiEndpoint(model='player', title='Get all Players', handle='api_players_get_all', method='GET',
                        template='api_players_get_all.html'),
            ApiEndpoint(model='player', title='Get Player by id', handle='api_players_get_by_id', method='GET',
                        template='api_players_get_by_id.html', default_params={'player_id': '.PLAYER_ID.'}),
            ApiEndpoint(model='player', title='Add Player', handle='api_players_add', method='POST',
                        template='api_players_add.html'),
            ApiEndpoint(model='player', title='Update Player', handle='api_players_update_by_id', method='PUT',
                        template='api_players_update_by_id.html', default_params={'player_id': '.PLAYER_ID.'}),
        ]
        return render_template("api_index.html", api_endpoint_list=api_endpoint_list)


    @app.route("/api/players/new", methods=["POST"])
    def api_players_add():
        player = None
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            request_params = request.json
            required_params = ['name', 'type']
            if all(param in required_params for param in request_params):
                player = models.Player.Player(name=request_params['name'], type=request_params['type'])
        if player:
            player_csv.synchronize_players('to_file', True, models.Player.Player.get_players())
            status_code = 201  # Created
        else:
            status_code = 400  # Bad request
        return {"status": status_code, "data": player}


    @app.route("/api/players/", methods=["GET"])
    def api_players_get_all():
        players = models.Player.Player.get_players()
        return {"status": 200, "data": players}


    @app.route("/api/players/<player_id>/", methods=["GET"])
    def api_players_get_by_id(player_id):
        player = models.Player.Player.get_player_by_id(player_id)
        if player:
            status_code = 200
        else:
            status_code = 400  # Bad request
        return {"status": status_code, "data": player}


    @app.route("/api/players/<player_id>/", methods=["PUT"])
    def api_players_update_by_id(player_id):
        updated_player = None
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            params = request.json
            updated_player = models.Player.Player.update_player_by_id(player_id, params)
            if updated_player:
                player_csv.synchronize_players('to_file', True, models.Player.Player.get_players())
                status_code = 200  # OK
            else:
                status_code = 400  # Bad request
        else:
            status_code = 400  # Bad request
        return {"status": status_code, "data": updated_player}


    app.run(DEBUG=True)
