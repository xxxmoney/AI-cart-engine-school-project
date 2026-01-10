import csv
import enum
import random
from collections import deque
from pathlib import Path
from typing import List, Optional, Dict, TypedDict
from constants import Tile

#
# How to run this file: python -m core.map_generator
#
# Algorithm for creating valid race map
# It consists of two main parts
# - The Walker (_solve_path)
#   - Start at the START tile and chooses random compatible tiles for next placement
#   - It does so until it hits dead end - in this case it uses backtracking - set previous tile as EMPTY and try again
#   - Or reaches the START tile again, thus creating loop
# - The Scout (has_path_to_start)
#   - Part of The Walker - it checks whether the current path can connect back to the start
#
# The algorithm is limited in:
# - MAX_DEPTH - how deep it can go in checking the path
# - MAX_ATTEMPTS - how many attempts it can try to generate the map
#


class Side(enum.Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


class Context(TypedDict):
    depth: int


NEXT_SIDES: Dict[Tile, List[Side]] = {
    Tile.HORIZONTAL: [Side.LEFT, Side.RIGHT],
    Tile.VERTICAL: [Side.TOP, Side.BOTTOM],
    Tile.LEFT_BOTTOM: [Side.TOP, Side.RIGHT],
    Tile.LEFT_TOP: [Side.BOTTOM, Side.RIGHT],
    Tile.RIGHT_TOP: [Side.LEFT, Side.BOTTOM],
    Tile.BOTTOM_RIGHT: [Side.LEFT, Side.TOP],
    Tile.HORIZONTAL_START: [Side.LEFT, Side.RIGHT],
    Tile.EMPTY: []
}

OPPOSITE = {
    Side.TOP: Side.BOTTOM,
    Side.BOTTOM: Side.TOP,
    Side.LEFT: Side.RIGHT,
    Side.RIGHT: Side.LEFT
}

MAX_ATTEMPTS = 50
MAX_DEPTH = 2000

class Map:
    grid: Optional[List[List[Tile]]]

    def __init__(self) -> None:
        self.grid = None

    def generate(self, width: int, height: int, start_x: Optional[int] = None, start_y: Optional[int] = None) -> bool:
        for attempt in range(MAX_ATTEMPTS):
            self.grid = [[Tile.EMPTY for _ in range(width)] for _ in range(height)]

            if start_x is None:
                start_x = random.randint(2, width - 3)
            if start_y is None:
                start_y = random.randint(2, height - 3)
            self.grid[start_y][start_x] = Tile.HORIZONTAL_START

            # Start moving RIGHT from the start tile
            delta_x, delta_y = 1, 0

            context: Context = {"depth": 0}

            if self.solve_path(start_x + delta_x, start_y + delta_y, Side.LEFT, width, height, start_x, start_y, 1, context):
                return True

        print("Could not generate a valid map within constraints.")
        return False

    @staticmethod
    def generate_maps(width: int, height: int, count: int, start_x: Optional[int] = None, start_y: Optional[int] = None):
        maps = []
        for index in range(count):
            print(f"Generating map {index}...")

            map = Map()
            if map.generate(width, height, start_x, start_y):
                maps.append(map)

            print(f"Generated map {index}")

        return maps


    def has_path_to_start(self, start_x: int, start_y: int, target_x: int, target_y: int, width: int, height: int):
        """
        BFS to check if the target (start tile) is reachable

        :param grid:
        :param start_x:
        :param start_y:
        :param target_x:
        :param target_y:
        :param width:
        :param height:
        :return:
        """

        if start_x == target_x and start_y == target_y:
            return True

        queue = deque([(start_x, start_y)])
        visited = {(start_x, start_y)}

        while queue:
            current_x, current_y = queue.popleft()

            for delta_x, delta_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbour_x, neighbour_y = current_x + delta_x, current_y + delta_y

                if 0 <= neighbour_x < width and 0 <= neighbour_y < height:
                    if (neighbour_x, neighbour_y) not in visited:
                        # Allow move if Empty OR if it's the Target
                        if self.grid[neighbour_y][neighbour_x] == Tile.EMPTY or (neighbour_x == target_x and neighbour_y == target_y):
                            if neighbour_x == target_x and neighbour_y == target_y:
                                return True
                            visited.add((neighbour_x, neighbour_y))
                            queue.append((neighbour_x, neighbour_y))
        return False


    def solve_path(self, x: int, y: int, entry_side: Side, width: int, height: int, start_x: int, start_y: int, length: int, context: Context):
        """
        Tries solving possible path recursively

        :param grid:
        :param x:
        :param y:
        :param entry_side:
        :param width:
        :param height:
        :param start_x:
        :param start_y:
        :param length:
        :param context:
        :return:
        """

        # Limit how deep it can check for solving path
        if context["depth"] > MAX_DEPTH:
            return False

        context["depth"] += 1

        # Check if the track loop has completed
        if x == start_x and y == start_y:
            if entry_side == Side.LEFT and length > 8:  # Min length constraint
                return True
            return False

        #  Check for bounds and collisions
        if not (0 <= x < width and 0 <= y < height):
            return False
        if self.grid[y][x] != Tile.EMPTY:
            return False

        # Get possible candidates for next tile
        candidates = []
        for tile in Tile:
            if tile == Tile.HORIZONTAL_START or tile == Tile.EMPTY:
                continue
            if entry_side in NEXT_SIDES[tile]:
                candidates.append(tile)

        random.shuffle(candidates)

        # Try possible candidates
        for tile in candidates:
            connections = NEXT_SIDES[tile]
            exits = [s for s in connections if s != entry_side]
            if not exits: continue
            exit_side = exits[0]

            delta_x, delta_y = 0, 0
            if exit_side == Side.TOP:
                delta_y = -1
            elif exit_side == Side.BOTTOM:
                delta_y = 1
            elif exit_side == Side.LEFT:
                delta_x = -1
            elif exit_side == Side.RIGHT:
                delta_x = 1

            next_x, next_y = x + delta_x, y + delta_y
            next_entry = OPPOSITE[exit_side]

            # Place tentatively
            self.grid[y][x] = tile

            # Reachability Check
            # Only check if we aren't closing the loop immediately
            path_possible = True
            if not (next_x == start_x and next_y == start_y):
                # Optim: Only run BFS every few steps or if close to edges
                if not self.has_path_to_start(next_x, next_y, start_x, start_y, width, height):
                    path_possible = False

            if path_possible:
                if self.solve_path(next_x, next_y, next_entry, width, height, start_x, start_y, length + 1, context):
                    return True

            # Backtrack - if path not possible and we can still try, revert to empty
            self.grid[y][x] = Tile.EMPTY

        return False


    def print(self):
        chars = {
            Tile.HORIZONTAL: "═", Tile.VERTICAL: "║",
            Tile.LEFT_BOTTOM: "╚", Tile.LEFT_TOP: "╔",
            Tile.RIGHT_TOP: "╗", Tile.BOTTOM_RIGHT: "╝",
            Tile.HORIZONTAL_START: "S", Tile.EMPTY: " "
        }

        print("-" * (len(self.grid[0]) + 2))
        for row in self.grid:
            print("|" + "".join(chars[tile] for tile in row) + "|")
        print("-" * (len(self.grid[0]) + 2))

    def save_as_csv(self, path: Path):
        with open(path, mode='w', newline='') as f:
            writer = csv.writer(f)
            for row in self.grid:
                writer.writerow([tile.value for tile in row])


if __name__ == "__main__":
    BASE_PATH = Path(__file__).parent

    # Defined start and with of map
    start_x, start_y = 5, 9
    width, height = 10, 10

    # How many maps to generate
    count = 5

    # Generate the map
    maps = Map.generate_maps(width, height, count, start_x, start_y)
    folder_path = BASE_PATH / ".." / "UserData" / "generated"
    easy_path = folder_path / "easy"
    medium_path = folder_path / "medium"
    hard_path = folder_path / "hard"

    for i, map in enumerate(maps):
        path = folder_path / f"map_generated_{i:02d}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)

        map.save_as_csv(path)
        map.print()
