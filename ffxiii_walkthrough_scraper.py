import requests
from bs4 import BeautifulSoup
import re


def scrape_walkthrough(url):
    """
    Scrape the Final Fantasy XIII walkthrough from GameFAQs and convert to markdown
    """
    print("Fetching webpage...")
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    print("Parsing content...")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Try different selectors to find the walkthrough content
    selectors_to_try = [
        'div.faq-content',
        'div.faqtext',
        '#faqwrap',
        '.guide_content',
        '.page-content',
        '#content',
        'main',
        'div[class*="content"]'
    ]
    
    content_div = None
    for selector in selectors_to_try:
        content_div = soup.select_one(selector)
        if content_div:
            print(f"Found content using selector: {selector}")
            break
    
    if not content_div:
        # If we still can't find it, let's see what divs are available
        divs = soup.find_all('div')
        print("Available div classes:")
        for div in divs[:10]:  # Show first 10 divs
            if div.get('class'):
                print(f"  - {div.get('class')}")
        
        raise Exception("Could not find walkthrough content on the page")
    
    # Extract the text content
    content_text = content_div.get_text()
    
    # Parse the content into sections
    markdown_content = parse_walkthrough_content(content_text)
    
    return markdown_content


def parse_walkthrough_content(content):
    """
    Parse the walkthrough content into structured markdown
    """
    # Split content into lines
    lines = content.splitlines()
    
    # Remove empty lines
    lines = [line for line in lines if line.strip()]
    
    # Initialize markdown content
    markdown = []
    markdown.append("# Final Fantasy XIII 100% Walkthrough\n")
    markdown.append("\n")
    
    # Process lines
    in_section = False
    current_section = ""
    
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
            current_section = section_letter
            continue
            
        # Check for subsections (B1, B2, etc.)
        subsection_match = re.match(r'^([A-Z]\\d+):?\s*(.*)$', line)
        if subsection_match and in_section:
            subsection_id = subsection_match.group(1)
            subsection_title = subsection_match.group(2).strip()
            markdown.append(f"### {subsection_id}: {subsection_title}\n\n")
            continue
            
        # Check for numbered items (1., 2., 3., etc.)
        numbered_match = re.match(r'^(\\d+)\\.\\s+(.*)$', line)
        if numbered_match:
            number = numbered_match.group(1)
            text = numbered_match.group(2).strip()
            markdown.append(f"{number}. {text}\n")
            continue
            
        # Check for bullet points
        bullet_match = re.match(r'^[*\\-]\\s+(.*)$', line)
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


def main():
    url = "https://gamefaqs.gamespot.com/ps3/928790-final-fantasy-xiii/faqs/69497"
    
    try:
        print("Starting walkthrough scraping...")
        markdown_content = scrape_walkthrough(url)
        
        # Save to file
        output_file = "ffxiii_walkthrough.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        print(f"Walkthrough successfully saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()