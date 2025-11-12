from helpers import is_puzzle_completed

def fill_sudoku(page, puzzle):
    
    if is_puzzle_completed(page):
        print("Sudoku already completed, skipping.")
        return
    
    """
    Fill the Sudoku puzzle based on its solution.
    Uses pre-fetching to reduce Playwright query overhead.
    """
    solution = puzzle.get("solution", [])
    preset = puzzle.get("presetCellIdxes", [])

    # Pre-fetch elements for all cells that need input
    actions = []
    for idx, value in enumerate(solution):
        if idx in preset:
            continue  # skip preset cells

        cell = page.query_selector(f"[data-cell-idx='{idx}']")
        if cell:
            actions.append((cell, value))

    # Perform all clicks and typing back-to-back
    for cell, value in actions:
        cell.click()
        page.keyboard.type(str(value))