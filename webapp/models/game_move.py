from webapp.models.base import db
from webapp.event import Event
from webapp.helpers import GamePosition

class GameMove(db.Model):
    game: "Game"
    id = db.Column(db.Integer(), primary_key=True)
    game_id = db.Column(db.Integer(), db.ForeignKey('game.id'), nullable=False)
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

        db.session.add(self)

        # Inform any event listeners:
        self.e_added.post_event(self)