from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event as sql_event
from sqlalchemy.engine import Engine

from webapp.event import Event as Event
from webapp.helpers import GameStatus, WinningPlayerNum, GamePosition

db = SQLAlchemy()


# Instruct SQLAlchemy to enforce FK constraints:
@sql_event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Player(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    player_type = db.Column(db.String(255))
    games_as_player_one = db.relationship(
        'Game',
        backref='player_one',
        lazy='subquery', # 'dynamic'
        foreign_keys='Game.player_one_id'
    )
    games_as_player_two = db.relationship(
        'Game',
        backref='player_two',
        lazy='subquery', # 'dynamic'
        foreign_keys='Game.player_two_id'
    )

    e_added = Event()
    e_updated = Event()

    def __init__(self, name, player_type):
        self.name = name
        self.player_type = player_type

        # Commit to database:
        db.session.add(self)
        db.session.commit()

        # Inform any event listeners:
        self.e_added.post_event(self)

    def __repr__(self):
        return "<Player '{}'>".format(self.name)

    def to_dict(self):
        player_as_dict = {
            "id": self.id,
            "name": self.name,
            "player_type": self.player_type,
        }
        return player_as_dict

    @classmethod
    def get_players(cls):
        return cls.query.all()

    @classmethod
    def get_player_by_id(cls, player_id: int):
        this_player = cls.query.get(int(player_id))
        return this_player

    @classmethod
    def update_player_by_id(cls, player_id: int, params):
        updated_player = None
        allowable_params = ('name', 'player_type')
        all_params = set(params.keys()).union(allowable_params)

        if len(all_params) > len(allowable_params):
            raise ValueError("Parameters specified are not allowed")
        else:
            did_update = cls.query.filter_by(id=int(player_id)).update(params)

            if did_update:
                db.session.commit()
                updated_player = cls.get_player_by_id(player_id)
                cls.e_added.post_event(updated_player)

        return updated_player


class Game(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    player_one_id = db.Column(db.Integer(), db.ForeignKey('player.id'))
    player_two_id = db.Column(db.Integer(), db.ForeignKey('player.id'))
    status = db.Column(db.Enum(GameStatus))
    next_move_sequence = db.Column(db.Integer())
    next_move_player_number = db.Column(db.Integer())
    board_state = db.Column(db.String(9))
    winning_player_id = db.Column(db.Integer())
    winning_player_number = db.Column(db.Enum(WinningPlayerNum))


    e_added = Event()
    e_updated = Event()

    winning_combinations = [
        # Horizontal
        [GamePosition.TOP_ROW_LEFT_COL, GamePosition.TOP_ROW_CENTER_COL, GamePosition.TOP_ROW_RIGHT_COL],
        [GamePosition.MIDDLE_ROW_LEFT_COL, GamePosition.MIDDLE_ROW_CENTER_COL, GamePosition.MIDDLE_ROW_RIGHT_COL],
        [GamePosition.BOTTOM_ROW_LEFT_COL, GamePosition.BOTTOM_ROW_CENTER_COL, GamePosition.BOTTOM_ROW_RIGHT_COL],
        # Vertical
        [GamePosition.TOP_ROW_LEFT_COL, GamePosition.MIDDLE_ROW_LEFT_COL, GamePosition.BOTTOM_ROW_LEFT_COL],
        [GamePosition.TOP_ROW_CENTER_COL, GamePosition.MIDDLE_ROW_CENTER_COL, GamePosition.BOTTOM_ROW_CENTER_COL],
        [GamePosition.TOP_ROW_RIGHT_COL, GamePosition.MIDDLE_ROW_RIGHT_COL, GamePosition.BOTTOM_ROW_RIGHT_COL],
        # Diagonal
        [GamePosition.TOP_ROW_LEFT_COL, GamePosition.MIDDLE_ROW_CENTER_COL, GamePosition.BOTTOM_ROW_RIGHT_COL],
        [GamePosition.TOP_ROW_RIGHT_COL, GamePosition.MIDDLE_ROW_CENTER_COL, GamePosition.BOTTOM_ROW_LEFT_COL],
    ]

    def __init__(self, player_one_id: int, player_two_id: int):

        self.player_one_id = player_one_id
        self.player_two_id = player_two_id
        self.status = GameStatus.IN_PROGRESS
        self.board_state = "0" * 9
        self.winning_player_id = None
        self.winning_player_number = None
        self.next_move_sequence = 1

        # This tells us which player number (1 or 2), will take the next move.
        # Later, we might change this logic to randomise or alternate who the first player is?
        self.next_move_player_number = 1

        # Inform any event listeners:
        self.e_added.post_event(self)

    def board_state_as_matrix(self):
        b = self.board_state
        z = [b[0] + b[1] + b[2], b[3] + b[4] + b[5], b[6] + b[7] + b[8]]
        return z

    def get_valid_next_positions(self):
        return [GamePosition(idx + 1) for idx, value in enumerate(self.board_state) if value == "0"]

    def get_next_move_player_type(self):
        player_type = None
        if self.status == GameStatus.IN_PROGRESS:
            if self.next_move_player_number == 1:
                next_move_player = Player.get_player_by_id(self.player_one_id)
            elif self.next_move_player_number == 2:
                next_move_player = Player.get_player_by_id(self.player_two_id)

        if type(next_move_player) == Player:
            player_type = next_move_player.player_type

        return player_type

    def to_dict(self, full_detail=True):
        game_as_dict = {
            "id": self.id,
            "player_one_id": self.player_one_id,
            "player_two_id": self.player_two_id,
            "status": self.status.name,
        }
        if full_detail:
            game_as_dict.update({
                "next_move_sequence": self.next_move_sequence,
                "board_state": self.board_state,
                "board_state_as_matrix": self.board_state_as_matrix(),
                "winning_player_id": self.winning_player_id,
                "winning_player_number": self.winning_player_number.name if self.winning_player_number else None,
                "next_move_player_number": self.next_move_player_number
            })
        return game_as_dict

    @classmethod
    def get_games(cls):
        return cls.query.all()

    @classmethod
    def get_game_by_id(cls, game_id: int):
        this_game = cls.query.get(int(game_id))
        return this_game

    @classmethod
    def update_game_by_id(cls, game_id: int, params):
        updated_game = None
        allowable_params = []
        all_params = set(params.keys()).union(allowable_params)

        if len(all_params) > len(allowable_params):
            raise ValueError("Parameters specified are not allowed")
        else:
            did_update = cls.query.filter_by(id=int(game_id)).update(params)
            if did_update:
                db.session.commit()
                updated_game = cls.get_game_by_id(game_id)
                cls.e_added.post_event(updated_game)

        return updated_game

    def append_move(self, player_number: int, position: GamePosition):
        updated_board_state = list(self.board_state)

        # noinspection PyTypeChecker
        updated_board_state[position.value - 1] = str(player_number)

        updated_board_state = "".join(updated_board_state)
        self.board_state = updated_board_state
        self.next_move_sequence += 1

        # If this move was player 1, next move is player 2
        # If this move was player 2, next move is player 1
        self.next_move_player_number = 3 - player_number

        winner_or_tie = Game.check_for_winner(self.board_state)
        if winner_or_tie:
            self.status = GameStatus.FINISHED
            self.winning_player_number = winner_or_tie
            if winner_or_tie == WinningPlayerNum.PLAYER_ONE:
                self.winning_player_id = self.player_one_id
            if winner_or_tie == WinningPlayerNum.PLAYER_TWO:
                self.winning_player_id = self.player_two_id
        return self

    @classmethod
    def check_for_winner(cls, board_state_str):
        b = list(board_state_str)
        for cond in cls.winning_combinations:
            # noinspection PyTypeChecker
            line = "".join([b[gp.value - 1] for gp in cond])
            if line == "111":
                return WinningPlayerNum.PLAYER_ONE
            if line == "222":
                return WinningPlayerNum.PLAYER_TWO
        if "0" not in b:
            return WinningPlayerNum.TIE
        return None  # No winner


class GameMove(db.Model):
    game: Game
    id = db.Column(db.Integer(), primary_key=True)
    game_id = db.Column(db.Integer())
    move_sequence = db.Column(db.Integer())
    player_number = db.Column(db.Integer())
    player_id = db.Column(db.Integer())
    position = db.Column(db.Enum(GamePosition))
    e_added = Event()

    def __init__(
            self,
            game_id: int,
            move_sequence: int,
            player_number: int,
            player_id: int,
            position: GamePosition
    ):
        self.game_id = game_id
        self.move_sequence = move_sequence
        self.player_number = player_number
        self.player_id = player_id
        self.position = position

        # Inform any event listeners:
        self.e_added.post_event(self)

