"""Configuration and constants for bot difficulties"""

DIFFICULTY_EASY = "easy"
DIFFICULTY_MEDIUM = "medium"
DIFFICULTY_HARD = "hard"
DIFFICULTY_EXPERT = "expert"

AVAILABLE_DIFFICULTIES = [
    DIFFICULTY_EASY,
    DIFFICULTY_MEDIUM,
    DIFFICULTY_HARD,
    DIFFICULTY_EXPERT,
]

# Default difficulty if none specified or invalid difficulty provided
DEFAULT_DIFFICULTY = DIFFICULTY_EASY