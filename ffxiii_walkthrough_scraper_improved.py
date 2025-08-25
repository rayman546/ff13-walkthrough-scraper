"""
Final Fantasy XIII Walkthrough Scraper

This script scrapes the Final Fantasy XIII 100% walkthrough from GameFAQs 
and converts it to a structured markdown file.

Best practices implemented:
- Proper error handling with specific exceptions
- Session management for connection pooling
- Configurable headers and timeouts
- Modular code structure
- Type hints for better code documentation
- Comprehensive logging
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import re
import logging
from typing import Optional, List, Tuple
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
DEFAULT_TIMEOUT = 30
OUTPUT_FILE = "ffxiii_walkthrough.md"

# Content selectors to try
CONTENT_SELECTORS = [
    'div.faq-content',
    'div.faqtext',
    '#faqwrap',
    '.guide_content',
    '.page-content',
    '#content',
    'main',
    'div[class*="content"]'
]


class WalkthroughScraper:
    """A scraper for GameFAQs walkthroughs."""
    
    def __init__(self, headers: dict = None, timeout: int = None):
        """
        Initialize the scraper.
        
        Args:
            headers: HTTP headers to use for requests
            timeout: Request timeout in seconds
        """
        self.headers = headers or DEFAULT_HEADERS
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry strategy.
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def fetch_content(self, url: str) -> tuple:
        """
        Fetch and parse webpage content.
        
        Args:
            url: URL to fetch
            
        Returns:
            Tuple of (BeautifulSoup object, content div)
            
        Raises:
            requests.RequestException: If the request fails
            ValueError: If content cannot be found
        """
        logger.info(f"Fetching webpage: {url}")
        
        try:
            response = self.session.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch webpage: {e}")
            raise
        
        logger.info("Parsing content...")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find content using various selectors
        content_div = None
        for selector in CONTENT_SELECTORS:
            content_div = soup.select_one(selector)
            if content_div:
                logger.info(f"Found content using selector: {selector}")
                break
        
        if not content_div:
            # If we still can't find it, let's see what divs are available
            divs = soup.find_all('div')
            logger.info("Available div classes:")
            for div in divs[:10]:  # Show first 10 divs
                if div.get('class'):
                    logger.info(f"  - {div.get('class')}")
            
            raise ValueError("Could not find walkthrough content on the page")
        
        return soup, content_div
    
    def parse_walkthrough_content(self, content_div: BeautifulSoup) -> str:
        """
        Parse the walkthrough content into structured markdown.
        
        Args:
            content_div: BeautifulSoup object containing the content
            
        Returns:
            Formatted markdown string
        """
        logger.info("Parsing walkthrough content...")
        
        # Extract the text content
        content_text = content_div.get_text()
        
        # Split content into lines
        lines = content_text.splitlines()
        
        # Remove empty lines
        lines = [line for line in lines if line.strip()]
        
        # Initialize markdown content
        markdown = []
        markdown.append("# Final Fantasy XIII 100% Walkthrough\n")
        markdown.append("\n")
        
        # Process lines
        in_section = False
        
        for line in lines:
            line = line.strip()
            
            # Check for main sections (SECTION A, SECTION B, etc.)
            section_match = re.match(r'^SECTION\s+([A-H]):?\s*(.*)$', line, re.IGNORECASE)
            if section_match:
                # Close previous section if exists
                if in_section:
                    markdown.append("\n---\n\n")
                
                section_letter = section_match.group(1).upper()
                section_title = section_match.group(2).strip()
                markdown.append(f"## Section {section_letter}: {section_title}\n\n")
                in_section = True
                continue
                
            # Check for subsections (B1, B2, etc.)
            subsection_match = re.match(r'^([A-Z]\d+):?\s*(.*)$', line)
            if subsection_match and in_section:
                subsection_id = subsection_match.group(1)
                subsection_title = subsection_match.group(2).strip()
                markdown.append(f"### {subsection_id}: {subsection_title}\n\n")
                continue
                
            # Check for numbered items (1., 2., 3., etc.)
            numbered_match = re.match(r'^(\d+)\.\s+(.*)$', line)
            if numbered_match:
                number = numbered_match.group(1)
                text = numbered_match.group(2).strip()
                markdown.append(f"{number}. {text}\n")
                continue
                
            # Check for bullet points
            bullet_match = re.match(r'^[*\-]\s+(.*)$', line)
            if bullet_match:
                text = bullet_match.group(1).strip()
                markdown.append(f"- {text}\n")
                continue
                
            # Add regular paragraph
            if line:
                # If line looks like a header (all caps), make it a markdown header
                if line.isupper() and len(line.split()) <= 6:
                    markdown.append(f"### {line.title()}\n\n")
                else:
                    markdown.append(f"{line}\n\n")
        
        return ''.join(markdown)
    
    def scrape(self, url: str) -> str:
        """
        Scrape a walkthrough from the given URL.
        
        Args:
            url: URL to scrape
            
        Returns:
            Formatted markdown content
        """
        soup, content_div = self.fetch_content(url)
        return self.parse_walkthrough_content(content_div)
    
    def save_to_file(self, content: str, filename: str = None) -> Path:
        """
        Save content to a file.
        
        Args:
            content: Content to save
            filename: Output filename (defaults to OUTPUT_FILE)
            
        Returns:
            Path to the saved file
        """
        filename = filename or OUTPUT_FILE
        filepath = Path(filename)
        
        logger.info(f"Saving walkthrough to {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath


def main():
    """Main entry point."""
    url = "https://gamefaqs.gamespot.com/ps3/928790-final-fantasy-xiii/faqs/69497"
    
    # Create scraper instance
    scraper = WalkthroughScraper()
    
    try:
        logger.info("Starting walkthrough scraping...")
        markdown_content = scraper.scrape(url)
        filepath = scraper.save_to_file(markdown_content)
        logger.info(f"Walkthrough successfully saved to {filepath}")
        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise


if __name__ == "__main__":
    main()