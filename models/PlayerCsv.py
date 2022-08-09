import csv
from models.Player import Player


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
