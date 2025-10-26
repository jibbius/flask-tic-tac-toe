from typing import List
import random
from webapp.helpers import GamePosition
from webapp.models.game import Game
from webapp.bots.strategy import BotStrategy
from webapp.bots.utils import (
    get_winning_moves,
    get_blocking_moves,
    get_center_positions,
    get_corner_positions,
    get_edge_positions,
    is_a_corner,
    is_middle,
    is_an_edge,
    get_opposite_corner,
    simulate_move,
    is_winning_state
)


class ExpertBot(BotStrategy):
    """
    Expert difficulty bot - uses minimax algorithm for optimal play.
    
    Strategy:
    1. Take winning move if available
    2. Block opponent's winning move
    3. Use minimax algorithm to evaluate all possible moves
    4. Select the optimal move
    
    """
    
    def calculate_next_move(self, game: Game) -> GamePosition:
        """
        Calculate next move using expert-level strategy.
        
        Args:
            game: The current game state
            
        Returns:
            An optimally selected GamePosition
        """
        player_number = game.next_move_player_number
        board_state = game.board_state
        
        # 1. Check for winning moves (instant win)
        winning_moves = get_winning_moves(board_state, player_number)
        if winning_moves:
            return random.choice(winning_moves)
        
        # 2. Check for blocking moves (prevent instant loss)
        blocking_moves = get_blocking_moves(board_state, player_number)
        if blocking_moves:
            return random.choice(blocking_moves)
        
        # 3. Optimal move algorithm
        optimal_move = self.optimal_move(game)
        if optimal_move:
            return random.choice(optimal_move)
        
        # 3. Try to take center
        center_positions = get_center_positions(board_state)
        if center_positions:
            return center_positions[0]
        
        # 4. Try to take corners
        corner_positions = get_corner_positions(board_state)
        if corner_positions:
            return random.choice(corner_positions)
        
        # 5. Random valid move
        valid_positions = game.get_valid_next_positions()
        return random.choice(valid_positions)
    
    def optimal_move(self, game) -> List[GamePosition]:
        valid_positions = game.get_valid_next_positions()
        optimal_moves = []
        this_player_number = game.next_move_player_number
        other_player_number = 3 - this_player_number
        if(this_player_number == 1):

            # Strategy for the first player

            # If it's the first move, take a corner
            if(game.next_move_sequence == 1):
                corner_positions = get_corner_positions(game.board_state)
                if corner_positions:
                    return corner_positions
                
            # If it's the second move, next move differs based on:           
            if(game.next_move_sequence == 3):
                first_move = game.moves[0].position.value
                opponent_move = game.moves[1].position.value
                # A] Opponent took the middle (we shall take the corner that opposes our first move)
                if is_middle(opponent_move):
                    opposite_corner = get_opposite_corner(first_move)
                    if opposite_corner:
                        return [GamePosition(opposite_corner)]
                # B] Opponent took an edge (we shall take the middle)
                elif is_an_edge(opponent_move):
                    center_positions = get_center_positions(game.board_state)
                    if center_positions:
                        return center_positions
                # C] Opponent took the opposing corner (we shall take a 3rd corner)
                elif is_a_corner(opponent_move) and get_opposite_corner(first_move) == opponent_move:
                    corner_positions = get_corner_positions(game.board_state)
                    if corner_positions:
                        return corner_positions
                # D] Opponent took a non-opposing corner (we shall take the corner that opposes theirs)
                elif is_a_corner(opponent_move):
                    return [GamePosition(get_opposite_corner(opponent_move))]
                
        elif(this_player_number == 2):
            # Strategy for the second player
            if(game.next_move_sequence == 4):
                opponent_first_move = game.moves[0].position.value
                our_first_move = game.moves[1].position.value
                opponent_second_move = game.moves[2].position.value
                # This is our most dangerous turn
                if( is_a_corner(opponent_first_move) \
                   and is_middle(our_first_move) \
                   and opponent_second_move == get_opposite_corner(opponent_first_move)
                ):
                    edge_positions = get_edge_positions(game.board_state)
                    return edge_positions
               


        # See if we can create a fork, or block opponent's fork:
        for player_num in [this_player_number, other_player_number]:
            for pos in valid_positions:
                # Simulate placing our mark in this position
                simulated_state = simulate_move(game.board_state, player_num, pos)
                winning_moves = get_winning_moves(simulated_state, player_num)
                if len(winning_moves) >= 2:
                    optimal_moves.append(pos)
            if optimal_moves:
                return optimal_moves
            
        return optimal_moves