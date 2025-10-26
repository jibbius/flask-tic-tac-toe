import random
from webapp.helpers import GamePosition
from webapp.models.game import Game
from webapp.bots.strategy import BotStrategy


class EasyBot(BotStrategy):
    """Easy difficulty bot - makes random valid moves"""
    
    def calculate_next_move(self, game: Game) -> GamePosition:
        """
        Select a random valid position.
        
        Args:
            game: The current game state
            
        Returns:
            A randomly selected valid GamePosition
        """
        valid_positions = game.get_valid_next_positions()
        return random.choice(valid_positions)