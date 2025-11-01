from webapp.models.base import db
from webapp.event import Event
from webapp.helpers import GameStatus, WinningPlayerNum, GamePosition
from webapp.models.game_move import GameMove
from webapp.models.player import Player

class Game(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    player_one_id = db.Column(db.Integer(), db.ForeignKey('player.id'), nullable=False)
    player_two_id = db.Column(db.Integer(), db.ForeignKey('player.id'), nullable=False)
    status = db.Column(db.Enum(GameStatus), nullable=False)
    next_move_sequence = db.Column(db.Integer())
    next_move_player_number = db.Column(db.Integer())
    next_move_player_id = db.Column(db.Integer(), db.ForeignKey('player.id'), nullable=True)
    board_state = db.Column(db.String(9))
    winning_player_id = db.Column(db.Integer(), db.ForeignKey('player.id'), nullable=True)
    winning_player_number = db.Column(db.Enum(WinningPlayerNum), nullable=True)
    moves = db.relationship(
        'GameMove',
        backref='game',
        lazy='dynamic',  # Load if required
        foreign_keys='GameMove.game_id'
    )

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

    @classmethod
    def get_games(cls):
        return cls.query.order_by(Game.id.desc()).all()

    @classmethod
    def get_game_by_id(cls, game_id: int):
        return cls.query.get(int(game_id))

    @classmethod
    def check_for_winner(cls, board_state_str) -> WinningPlayerNum | None:
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

    @property
    def winning_pieces(self) -> set[int]:
        b = list(self.board_state)
        winning_pieces = set()
        for cond in Game.winning_combinations:
            # noinspection PyTypeChecker
            line = "".join([b[gp.value - 1] for gp in cond])
            if line == "111" or line == "222":
                winning_pieces.update({gp.value for gp in cond})
        return winning_pieces
    
    @classmethod
    def valid_next_positions(cls, board_state_str) -> list[GamePosition]:
        return [GamePosition(idx + 1) for idx, value in enumerate(board_state_str) if value == "0"]

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

    def get_valid_next_positions(self) -> list:
        return Game.valid_next_positions(self.board_state)

    def get_next_move_player_type(self) -> str:
        player_type = None
        next_move_player = None
        if self.status == GameStatus.IN_PROGRESS:
            if self.next_move_player_number == 1:
                next_move_player = Player.get_player_by_id(self.player_one_id)
            elif self.next_move_player_number == 2:
                next_move_player = Player.get_player_by_id(self.player_two_id)

        if type(next_move_player) == Player:
            player_type = next_move_player.player_type

        return player_type

    def to_dict(self, full_detail=True) -> dict:
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
            self.next_move_player_number = None
            self.next_move_player_id = None
        else:
            # If this move was player 1, next move is now player 2
            # If this move was player 2, next move is now player 1
            self.next_move_player_number = 3 - player_number
            self.next_move_player_id = self.player_one_id if self.next_move_player_number == 1 else self.player_two_id

        db.session.add(self)
        self.e_added.post_event(self)
        return self