import enum
import random
import sys
from typing import List, Optional, Dict

# Increase recursion depth for deep pathfinding if needed
sys.setrecursionlimit(2000)


class Tiles(str, enum.Enum):
    HORIZONTAL = "road_dirt01"
    VERTICAL = "road_dirt90"
    LEFT_BOTTOM = "road_dirt38"
    LEFT_TOP = "road_dirt02"
    RIGHT_TOP = "road_dirt04"
    BOTTOM_RIGHT = "road_dirt40"
    HORIZONTAL_START = "road_dirt42"
    EMPTY = "land_grass04"


class Sides(enum.Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


# Rules: which tiles can be next to road tiles
NEXT_SIDES: Dict[Tiles, List[Sides]] = {
    Tiles.HORIZONTAL: [Sides.LEFT, Sides.RIGHT],
    Tiles.VERTICAL: [Sides.TOP, Sides.BOTTOM],
    Tiles.LEFT_BOTTOM: [Sides.TOP, Sides.RIGHT],
    Tiles.LEFT_TOP: [Sides.BOTTOM, Sides.RIGHT],
    Tiles.RIGHT_TOP: [Sides.LEFT, Sides.BOTTOM],
    Tiles.BOTTOM_RIGHT: [Sides.LEFT, Sides.TOP],
    Tiles.HORIZONTAL_START: [Sides.LEFT, Sides.RIGHT],
    Tiles.EMPTY: []
}

OPPOSITE = {
    Sides.TOP: Sides.BOTTOM,
    Sides.BOTTOM: Sides.TOP,
    Sides.LEFT: Sides.RIGHT,
    Sides.RIGHT: Sides.LEFT
}


def generate_map(width: int, height: int) -> List[List[Tiles]]:
    # Retry wrapper to handle occasional dead-end generations
    for attempt in range(100):
        grid = [[Tiles.EMPTY for _ in range(width)] for _ in range(height)]

        # 1. Place Start Tile
        start_x = random.randint(2, width - 3)
        start_y = random.randint(2, height - 3)
        grid[start_y][start_x] = Tiles.HORIZONTAL_START

        # 2. Start recursion
        # We force a move to the RIGHT from the start tile to begin the loop.
        # This implies we must eventually re-enter the Start tile from the LEFT.
        start_side = Sides.RIGHT
        dx, dy = 1, 0  # Moving Right

        if _solve_path(grid, start_x + dx, start_y + dy, Sides.LEFT, width, height, start_x, start_y, 1):
            return grid

    # Fallback if generation fails (return empty or simple grid)
    print("Failed to generate closed loop after retries.")
    return grid


def _solve_path(grid, x, y, entry_side, width, height, start_x, start_y, length):
    """
    Recursive Backtracking (DFS) to find a closed loop.
    x, y: Current coordinates to place a tile
    entry_side: The side of the current tile we are entering from
    """

    # 1. Check if we reached the start (Closing the Loop)
    if x == start_x and y == start_y:
        # We need to enter the start tile from the LEFT (since we left RIGHT).
        # entry_side here represents the side of the Start Tile we are entering.
        if entry_side == Sides.LEFT and length > 6:  # Min length to prevent tiny loops
            return True
        return False

    # 2. Bounds and Overlap Checks
    if not (0 <= x < width and 0 <= y < height):
        return False
    if grid[y][x] != Tiles.EMPTY:
        return False

    # 3. Find Candidates
    candidates = []
    for tile in Tiles:
        # Don't place another start or empty
        if tile == Tiles.HORIZONTAL_START or tile == Tiles.EMPTY:
            continue

        # Must have a connection to where we came from
        if entry_side in NEXT_SIDES[tile]:
            candidates.append(tile)

    # Shuffle for random path generation
    random.shuffle(candidates)

    # 4. Try Candidates
    for tile in candidates:
        # Determine exit side
        connections = NEXT_SIDES[tile]
        exits = [s for s in connections if s != entry_side]

        if not exits: continue
        exit_side = exits[0]  # Assuming 2-way tiles

        # Place tile tentatively
        grid[y][x] = tile

        # Calculate next coordinates
        dx, dy = 0, 0
        if exit_side == Sides.TOP:
            dy = -1
        elif exit_side == Sides.BOTTOM:
            dy = 1
        elif exit_side == Sides.LEFT:
            dx = -1
        elif exit_side == Sides.RIGHT:
            dx = 1

        next_entry = OPPOSITE[exit_side]

        # Recurse
        if _solve_path(grid, x + dx, y + dy, next_entry, width, height, start_x, start_y, length + 1):
            return True

        # Backtrack: Remove tile if it leads to dead end
        grid[y][x] = Tiles.EMPTY

    return False


def print_map(grid):
    chars = {
        Tiles.HORIZONTAL: "═", Tiles.VERTICAL: "║",
        Tiles.LEFT_BOTTOM: "╚", Tiles.LEFT_TOP: "╔",
        Tiles.RIGHT_TOP: "╗", Tiles.BOTTOM_RIGHT: "╝",
        Tiles.HORIZONTAL_START: "S", Tiles.EMPTY: " "  # Changed Start to 'S'
    }

    print("-" * (len(grid[0]) + 2))
    for row in grid:
        print("|" + "".join(chars[tile] for tile in row) + "|")
    print("-" * (len(grid[0]) + 2))


if __name__ == "__main__":
    map_data = generate_map(10, 10)
    print_map(map_data)