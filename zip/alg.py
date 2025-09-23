def find_path(grid, walls = None):
    
    # directions: up, down, left, right
    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    n = len(grid)
    total = n * n
    
    if walls is None:
        walls = set()
    
    # find start cell (with value 1)
    start = [(r, c) for r in range(n) for c in range(n) if grid[r][c] == 1][0]
    path = [start]
    visited = {start}

    def dfs(r, c, next_required):
        if len(path) == total:
            return True  # success!

        for dr, dc in DIRS:
            rr, cc = r + dr, c + dc
            if 0 <= rr < n and 0 <= cc < n:
                if (rr, cc) in visited:
                    continue  # can't revisit

                # check for a wall between (r,c) and (rr,cc)
                if ((r, c), (rr, cc)) in walls:
                    continue

                val = grid[rr][cc]
                if val is not None and val != next_required:
                    continue  # must match required number

                visited.add((rr, cc))
                path.append((rr, cc))
                new_required = next_required + 1 if val == next_required else next_required

                if dfs(rr, cc, new_required):
                    return True  # found a full path

                # backtrack
                path.pop()
                visited.remove((rr, cc))

        return False

    dfs(*start, next_required=2)
    return path


# Testing
if __name__ == "__main__":
    from grid_utils import build_grid
    ordered_cells = [(0, None), (1, None), (2, None), (3, None), (4, None), (5, None), (6, None), (7, 1), (8, None), (9, None), (10, 2), (11, None), (12, None), (13, None), (14, 3), (15, 4), (16, None), (17, None), (18, None), (19, None), (20, 6), (21, 5), (22, None), (23, None), (24, None), (25, 8), (26, None), (27, None), (28, 7), (29, None), (30, None), (31, None), (32, None), (33, None), (34, None), (35, None)]
    walls = {((1, 1), (1, 0)), ((4, 4), (4, 5)), ((2, 4), (1, 4)), ((3, 2), (4, 2)), ((2, 1), (2, 2)), ((1, 3), (2, 3)), ((3, 1), (4, 1)), ((2, 3), (1, 3)), ((4, 1), (3, 1)), ((3, 3), (3, 4)), ((1, 1), (0, 1)), ((4, 5), (4, 4)), ((0, 1), (1, 1)), ((4, 2), (3, 2)), ((2, 2), (2, 1)), ((5, 4), (4, 4)), ((1, 4), (2, 4)), ((1, 0), (1, 1)), ((4, 4), (5, 4)), ((3, 4), (3, 3))}
    grid = build_grid(ordered_cells)
    solution = find_path(grid, walls)
    print("Solution path:", solution)
