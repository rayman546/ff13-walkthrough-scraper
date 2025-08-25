# Final Fantasy XIII Walkthrough Scraper (Context7 Improved Version)

This Python script scrapes the Final Fantasy XIII 100% walkthrough from GameFAQs and converts it to a markdown file.

## Improvements from Context7 Analysis

This version incorporates best practices from analyzing the requests and BeautifulSoup libraries:

1. **Better Error Handling**: Proper exception handling with specific error types
2. **Session Management**: Uses requests Session with connection pooling for better performance
3. **Retry Strategy**: Implements exponential backoff for failed requests
4. **Modular Design**: Object-oriented approach with clear separation of concerns
5. **Type Hints**: Added type annotations for better code documentation
6. **Logging**: Comprehensive logging instead of print statements
7. **Configuration**: Easily configurable headers and timeouts
8. **Resource Management**: Proper file handling with context managers

## Requirements

- Python 3.9+
- requests
- beautifulsoup4
- urllib3

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the improved script:
```
python ffxiii_walkthrough_scraper_improved.py
```

The script will:
1. Fetch the walkthrough from GameFAQs
2. Parse the content into structured sections
3. Save the result as `ffxiii_walkthrough.md`

## Files

- `ffxiii_walkthrough_scraper_improved.py`: Main scraper script with improvements
- `ffxiii_walkthrough_scraper.py`: Original scraper script
- `requirements.txt`: Python dependencies
- `README.md`: This file

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