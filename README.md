git # LinkedIn Games Bot

An automated bot that solves LinkedIn's daily puzzle games using Playwright browser automation.

## Features

Automatically solves all 6 LinkedIn games:

- Mini Sudoku
- Tango
- Queens
- Zip
- Pinpoint
- CrossClimb

## Requirements

- Python 3.7+
- Microsoft Edge browser
- Playwright

## Installation

1. Clone this repository
2. Install Playwright:

```bash
pip install playwright
```

## Usage

**Basic usage (uses "Profile 1" by default):**

```bash
python main.py
```

**With custom Edge profile:**

```bash
python main.py --profile "Default"
python main.py --profile "Profile 2"
```

## How It Works

The bot:

1. Launches Microsoft Edge with your existing profile (maintains LinkedIn login)
2. Opens all game pages in separate tabs
3. Extracts puzzle solutions from hidden JSON data in the page
4. Automatically fills in answers using DOM manipulation
5. Keeps the browser open for you to view results

## Important Notes

- **Microsoft Edge must be closed** before running the bot (Playwright needs exclusive access to the profile)
- The bot uses your Edge profile to maintain your LinkedIn login session
- Each game is checked for completion - already solved puzzles are skipped

## Project Structure

```
linkedin/
├── main.py              # Main script - orchestrates all games
├── helpers.py           # Helper functions for JSON extraction
├── games/              # Individual game solvers
│   ├── minisudoku.py
│   ├── tango.py
│   ├── queens.py
│   ├── zip.py
│   ├── pinpoint.py
│   └── crossClimb.py
└── CLAUDE.md           # Detailed technical documentation
```

## Troubleshooting

**Profile issues:**

- Find your Edge profile name by going to `edge://version/` and looking at the "Profile Path"
- Common profile names: "Profile 1", "Profile 2", "Default"

**Edge won't launch:**

- Make sure all Edge windows are closed
- Check Task Manager for lingering Edge processes

## License

MIT
