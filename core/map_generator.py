import enum

class Tiles(str, enum):
    HORIZONTAL = "road_dirt01",
    VERTICAL = "road_dirt90",
    LEFT_BOTTOM = "road_dirt38",
    LEFT_TOP = "road_dirt02",
    RIGHT_TOP = "road_dirt04",
    BOTTOM_RIGHT = "road_dirt40",
    HORIZONTAL_START = "road_dirt42",
    EMPTY = "land_grass04"

class Sides(enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4

NEXT_SIDES = {
    Tiles.HORIZONTAL: [Sides.LEFT, Sides.RIGHT],
    Tiles.VERTICAL: [Sides.TOP, Sides.BOTTOM],
    Tiles.LEFT_BOTTOM: [Sides.TOP, Sides.RIGHT],
    Tiles.LEFT_TOP: [Sides.BOTTOM, Sides.RIGHT],
    Tiles.RIGHT_TOP: [Sides.LEFT, Sides.BOTTOM],
    Tiles.BOTTOM_RIGHT: [Sides.LEFT, Sides.TOP],
    Tiles.HORIZONTAL_START: [Sides.LEFT],
    Tiles.EMPTY: [Sides.TOP, Sides.RIGHT, Sides.BOTTOM, Sides.LEFT]
}


