import time
import getpass
import argparse

from playwright.sync_api import sync_playwright

from helpers import get_full_json, parse_active_puzzle, get_solution_zip
from games.minisudoku import fill_sudoku
from games.zip import fill_zip
from games.tango import fill_tango
from games.queens import fill_queens
from games.pinpoint import fill_pinpoint
from games.crossClimb import fill_crossClimb

# Parse command-line arguments
parser = argparse.ArgumentParser(description='LinkedIn Games Automation Bot')
parser.add_argument('--profile', type=str, default='Profile 1',
                    help='Edge profile name (default: Profile 1)')
args = parser.parse_args()

# Auto-detect user's Edge profile
username = getpass.getuser()
EDGE_USER_DATA_DIR = rf"C:\Users\{username}\AppData\Local\Microsoft\Edge\User Data"
PROFILE_DIR = args.profile

PUZZLES = {
    "miniSudokuGamePuzzle": "https://www.linkedin.com/games/mini-sudoku",
    "lotkaGamePuzzle": "https://www.linkedin.com/games/tango",
    "queensGamePuzzle": "https://www.linkedin.com/games/queens",
    "trailGamePuzzle": "https://www.linkedin.com/games/zip",
    "blueprintGamePuzzle": "https://www.linkedin.com/games/pinpoint",
    "crossClimbGamePuzzle": "https://www.linkedin.com/games/crossclimb"
}

PUZZLE_FILLERS = {
    "miniSudokuGamePuzzle": fill_sudoku,
    "lotkaGamePuzzle": fill_tango,
    "queensGamePuzzle": fill_queens,
    "trailGamePuzzle": fill_zip,
    "blueprintGamePuzzle": fill_pinpoint,
    "crossClimbGamePuzzle": fill_crossClimb
}

p = sync_playwright().start()

browser = p.chromium.launch_persistent_context(
    user_data_dir=EDGE_USER_DATA_DIR,
    args=[f"--profile-directory={PROFILE_DIR}", "--start-maximized"],
    channel="msedge",
    headless=False,
    no_viewport=True
)
open_pages = []

for puzzle_name, puzzle_url in PUZZLES.items():
    print(f"\nOpening {puzzle_name} → {puzzle_url}")
    page = browser.new_page()
    open_pages.append(page)
    try:
        page.goto(puzzle_url)
        time.sleep(0.5)

        if puzzle_name == "trailGamePuzzle":
            print("Solving Zip (special case, no JSON)...")
            zip_solution = get_solution_zip(page)
            fill_zip(page, zip_solution)
        else:
            json_str = get_full_json(page)
            if not json_str:
                raise RuntimeError("Could not find JSON block")

            puzzle_info = parse_active_puzzle(json_str)
            if not puzzle_info:
                raise RuntimeError("Could not parse gamePuzzle")

            print(f"Parsed {puzzle_name}, running filler...")
            filler = PUZZLE_FILLERS[puzzle_name]
            filler(page, puzzle_info)

        print(f"{puzzle_name} completed.")

    except Exception as e:
        print(f"Error while solving {puzzle_name}: {e}")

    finally:
        time.sleep(0.3)
        
print("All puzzles processed. Browser will stay open until you press Enter.")
input()

browser.close()
p.stop()
