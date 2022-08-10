import csv
from dataclasses import dataclass, field
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from webapp.event import Event

db = SQLAlchemy()

@dataclass
class ApiEndpoint:
    """
    This class helps us to generate our API page.
    """
    model: str
    title: str
    handle: str
    method: str
    template: str
    default_params: dict = field(default_factory=dict)

    def url(self):
        if self.default_params:
            return url_for(self.handle, **self.default_params)
        else:
            return url_for(self.handle)


class Player(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))

    e_added = Event()
    e_updated = Event()

    def __init__(self, name, type):
        self.name = name
        self.type = type

        # Commit to database:
        db.session.add(self)
        db.session.commit()

        # Inform any event listeners:
        self.e_added.post_event(self)

    def __repr__(self):
        return "<Player '{}'>".format(self.name)

    def to_dict(self):
        player_as_dict = {
            "id" : self.id,
            "name" : self.name,
            "type" : self.type,
        }
        return player_as_dict

    @classmethod
    def get_players(cls):
        return cls.query.all()

    @classmethod
    def get_player_by_id(cls, player_id:int):
        this_player = cls.query.get(int(player_id))
        return this_player

    @classmethod
    def update_player_by_id(cls, player_id:int, params):
        updated_player = None
        allowable_params = ('name', 'type')
        if len(allowable_params) <= len(allowable_params | params.keys()):
            did_update = cls.query.filter_by(id=int(player_id)).update(params)

            if did_update:
                db.session.commit()
                updated_player = cls.get_player_by_id(player_id)
                cls.e_added.post_event(updated_player)

        return updated_player

class PlayerCsv:
    csv_filename : str

    def __init__(self, csv_filename):
        self.csv_filename = csv_filename

    def synchronize_players_from_file(self):
        player_list = []
        with open(self.csv_filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, playerData in enumerate(reader):
                allowablePlayerData = {
                    "name":playerData["name"],
                    "type":playerData["type"],
                }
                player_list.append(Player(**allowablePlayerData))
        return player_list

    def synchronize_players_to_file(self, updated_data):
        # To keep things simple, we are just going to get all players from DB
        # (and forgo any attempt at delta processing)
        player_list = Player.get_players()
        with open(self.csv_filename, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'name', 'type'])

            player: Player
            for player in player_list:
                if player:
                    writer.writerow([player.id, player.name, player.type])

        return True
