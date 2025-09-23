import html
import json
import re

def get_full_json(page, marker="presetCellIdxes"):
    hidden_codes = page.query_selector_all("code[style='display: none']")
    for code in hidden_codes:
        text = code.inner_text()
        if marker in text:
            return html.unescape(text)
    return None


def parse_active_puzzle(decoded_json):
    """
    Returns the type and data of the first non-null puzzle in the response.
    """
    data = json.loads(decoded_json)

    for item in data.get("included", []):
        game_puzzle = item.get("gamePuzzle", {})
        if not game_puzzle:
            continue
        
        # Find the first non-null puzzle
        for puzzle_type, puzzle_data in game_puzzle.items():
            if puzzle_data:
                return puzzle_data

    return None

def get_solution_zip(page):
    
    html_content = page.content()  # get full DOM as string
    match = re.search(r'\\"solution\\":\s*(\[[^\]]*\])', html_content)
    if match:
        solution = json.loads(match.group(1))  # converts string "[22,21,..]" to Python list
        return solution
    else:
        print("Could not find solution array")