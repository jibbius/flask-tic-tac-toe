"""Utility functions for bot move calculations"""

from typing import List
from webapp.helpers import GamePosition
from webapp.models.game import Game


def get_winning_moves(game: Game, player_number: int) -> List[GamePosition]:
    """
    Find moves that would win the game for the specified player.
    
    Args:
        game: The current game state
        player_number: The player number to check winning moves for (1 or 2)
        
    Returns:
        List of GamePosition objects that would result in a win
    """
    winning_moves = []
    valid_positions = game.get_valid_next_positions()
    
    for position in valid_positions:
        # Simulate the move
        test_game = _simulate_move(game, player_number, position)
        if _is_winning_state(test_game, player_number):
            winning_moves.append(position)
    
    return winning_moves


def get_blocking_moves(game: Game, player_number: int) -> List[GamePosition]:
    """
    Find moves that would block the opponent from winning on their next turn.
    
    Args:
        game: The current game state
        player_number: The player number making the blocking move (1 or 2)
        
    Returns:
        List of GamePosition objects that would block opponent's win
    """
    opponent_number = 2 if player_number == 1 else 1
    
    # Find opponent's winning moves
    opponent_winning_moves = get_winning_moves(game, opponent_number)
    
    return opponent_winning_moves


def get_center_positions(game: Game) -> List[GamePosition]:
    """
    Return center positions that are still available for strategic play.
    Assumes a 3x3 tic-tac-toe board where position 5 is center.
    
    Args:
        game: The current game state
        
    Returns:
        List of center GamePosition objects that are available
    """
    valid_positions = game.get_valid_next_positions()
    
    # For a 3x3 board, center is position 5 (assuming 1-9 numbering)
    # Adjust this based on your actual GamePosition enum values
    center_position = GamePosition(5)
    
    if center_position in valid_positions:
        return [center_position]
    return []


def get_corner_positions(game: Game) -> List[GamePosition]:
    """
    Return corner positions that are still available for strategic play.
    Assumes a 3x3 tic-tac-toe board where positions 1,3,7,9 are corners.
    
    Args:
        game: The current game state
        
    Returns:
        List of corner GamePosition objects that are available
    """
    valid_positions = game.get_valid_next_positions()
    
    # For a 3x3 board, corners are positions 1, 3, 7, 9
    # Adjust this based on your actual GamePosition enum values
    corner_values = [1, 3, 7, 9]
    corners = [GamePosition(val) for val in corner_values]
    
    available_corners = [pos for pos in corners if pos in valid_positions]
    return available_corners


def _simulate_move(game: Game, player_number: int, position: GamePosition) -> Game:
    """
    Simulate a move without modifying the actual game state.
    
    Args:
        game: The current game state
        player_number: The player making the move
        position: The position to move to
        
    Returns:
        A new Game object with the simulated move applied
    """
    # TODO: Implement actual game state simulation
    # This is a placeholder that needs to be implemented based on your Game model
    # You may need to create a copy of the game and apply the move
    pass


def _is_winning_state(game: Game, player_number: int) -> bool:
    """
    Check if the game is in a winning state for the specified player.
    
    Args:
        game: The game state to check
        player_number: The player number to check for win
        
    Returns:
        True if the player has won, False otherwise
    """
    # TODO: Implement win condition checking
    # This is a placeholder that needs to be implemented based on your Game model
    pass