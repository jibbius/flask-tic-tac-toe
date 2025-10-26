import csv
import os
from webapp.models.player import Player

class PlayerCsv:
    csv_filename : str

    def __init__(self, csv_filename):

        check_filenames = [
            csv_filename,
            '..\\' + csv_filename
        ]

        for filename in check_filenames:
            if os.path.exists(filename):
                self.csv_filename = filename
                return


    def synchronize_players_from_file(self):
        player_list = []
        with open(self.csv_filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, playerData in enumerate(reader):
                allowablePlayerData = {
                    "name":playerData["name"],
                    "player_type":playerData["player_type"],
                    "bot_difficulty":playerData["bot_difficulty"]
                }
                player_list.append(Player(**allowablePlayerData))
        return player_list

    def synchronize_players_to_file(self, updated_data):
        # To keep things simple, we are just going to get all players from DB
        # (and forgo any attempt at delta processing)
        player_list = Player.get_players()
        with open(self.csv_filename, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'name', 'player_type', 'bot_difficulty'])

            player: Player
            for player in player_list:
                if player:
                    writer.writerow([player.id, player.name, player.player_type, player.bot_difficulty])

        return True