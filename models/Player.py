from dataclasses import dataclass


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