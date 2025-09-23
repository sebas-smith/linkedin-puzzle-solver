import time


def fill_sudoku(page, puzzle):
    """
    Fill the Sudoku puzzle on the page based on the solution.
    Assumes solution is a flat list of integers and uses data-cell-idx for targeting.
    """
    solution = puzzle.get("solution", [])
    preset = puzzle.get("presetCellIdxes", [])

    for idx, value in enumerate(solution):
        if idx in preset:
            continue  # skip preset cells

        selector = f"div.sudoku-cell[data-cell-idx='{idx}']"
        cell = page.query_selector(selector)
        if not cell:
            continue  # cell not found, skip it

        cell.click()
        page.keyboard.type(str(value))
        time.sleep(0.02)  # small delay to look more human
