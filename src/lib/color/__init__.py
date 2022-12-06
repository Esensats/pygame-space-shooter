""" Store color codes and their names in CLR_CODE and aliases for the game in CLR"""

from enum import Enum
from typing import Dict, Tuple


class Code:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (127, 127, 127)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


# CLR: Dict[str, Tuple[int, int, int]] = {
#     "BACKGROUND": Code["WHITE"],
#     "BORDER": Code["GRAY"],
# }


class Alias:
    BACKGROUND = Code.WHITE
    BORDER = Code.WHITE
    TEXT = Code.WHITE
