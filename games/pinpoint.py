from helpers import is_puzzle_completed

def fill_pinpoint(page, puzzle):
    
    if is_puzzle_completed(page):
        print("Pinpoint already completed, skipping.")
        return
    
    solutions = puzzle.get("solutions", [])
    answer = solutions[0]
    page.keyboard.type(f"{answer}")
    page.keyboard.press("Enter")