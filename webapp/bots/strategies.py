"""Factory for creating bot instances based on difficulty"""

from typing import Dict, Type
from webapp.bots.strategy import BotStrategy
from webapp.bots.difficulties import EasyBot, MediumBot, HardBot, ExpertBot
from webapp.bots.config import (
    DIFFICULTY_EASY,
    DIFFICULTY_MEDIUM,
    DIFFICULTY_HARD,
    DIFFICULTY_EXPERT,
    DEFAULT_DIFFICULTY
)


def get_bot_strategy(difficulty: str = DEFAULT_DIFFICULTY) -> BotStrategy:
    """
    Factory function to get the appropriate bot strategy based on difficulty.
    
    Args:
        difficulty: The difficulty level ("easy", "medium", "hard", or "expert")
        
    Returns:
        BotStrategy: An instance of the appropriate bot strategy
        
    Examples:
        >>> bot = get_bot_strategy("easy")
        >>> bot = get_bot_strategy("hard")
        >>> bot = get_bot_strategy()  # Returns easy bot by default
    """
    strategies: Dict[str, Type[BotStrategy]] = {
        DIFFICULTY_EASY: EasyBot,
        DIFFICULTY_MEDIUM: MediumBot,
        DIFFICULTY_HARD: HardBot,
        DIFFICULTY_EXPERT: ExpertBot,
    }
    
    # Get the bot class, defaulting to EasyBot if difficulty not found
    bot_class = strategies.get(difficulty.lower(), EasyBot)
    
    # Return an instance of the bot
    return bot_class()