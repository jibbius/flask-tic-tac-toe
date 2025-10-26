from webapp.models.base import db
from webapp.event import Event
from webapp.helpers import GameStatus, WinningPlayerNum, GamePosition

class Player(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    player_type = db.Column(db.String(255))
    bot_difficulty = db.Column(db.String(255))
    games_as_player_one = db.relationship(
        'Game',
        backref='player_one',
        lazy='subquery',  # Always load
        foreign_keys='Game.player_one_id'
    )
    games_as_player_two = db.relationship(
        'Game',
        backref='player_two',
        lazy='subquery',  # Always load
        foreign_keys='Game.player_two_id'
    )
    games_as_winner = db.relationship(
        'Game',
        backref='winning_player',
        lazy='dynamic',  # Load if required
        foreign_keys='Game.winning_player_id'
    )
    games_as_next_move = db.relationship(
        'Game',
        backref='next_move_player',
        lazy='dynamic',  # Load if required
        foreign_keys='Game.next_move_player_id'
    )

    e_added = Event()
    e_updated = Event()

    def __init__(self, name, player_type, bot_difficulty):
        self.name = name
        self.player_type = player_type
        self.bot_difficulty = bot_difficulty

        # Commit to database:
        db.session.add(self)
        db.session.commit()

        # Inform any event listeners:
        self.e_added.post_event(self)

    def __repr__(self):
        return "<Player '{}' ({})>".format(self.name, self.player_type)

    def to_dict(self) -> dict:
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