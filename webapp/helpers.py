from dataclasses import dataclass, field
from enum import Enum

from flask import url_for


@dataclass
class ApiEndpoint:
    """
    This class helps us to generate our API page.
    """
    model: str
    title: str
    handle: str
    method: str
    template: str
    default_params: dict = field(default_factory=dict)

    def url(self):
        if self.default_params:
            return url_for(self.handle, **self.default_params)
        else:
            return url_for(self.handle)


class GameStatus(Enum):
    IN_PROGRESS = 1
    FINISHED = 2


class WinningPlayerNum(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    TIE = 3


class GamePosition(Enum):
    TOP_ROW_LEFT_COL = 1
    TOP_ROW_CENTER_COL = 2
    TOP_ROW_RIGHT_COL = 3
    MIDDLE_ROW_LEFT_COL = 4
    MIDDLE_ROW_CENTER_COL = 5
    MIDDLE_ROW_RIGHT_COL = 6
    BOTTOM_ROW_LEFT_COL = 7
    BOTTOM_ROW_CENTER_COL = 8
    BOTTOM_ROW_RIGHT_COL = 9
