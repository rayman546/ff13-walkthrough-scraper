# Final Fantasy XIII Walkthrough Scraper

This repository contains a Python scraper for the Final Fantasy XIII 100% walkthrough from GameFAQs, with multiple versions showing different approaches and improvements.

## Branches

### `master`
The original version of the FF13 walkthrough scraper.

### `fix-scraper-issues`
Fixed version with corrected regex patterns and improved content parsing.

### `context7-analysis`
Improved scraper incorporating best practices from analyzing the requests and BeautifulSoup libraries:
- Better error handling with proper exception types
- Session management with connection pooling
- Retry strategy with exponential backoff
- Modular design with object-oriented approach
- Type hints for better documentation
- Comprehensive logging

### `rag-embedding-optimization` (default branch)
Optimized for Retrieval Augmented Generation (RAG) pipeline usage:
- Semantic chunking of the document
- Metadata extraction for each chunk
- JSONL output format for vector database ingestion
- Context-aware embedding preparation
- Processing statistics

## Features

- Scrapes the complete FF13 walkthrough from GameFAQs
- Converts content to structured markdown
- Processes content for RAG pipeline usage
- Extracts metadata for filtering and relevance scoring
- Outputs data in formats suitable for vector databases

## Requirements

- Python 3.9+
- requests
- beautifulsoup4
- urllib3

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Depending on which branch you're using:

```bash
# Original scraper
python ffxiii_walkthrough_scraper.py

# Improved scraper with best practices
python ffxiii_walkthrough_scraper_improved.py

# RAG processor
python ffxiii_rag_processor.py
```

## Output

The scrapers generate:
- `ffxiii_walkthrough.md` - Complete walkthrough in markdown format
- `rag_output/ffxiii_walkthrough_rag.jsonl` - Chunks prepared for RAG pipeline
- `rag_output/processing_stats.json` - Statistics about the chunking process

## License

This project is for educational purposes only. The scraped content is copyrighted by their respective owners.