from helpers import is_puzzle_completed

def fill_queens(page, puzzle):
    
    if is_puzzle_completed(page):
        print("Queens already completed, skipping.")
        return
    
    """
    Fill the Tango puzzle based on its solution.
    Uses pre-fetching to reduce Playwright query overhead.
    """
    solution = puzzle.get("solution", [])
    gridsize = int(puzzle.get("gridSize"))
    # Pre-fetch elements for all cells that need input
    elements = []
    for cell in solution:
        row = cell["row"]
        col = cell["col"]
        
        idx = row * gridsize + col
        cell = page.query_selector(f"[data-cell-idx='{idx}']")
        if cell:
            elements.append(cell)

    for el in elements:
        el.click(click_count = 2)