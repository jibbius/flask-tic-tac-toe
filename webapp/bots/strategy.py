
from abc import ABC, abstractmethod
from webapp.helpers import GamePosition
from webapp.models.game import Game


class BotStrategy(ABC):
    """Base class for bot move calculation strategies"""
    
    @abstractmethod
    def calculate_next_move(self, game: Game) -> GamePosition:
        """
        Calculate the next move for the bot player.
        
        Args:
            game: The current game state
            
        Returns:
            GamePosition: The position where the bot chooses to move
        """
        pass