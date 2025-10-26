import random
from webapp.helpers import GamePosition
from webapp.models.game import Game
from webapp.bots.strategy import BotStrategy
from webapp.bots.utils import get_winning_moves, get_blocking_moves, get_center_positions


class MediumBot(BotStrategy):
    """
    Medium difficulty bot - makes strategic moves with some intelligence.
    
    Strategy:
    1. Take winning move if available
    2. Block opponent's winning move
    3. Take center if available
    4. Otherwise, random move
    """
    
    def calculate_next_move(self, game: Game) -> GamePosition:
        """
        Calculate next move using medium-level strategy.
        
        Args:
            game: The current game state
            
        Returns:
            A strategically selected GamePosition
        """
        player_number = game.next_move_player_number
        
        # 1. Check for winning moves
        winning_moves = get_winning_moves(game, player_number)
        if winning_moves:
            return random.choice(winning_moves)
        
        # 2. Check for blocking moves
        blocking_moves = get_blocking_moves(game, player_number)
        if blocking_moves:
            return random.choice(blocking_moves)
        
        # 3. Try to take center
        center_positions = get_center_positions(game)
        if center_positions:
            return center_positions[0]
        
        # 4. Random valid move
        valid_positions = game.get_valid_next_positions()
        return random.choice(valid_positions)