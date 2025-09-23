import time


def fill_zip(page, solution):

    for idx in solution:

        selector = f"div.sudoku-cell[data-cell-idx='{idx}']"
        cell = page.query_selector(selector)
        if not cell:
            continue  # cell not found, skip it

        cell.click()
        time.sleep(0.02)  # small delay to look more human
