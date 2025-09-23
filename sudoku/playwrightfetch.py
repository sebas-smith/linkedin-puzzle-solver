from playwright.sync_api import sync_playwright
import json
import html
import time

edge_user_data_dir = r"C:\Users\sebeg\AppData\Local\Microsoft\Edge\User Data"

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=edge_user_data_dir,
        args=[r"--profile-directory=Profile 1"],
        channel="msedge",
        headless=False
    )

    page = browser.new_page()
    page.goto("https://www.linkedin.com/games/mini-sudoku")  # replace with actual puzzle URL

    time.sleep(1)

    hidden_codes = page.query_selector_all("code[style='display: none']")
    json_str = None
    for code in hidden_codes:
        text = code.inner_text()
        if "presetCellIdxes" in text:  # unique marker for the puzzles
            json_str = text
            break

    if json_str is None:
        raise RuntimeError("Could not find sudoku JSON block")


    # Decode HTML entities
    decoded_json = html.unescape(json_str)

    # Parse into a Python dict
    data = json.loads(decoded_json)

    print(json.dumps(data, indent = 4))


    sudoku_game_puzzle = None
    for item in data.get("included", []):
        game_puzzle = item.get("gamePuzzle", {}).get("miniSudokuGamePuzzle")
        if game_puzzle:
            sudoku_game_puzzle = game_puzzle
            break

    browser.close()

solution = sudoku_game_puzzle.get("solution")

print(solution)