# get_puzzle_json.py
from playwright.sync_api import sync_playwright
import json
import time
from helpers import get_full_json, parse_active_puzzle

EDGE_USER_DATA_DIR = r"C:\Users\sebeg\AppData\Local\Microsoft\Edge\User Data"
PROFILE_DIR = "Profile 1"

PUZZLES = {
    "miniSudokuGamePuzzle": "https://www.linkedin.com/games/mini-sudoku",
    "lotkaGamePuzzle": "https://www.linkedin.com/games/tango",
    "queensGamePuzzle": "https://www.linkedin.com/games/queens",
    "trailGamePuzzle": "https://www.linkedin.com/games/zip",
    "blueprintGamePuzzle": "https://www.linkedin.com/games/pinpoint",
    "crossClimbGamePuzzle": "https://www.linkedin.com/games/crossclimb"
}

# Change this to whichever puzzle you want to inspect
PUZZLE_NAME = "miniSudokuGamePuzzle"

p = sync_playwright().start()

browser = p.chromium.launch_persistent_context(
    user_data_dir=EDGE_USER_DATA_DIR,
    args=[f"--profile-directory={PROFILE_DIR}"],
    channel="msedge",
    headless=False
)

page = browser.new_page()
page.goto(PUZZLES[PUZZLE_NAME])
time.sleep(0.5)  # wait for content to load

json_str = get_full_json(page)
if not json_str:
    raise RuntimeError("❌ Could not find JSON block on page.")

puzzle_info = parse_active_puzzle(json_str)
if not puzzle_info:
    raise RuntimeError("❌ Could not parse puzzle info from JSON.")

print(f"✅ Puzzle data for {PUZZLE_NAME}:")
print(json.dumps(puzzle_info, indent=4))

browser.close()
p.stop()
