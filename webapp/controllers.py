import random

from webapp.helpers import GamePosition, GameStatus
from webapp.models import Player, Game, GameMove, db


class GameController:
    player_one: Player
    player_two: Player
    game: Game

    def __init__(self, player_one_id: int = None, player_two_id: int = None, game_id: int = None):
        self.player_one = None
        self.player_two = None
        self.game = None

        if game_id:
            self.game = Game.get_game_by_id(int(game_id))
            if not self.game:
                raise ValueError("Invalid Game ID")

        if player_one_id:
            self.player_one = Player.get_player_by_id(int(player_one_id))
            if not self.player_one:
                raise ValueError("Invalid ID for Player 1")
            if self.game:
                if self.game.player_one_id != self.player_one.id:
                    raise ValueError(
                        f"Unexpected ID for Player 1. Expected {self.game.player_one_id}, got {self.player_one.id}")
        elif self.game:
            self.player_one = Player.get_player_by_id(int(self.game.player_one_id))

        if player_two_id:
            self.player_two = Player.get_player_by_id(int(player_two_id))
            if not self.player_two:
                raise ValueError("Invalid ID for Player 2")
            if self.game:
                if self.game.player_one_id != self.player_one.id:
                    raise ValueError(
                        f"Unexpected ID for Player 2. Expected {self.game.player_two_id}, got {self.player_two.id}")
        elif self.game:
            self.player_two = Player.get_player_by_id(int(self.game.player_two_id))

    def create_game(self) -> Game:
        if not all([self.player_one, self.player_two]):
            raise ValueError(f"Cannot create game without first specifying player IDs.")

        self.game = Game(self.player_one.id, self.player_two.id)

        # Append to database:
        db.session.add(self.game)

        # Determine if any automated moves to be executed
        self.perform_automated_moves()

        # Commit transaction to database
        db.session.commit()

        return self.game

    def append_game_move(self, move_sequence: int, player_id: int, position: GamePosition):

        # Sanitise inputs:
        sanitised_move_sequence = int(move_sequence)
        sanitised_player_id = int(player_id)
        sanitised_position = None
        if type(position) == str:
            sanitised_position = GamePosition(int(position))
        elif type(position) == int:
            sanitised_position = GamePosition(position)
        elif type(position) == GamePosition:
            sanitised_position = position

        # Validate inputs
        if type(sanitised_position) != GamePosition:
            raise ValueError("Unexpected GamePosition type")

        if not self.game:
            raise ValueError("Invalid Game ID")

        if self.game.status != GameStatus.IN_PROGRESS:
            raise ValueError(f"No further moves allowed; Game status = {self.game.status.name}")

        if sanitised_move_sequence != self.game.next_move_sequence:
            raise ValueError(
                f"Unexpected move sequence (expected {self.game.next_move_sequence}, got {move_sequence})")

        if self.game.next_move_player_number == 1:
            if not self.player_one:
                raise ValueError(f"It is Player 1's turn. Cannot execute move without first setting Player 1's ID.")
            else:
                if self.player_one.id != sanitised_player_id:
                    raise ValueError(
                        "It is Player 1's turn; (expected PlayerID {}), got PlayerID {})".format(
                            self.game.player_one_id,
                            sanitised_player_id
                        ))
        elif self.game.next_move_player_number == 2:
            if not self.player_two:
                raise ValueError(f"It is Player 2's turn. Cannot execute move without first setting Player 1's ID.")
            else:
                if self.player_two.id != sanitised_player_id:
                    raise ValueError(
                        "It is Player 2's turn; (expected PlayerID {}), got PlayerID {})".format(
                            self.game.player_two_id,
                            sanitised_player_id
                        ))

        if sanitised_position not in self.game.get_valid_next_positions():
            raise ValueError(
                f"Invalid position specified; {sanitised_position.name} is already occupied."
            )

        move = GameMove(
            game_id=self.game.id,
            move_sequence=sanitised_move_sequence,
            player_number=self.game.next_move_player_number,
            player_id=sanitised_player_id,
            position=sanitised_position,
        )
        # Append the update to our set of DB transactions:
        db.session.add(move)

        # An update is required for Game model also:
        newly_updated_game = self.game.append_move(move.player_number, move.position)
        db.session.add(newly_updated_game)

        self.perform_automated_moves()

        # Commit all updates to the database:
        db.session.commit()

        # Todo: Return a RESULT object?
        return self.game

    def perform_automated_moves(self):
        if all([self.player_one, self.player_two, self.game]):

            while True:
                if self.game.status != GameStatus.IN_PROGRESS:
                    break

                if self.game.next_move_player_number == 1 and self.player_one.player_type == "human":
                    break

                if self.game.next_move_player_number == 2 and self.player_two.player_type == "human":
                    break

                # Decide what kind of move to make:
                valid_positions = self.game.get_valid_next_positions()

                # TODO: Add different computer difficulty levels.
                #       Use the 'Strategy' pattern; and allow trickier AIs to make better moves.
                selected_position = random.choice(valid_positions)

                move_sequence = self.game.next_move_sequence

                if self.game.next_move_player_number == 1:
                    player_id = self.game.player_one_id
                else:
                    player_id = self.game.player_two_id

                self.append_game_move(move_sequence=move_sequence, player_id=player_id, position=selected_position)
