# Final Fantasy XIII Walkthrough Scraper

This Python script scrapes the Final Fantasy XIII 100% walkthrough from GameFAQs and converts it to a markdown file.

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

## Notes

- The script respects the website's robots.txt and includes proper headers to mimic a browser request
- Parsing preserves the original structure while converting to readable markdown format
- The script may take a few seconds to complete as it fetches and processes the entire walkthrough