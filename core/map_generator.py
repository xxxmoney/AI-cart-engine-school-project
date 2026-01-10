import enum
import random
import time
from collections import deque
from typing import List, Optional, Dict


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


def generate_map(width: int, height: int) -> Optional[List[List[Tiles]]]:
    # Attempt generation multiple times, but fail fast on each
    # to prevent UI freezes.
    max_attempts = 50

    for attempt in range(max_attempts):
        grid = [[Tiles.EMPTY for _ in range(width)] for _ in range(height)]

        start_x = random.randint(2, width - 3)
        start_y = random.randint(2, height - 3)
        grid[start_y][start_x] = Tiles.HORIZONTAL_START

        # Operation context to limit computation per attempt
        # 'ops': Current number of recursive steps/checks
        # 'limit': Max steps allowed before aborting this attempt
        ctx = {"ops": 0, "limit": 2000}

        # Start moving RIGHT from the start tile
        dx, dy = 1, 0

        if _solve_path(grid, start_x + dx, start_y + dy, Sides.LEFT, width, height, start_x, start_y, 1, ctx):
            return grid

    print("Could not generate a valid map within constraints.")
    return None


def has_path_to_start(grid, start_x, start_y, target_x, target_y, width, height):
    """
    BFS to check if the target (start tile) is reachable.
    """
    if start_x == target_x and start_y == target_y:
        return True

    queue = deque([(start_x, start_y)])
    visited = {(start_x, start_y)}

    while queue:
        cx, cy = queue.popleft()

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    # Allow move if Empty OR if it's the Target
                    if grid[ny][nx] == Tiles.EMPTY or (nx == target_x and ny == target_y):
                        if nx == target_x and ny == target_y:
                            return True
                        visited.add((nx, ny))
                        queue.append((nx, ny))
    return False


def _solve_path(grid, x, y, entry_side, width, height, start_x, start_y, length, ctx):
    # 1. Anti-Freeze Check
    ctx["ops"] += 1
    if ctx["ops"] > ctx["limit"]:
        return False

    # 2. Check for Loop Completion
    if x == start_x and y == start_y:
        if entry_side == Sides.LEFT and length > 8:  # Min length constraint
            return True
        return False

    # 3. Bounds/Collision
    if not (0 <= x < width and 0 <= y < height):
        return False
    if grid[y][x] != Tiles.EMPTY:
        return False

    # 4. Filter Candidates
    candidates = []
    for tile in Tiles:
        if tile == Tiles.HORIZONTAL_START or tile == Tiles.EMPTY:
            continue
        if entry_side in NEXT_SIDES[tile]:
            candidates.append(tile)

    random.shuffle(candidates)

    # 5. Try Candidates
    for tile in candidates:
        connections = NEXT_SIDES[tile]
        exits = [s for s in connections if s != entry_side]
        if not exits: continue
        exit_side = exits[0]

        dx, dy = 0, 0
        if exit_side == Sides.TOP:
            dy = -1
        elif exit_side == Sides.BOTTOM:
            dy = 1
        elif exit_side == Sides.LEFT:
            dx = -1
        elif exit_side == Sides.RIGHT:
            dx = 1

        next_x, next_y = x + dx, y + dy
        next_entry = OPPOSITE[exit_side]

        # Place tentatively
        grid[y][x] = tile

        # 6. Reachability Check (Heuristic)
        # Only check if we aren't closing the loop immediately
        path_possible = True
        if not (next_x == start_x and next_y == start_y):
            # Optim: Only run BFS every few steps or if close to edges?
            # For now, we rely on ctx['limit'] to catch expensive cases.
            if not has_path_to_start(grid, next_x, next_y, start_x, start_y, width, height):
                path_possible = False

        if path_possible:
            if _solve_path(grid, next_x, next_y, next_entry, width, height, start_x, start_y, length + 1, ctx):
                return True

        # Backtrack
        grid[y][x] = Tiles.EMPTY

    return False


def print_map(grid):
    if not grid:
        print("No Map Generated")
        return

    chars = {
        Tiles.HORIZONTAL: "═", Tiles.VERTICAL: "║",
        Tiles.LEFT_BOTTOM: "╚", Tiles.LEFT_TOP: "╔",
        Tiles.RIGHT_TOP: "╗", Tiles.BOTTOM_RIGHT: "╝",
        Tiles.HORIZONTAL_START: "S", Tiles.EMPTY: " "
    }

    print("-" * (len(grid[0]) + 2))
    for row in grid:
        print("|" + "".join(chars[tile] for tile in row) + "|")
    print("-" * (len(grid[0]) + 2))


if __name__ == "__main__":
    start_time = time.time()
    map_data = generate_map(15, 10)
    print(f"Generation took: {time.time() - start_time:.4f}s")
    print_map(map_data)