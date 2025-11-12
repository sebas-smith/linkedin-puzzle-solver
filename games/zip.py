from helpers import is_puzzle_completed

def fill_zip(page, solution):
    
    if is_puzzle_completed(page, iszip = True):
        print("Zip already completed, skipping.")
        return
    
    elements = []
    for idx in solution:
        el = page.query_selector(f"[data-cell-idx='{idx}']")
        if el:
            elements.append(el)

    for el in elements:
        el.click()
