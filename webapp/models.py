import csv
from dataclasses import dataclass, field
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

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


@dataclass
class Player:
    name: str
    type: str
    id: int = None

    # Class variable:
    __players = []

    def __post_init__(self):
        if not self.id:
            self.id = self.next_available_id()
        else:
            self.id = int(self.id)

        # Ensure player is appended to list of players:
        self.__players.append(self)

    @classmethod
    def next_available_id(cls):
        largest_id_review = max(cls.__players, default=None, key=lambda r: int(r.id))
        if largest_id_review:
            next_id = int(largest_id_review.id) + 1
        else:
            next_id = 1
        return next_id

    @classmethod
    def get_players(cls):
        return cls.__players

    @classmethod
    def get_player_by_id(cls, player_id:int):
        this_player = None
        for player in cls.__players:
            if player.id == int(player_id):
                this_player = player
                break
        return this_player

    @classmethod
    def update_player_by_id(cls, player_id:int, params):
        updated_player = None
        for key, this_player in enumerate(cls.__players):
            if this_player.id == int(player_id):
                # Player we are updating:
                updated_player = this_player
                # Properties to update:
                if 'name' in params:
                    updated_player.name = params['name']
                if 'type' in params:
                    updated_player.type = params['type']
                cls.__players[key] = updated_player
                break
        return updated_player


class PlayerCsv:
    csv_filename : str

    def __init__(self, csv_filename):
        self.csv_filename = csv_filename

    def synchronize_players(self, direction, whole_file=False, player_list=None):

        if type(player_list) != list:
            player_list = [player_list]

        if direction not in ('to_file', 'from_file'):
            return False

        if direction == 'to_file':
            if whole_file:

                # Write all our data to the CSV file, and overwrite
                with open(self.csv_filename, 'w', newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['id', 'name', 'type'])

                    player: Player
                    for player in player_list:
                        if player:
                            writer.writerow([player.id, player.name, player.type])

                return True
            else:
                # Write only updated or missing data to the file:
                return False # Operation is not supported.

        elif direction == 'from_file':
            player_list = []
            with open(self.csv_filename, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for idx, playerData in enumerate(reader):
                    player_list.append(Player(**playerData))
