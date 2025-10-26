"""Utility functions for bot move calculations"""

from typing import List
from webapp.helpers import GamePosition
from webapp.models.game import Game


def get_winning_moves(board_state: str, player_number: int) -> List[GamePosition]:
    """
    Find moves that would win the game for the specified player.
    
    Args:
        game: The current game state
        player_number: The player number to check winning moves for (1 or 2)
        
    Returns:
        List of GamePosition objects that would result in a win
    """
    winning_moves = []
    valid_positions = Game.valid_next_positions(board_state)
    
    for position in valid_positions:
        # Simulate the move
        simulated_state = simulate_move(board_state, player_number, position)
        if is_winning_state(simulated_state, player_number):
            winning_moves.append(position)
    
    return winning_moves


def get_blocking_moves(board_state: str, player_number: int) -> List[GamePosition]:
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
    opponent_winning_moves = get_winning_moves(board_state, opponent_number)
    
    return opponent_winning_moves


def get_center_positions(board_state: str) -> List[GamePosition]:
    """
    Return center positions that are still available for strategic play.
    Assumes a 3x3 tic-tac-toe board where position 5 is center.
    
    Args:
        game: The current game state
        
    Returns:
        List of center GamePosition objects that are available
    """
    valid_positions = Game.valid_next_positions(board_state)
    
    # For a 3x3 board, center is position 5 (assuming 1-9 numbering)
    # Adjust this based on your actual GamePosition enum values
    center_position = GamePosition(5)
    
    if center_position in valid_positions:
        return [center_position]
    return []
def get_edge_positions(board_state: str) -> List[GamePosition]:

    """
    Return edge positions that are still available for strategic play.
    Assumes a 3x3 tic-tac-toe board where positions 2,4,6,8 are edges.
    
    Args:
        game: The current game state
    Returns:
        List of edge GamePosition objects that are available
    """
    valid_positions = Game.valid_next_positions(board_state)
    
    # For a 3x3 board, edges are positions 2, 4, 6, 8
    # Adjust this based on your actual GamePosition enum values
    edge_values = [2, 4, 6, 8]
    edges = [GamePosition(val) for val in edge_values]
    
    available_edges = [pos for pos in edges if pos in valid_positions]
    return available_edges

def is_a_corner(pos:int)->int:  
    return pos in [1, 3, 7, 9]

def is_an_edge(pos:int)->int:  
    return pos in [2, 4, 6, 8]

def is_middle(pos:int)->int:  
    return pos in [5]

def get_opposite_corner(pos:int)->int:
    opposite_corners = {1:9, 3:7, 7:3, 9:1}
    return opposite_corners.get(pos, None)

def get_corner_positions(board_state: str) -> List[GamePosition]:
    """
    Return corner positions that are still available for strategic play.
    Assumes a 3x3 tic-tac-toe board where positions 1,3,7,9 are corners.
    
    Args:
        game: The current game state
        
    Returns:
        List of corner GamePosition objects that are available
    """
    valid_positions = Game.valid_next_positions(board_state)
    
    # For a 3x3 board, corners are positions 1, 3, 7, 9
    # Adjust this based on your actual GamePosition enum values
    corner_values = [1, 3, 7, 9]
    corners = [GamePosition(val) for val in corner_values]
    
    available_corners = [pos for pos in corners if pos in valid_positions]
    return available_corners


def simulate_move(board_state: str, player_number: int, position: GamePosition) -> Game:
    """
    Simulate a move without modifying the actual game state.
    
    Args:
        board_state: The current game's board_state
        player_number: The player making the move
        position: The position to move to
        
    Returns:
        A new Game object with the simulated move applied
    """
    # Create a new board state string
    chars_before = position.value - 1
    chars_after = position.value
    new_board_state = board_state[0:chars_before] + str(player_number) + board_state[chars_after:]
    return new_board_state


def is_winning_state(board_state: str, player_number: int) -> bool:
    """
    Check if the game is in a winning state for the specified player.
    
    Args:
        game: The game state to check
        player_number: The player number to check for win
        
    Returns:
        True if the player has won, False otherwise
    """
    result = Game.check_for_winner(board_state)
    if(result):
        if(result.value == player_number):
            return True
    return False