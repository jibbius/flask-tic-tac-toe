"""
Bots module for automated game players and strategies
"""

from webapp.bots.strategy import BotStrategy
from webapp.bots.difficulties import EasyBot, MediumBot, HardBot, ExpertBot
from webapp.bots.factory import get_bot_strategy
from webapp.bots.config import (
    DIFFICULTY_EASY,
    DIFFICULTY_MEDIUM,
    DIFFICULTY_HARD,
    DIFFICULTY_EXPERT,
    AVAILABLE_DIFFICULTIES,
    DEFAULT_DIFFICULTY
)

__all__ = [
    # Base class
    'BotStrategy',
    
    # Bot implementations
    'EasyBot',
    'MediumBot',
    'HardBot',
    'ExpertBot',
    
    # Factory
    'get_bot_strategy',
    
    # Configuration
    'DIFFICULTY_EASY',
    'DIFFICULTY_MEDIUM',
    'DIFFICULTY_HARD',
    'DIFFICULTY_EXPERT',
    'AVAILABLE_DIFFICULTIES',
    'DEFAULT_DIFFICULTY',
]