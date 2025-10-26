from webapp.helpers import GamePosition, GameStatus
from webapp.models.player import Player
from webapp.models.game import Game
from webapp.models.game_move import GameMove
from webapp.models.base import db
from webapp.bots import get_bot_strategy


class GameService:
    """Service for managing game state and player interactions"""
    
    player_one: Player
    player_two: Player
    game: Game

    def __init__(self, player_one_id: int = None, player_two_id: int = None, game_id: int = None):
        """
        Initialize the game service with players and/or existing game.
        
        Args:
            player_one_id: Optional ID of player one
            player_two_id: Optional ID of player two
            game_id: Optional ID of existing game to load
        """
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
        """
        Create a new game and perform any necessary automated moves.
        
        Returns:
            Game: The newly created game
        """
        if not all([self.player_one, self.player_two]):
            raise ValueError(f"Cannot create game without first specifying player IDs.")

        self.game = Game(self.player_one.id, self.player_two.id)

        # Append to database:
        db.session.add(self.game)
        db.session.commit()  # Need to commit, prior to automated moves. This ensures that we have a GameId.

        # Determine if any automated moves to be executed
        self._perform_automated_moves()

        return self.game

    def append_game_move(self, move_sequence: int, player_id: int, position: GamePosition) -> Game:
        """
        Add a move to the game and update game state.
        
        Args:
            move_sequence: The sequence number of this move
            player_id: The ID of the player making the move
            position: The position to place the move
            
        Returns:
            Game: The updated game
        """
        # Sanitise inputs:
        sanitised_move_sequence = int(move_sequence)
        sanitised_player_id = int(player_id)
        sanitised_position = self._sanitise_position(position)

        # Validate inputs
        self._validate_move(sanitised_move_sequence, sanitised_player_id, sanitised_position)

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

        self._perform_automated_moves()

        # Commit all updates to the database:
        db.session.commit()

        return self.game
    
    def get_next_turn_player(self) -> Player:
        """
        Get the player type of whoever's turn it is next.
        
        Returns:
            str: The player type ("human" or "computer") or None if game is over
        """
        if self.game.status == GameStatus.IN_PROGRESS:
            if self.game.next_move_player_number == 1:
                return self.player_one
            else:
                return self.player_two
        else:
            return None


    def get_last_move_position(self):
        """
        Get the position of the most recent move.
        
        Returns:
            int: The position value of the last move, or None if no moves yet
        """
        last_move = self.game.moves.order_by(GameMove.move_sequence.desc()).first()
        if not last_move:
            return None
        return last_move.position.value

    def _sanitise_position(self, position) -> GamePosition:
        """Sanitise position input to GamePosition enum"""
        if type(position) == str:
            return GamePosition(int(position))
        elif type(position) == int:
            return GamePosition(position)
        elif type(position) == GamePosition:
            return position
        else:
            raise ValueError("Unexpected GamePosition type")

    def _validate_move(self, move_sequence: int, player_id: int, position: GamePosition):
        """Validate that a move is legal"""
        if not self.game:
            raise ValueError("Invalid Game ID")

        if self.game.status != GameStatus.IN_PROGRESS:
            raise ValueError(f"No further moves allowed; Game status = {self.game.status.name}")

        if move_sequence != self.game.next_move_sequence:
            raise ValueError(
                f"Unexpected move sequence (expected {self.game.next_move_sequence}, got {move_sequence})")

        if self.game.next_move_player_number == 1:
            if not self.player_one:
                raise ValueError(f"It is Player 1's turn. Cannot execute move without first setting Player 1's ID.")
            else:
                if self.player_one.id != player_id:
                    raise ValueError(
                        "It is Player 1's turn; (expected PlayerID {}), got PlayerID {})".format(
                            self.game.player_one_id,
                            player_id
                        ))
        elif self.game.next_move_player_number == 2:
            if not self.player_two:
                raise ValueError(f"It is Player 2's turn. Cannot execute move without first setting Player 2's ID.")
            else:
                if self.player_two.id != player_id:
                    raise ValueError(
                        "It is Player 2's turn; (expected PlayerID {}), got PlayerID {})".format(
                            self.game.player_two_id,
                            player_id
                        ))

        if position not in self.game.get_valid_next_positions():
            raise ValueError(
                f"Invalid position specified; {position.name} is already occupied."
            )

    def _perform_automated_moves(self):
        """Execute moves for bot players until a human player's turn or game ends"""
        if all([self.player_one, self.player_two, self.game]):

            while True:
                if self.game.status != GameStatus.IN_PROGRESS:
                    break

                next_player = self.get_next_turn_player()

                if next_player.player_type == "human":
                    break

                if next_player.player_type == "computer":
                    # Get bot strategy and calculate move
                    bot_strategy = get_bot_strategy(next_player.bot_difficulty)
                    selected_position = bot_strategy.calculate_next_move(self.game)
                    self.append_game_move(move_sequence=self.game.next_move_sequence,
                                        player_id=next_player.id,
                                        position=selected_position)