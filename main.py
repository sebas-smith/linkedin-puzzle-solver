from playwright.sync_api import sync_playwright
import time
from helpers import get_full_json, parse_active_puzzle, get_solution_zip
from games.minisudoku import fill_sudoku
from games.zip import fill_zip
# from games.tango import fill_tango
# from games.queens import fill_queens
# from games.pinpoint import fill_pinpoint
# from games.crossClimb import fill_crossClimb
import json

EDGE_USER_DATA_DIR = r"C:\Users\sebeg\AppData\Local\Microsoft\Edge\User Data"
PROFILE_DIR = "Profile 1"

# PUZZLES = {
#     "miniSudokuGamePuzzle": "https://www.linkedin.com/games/mini-sudoku",
#     "lotkaGamePuzzle": "https://www.linkedin.com/games/lotka",
#     "queensGamePuzzle": "https://www.linkedin.com/games/queens",
#     "trailGamePuzzle": "https://www.linkedin.com/games/zip",
#     "blueprintGamePuzzle": "https://www.linkedin.com/games/pinpoint",
#     "crossClimbGamePuzzle": "https://www.linkedin.com/games/crossclimb"
# }

# PUZZLE_FILLERS = {
#     "miniSudokuGamePuzzle": fill_sudoku,
#     "lotkaGamePuzzle": fill_tango,
#     "queensGamePuzzle": fill_queens,
#     "trailGamePuzzle": fill_zip,
#     "blueprintGamePuzzle": fill_pinpoint,
#     "crossClimbGamePuzzle": fill_crossClimb
# }

PUZZLE_URL = "https://www.linkedin.com/games/zip"


with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=EDGE_USER_DATA_DIR,
        args=[f"--profile-directory={PROFILE_DIR}"],
        channel="msedge",
        headless=False
    )

    page = browser.new_page()
    page.goto(PUZZLE_URL)
    time.sleep(1)  # wait for content to load

    zip_solution = get_solution_zip(page)
    fill_zip(page, zip_solution)
    # json_str = get_full_json(page)
    # if not json_str:
    #     raise RuntimeError("Could not find Mini Sudoku JSON block")

    # puzzle_info = parse_active_puzzle(json_str)
    # if not puzzle_info:
    #     raise RuntimeError("Could not find Mini Sudoku gamePuzzle")
    # print(json.dumps(puzzle_info, indent = 4))
    # fill_sudoku(page, puzzle_info)