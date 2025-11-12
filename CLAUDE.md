# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LinkedIn Games automation bot that uses Playwright to automatically solve LinkedIn's daily puzzle games. The bot opens multiple game pages in Microsoft Edge using a persistent browser context (to maintain login state) and automatically solves each puzzle by extracting solutions from the page's JSON data and interacting with the DOM.

## Running the Bot

**Basic usage (uses "Profile 1" by default):**
```bash
python main.py
```

**With custom profile:**
```bash
python main.py --profile "Default"
python main.py --profile "Profile 2"
```

**Get help:**
```bash
python main.py --help
```

**REQUIREMENTS FOR RUNNING:**
- Microsoft Edge must NOT be open on the machine (Playwright needs exclusive access to the profile)

**What it does:**
1. Launches Microsoft Edge with your specified profile (auto-detects user directory)
2. Opens all 6 LinkedIn game URLs in separate tabs
3. Solves each puzzle automatically
4. Keeps the browser open until you press Enter

## Architecture

### Main Entry Point ([main.py](main.py))

The main script orchestrates the entire automation process:

- Uses Playwright with a **persistent browser context** pointing to Edge's user data directory (maintains login sessions)
- Defines two parallel data structures:
  - `PUZZLES`: Maps puzzle type names to their LinkedIn URLs
  - `PUZZLE_FILLERS`: Maps puzzle type names to their solver functions
- Opens each game URL in a new page and dispatches to the appropriate solver

### Core Helper Functions ([helpers.py](helpers.py))

- `get_full_json(page, marker)`: Extracts hidden JSON data from `<code style='display: none'>` elements containing puzzle data
- `parse_active_puzzle(decoded_json)`: Parses the JSON response to find the first non-null puzzle data (handles LinkedIn's multi-puzzle response format)
- `get_solution_zip(page)`: Special case for Zip game - uses regex to extract solution array from raw HTML (Zip doesn't use the standard JSON format)
- `is_puzzle_completed(page)`: Checks if "See results" button exists to avoid re-solving already completed puzzles

### Game Solvers (games/)

Each game has its own solver module that implements a `fill_*` function. All solvers:

1. Check if puzzle is already completed (via `is_puzzle_completed()`)
2. Extract necessary data from the puzzle JSON
3. Use Playwright to interact with the DOM via `data-cell-idx` attributes

**Game-specific implementations:**

- **minisudoku.py**: Types numbers into cells, skipping preset cells
- **zip.py**: Clicks cells in solution order (path-finding puzzle)
- **tango.py**: Uses left-click for "ONE", right-click for "ZERO" values
- **queens.py**: Double-clicks cells to place queens (converts row/col to linear index using `gridSize`)
- **pinpoint.py**: Simply types the first solution and presses Enter (word puzzle)
- **crossClimb.py**: Most complex - types all words, then uses slow drag-and-drop operations to reorder rungs to match `solutionRungIndex` (uses bottom-up placement strategy)

### Key Patterns

**Data extraction flow:**

```
Page DOM → get_full_json() → parse_active_puzzle() → puzzle data dict → game solver
```

**Special case (Zip):**

```
Page HTML → get_solution_zip() (regex) → solution array → fill_zip()
```

**Cell interaction:**
All games use `data-cell-idx` attributes to locate DOM elements. Index calculation varies by game:

- Linear games (Sudoku, Tango): Direct index from solution array
- Grid games (Queens): `idx = row * gridSize + col`
- Sequence games (Zip): Solution is ordered array of indices

## Browser Configuration

The bot automatically detects the current user and uses Microsoft Edge's persistent context:

```python
username = getpass.getuser()  # Auto-detects current Windows user
user_data_dir=rf"C:\Users\{username}\AppData\Local\Microsoft\Edge\User Data"
profile="Profile 1"  # Default Edge profile
headless=False  # Visible browser for monitoring
no_viewport=True  # Uses full window size
```

**To use a different profile:** Use the `--profile` command-line argument (common values: "Profile 1", "Profile 2", "Default")

## Dependencies

- `playwright`: Browser automation
- `time`: Delays for page loading and drag operations
- Standard library: `html`, `json`, `re`

Install Playwright:

```bash
pip install playwright
playwright install chromium
```

## Common Modifications

**Adding a new game:**

1. Add URL to `PUZZLES` dict in [main.py](main.py)
2. Create new solver in `games/` following the pattern: `fill_gamename(page, puzzle)`
3. Add solver to `PUZZLE_FILLERS` dict
4. Implement puzzle-specific logic using `data-cell-idx` selectors

**Adjusting timing:**

- Modify `time.sleep()` values in [main.py](main.py) for page load delays
- Adjust `pause_after_move` in [crossClimb.py](games/crossClimb.py) for drag-and-drop speed
- Change `steps` variable in crossClimb for smoother/faster drag animations
