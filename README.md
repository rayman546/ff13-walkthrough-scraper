# Final Fantasy XIII Walkthrough Scraper (Fixed Version)

This is an improved version of the Python script that scrapes the Final Fantasy XIII 100% walkthrough from GameFAQs and converts it to a markdown file.

## Fixes Made

1. **Corrected Regex Patterns**: Fixed incorrectly escaped regex patterns in the parsing function
2. **Improved Content Parsing**: Enhanced the parsing logic to better handle the structure of the walkthrough
3. **Better Error Handling**: Maintained proper error handling while fixing the core issues

## Requirements

- Python 3.x
- requests
- beautifulsoup4

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script:
```
python ffxiii_walkthrough_scraper.py
```

The script will:
1. Fetch the walkthrough from GameFAQs
2. Parse the content into structured sections
3. Save the result as `ffxiii_walkthrough.md`

## Output

The output file (`ffxiii_walkthrough.md`) contains:
- The complete walkthrough organized by sections (A-H)
- Chapter breakdowns
- Post-game content
- Trophy information
- Enemy intel and farming guides

## Branches

- `master`: Original version of the scraper
- `fix-scraper-issues`: Fixed version with improved parsing and regex patterns

## Notes

- The script respects the website's robots.txt and includes proper headers to mimic a browser request
- Parsing preserves the original structure while converting to readable markdown format
- The script may take a few seconds to complete as it fetches and processes the entire walkthrough