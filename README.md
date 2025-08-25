# Final Fantasy XIII Walkthrough Scraper (RAG Pipeline Version)

This directory contains tools for scraping and processing the Final Fantasy XIII walkthrough for use in a Retrieval Augmented Generation (RAG) pipeline.

## Branches

- `master`: Original version of the scraper
- `fix-scraper-issues`: Fixed version with improved parsing and regex patterns
- `context7-analysis`: Improved scraper with best practices from context7 analysis
- `rag-embedding-optimization`: Current branch - Optimized for RAG pipeline usage

## RAG Pipeline Tools

### ffxiii_rag_processor.py

This script processes the FF13 walkthrough markdown file and prepares it for use in a RAG pipeline:

1. **Semantic Chunking**: Respects the document structure while creating appropriately sized chunks
2. **Metadata Extraction**: Extracts section and subsection information for each chunk
3. **JSONL Output**: Saves chunks in JSONL format for easy ingestion into vector databases
4. **Statistics Generation**: Provides processing statistics for quality assurance

## Features

- Configurable chunk size and overlap
- Context-aware chunking that respects document structure
- Rich metadata extraction (section, subsection, titles)
- JSONL output format for vector database ingestion
- Processing statistics for quality assurance

## Usage

Run the RAG processor:
```
python ffxiii_rag_processor.py
```

The script will:
1. Read the `ffxiii_walkthrough.md` file
2. Process it into semantic chunks
3. Extract metadata for each chunk
4. Save the results to `rag_output/ffxiii_walkthrough_rag.jsonl`
5. Generate processing statistics in `rag_output/processing_stats.json`

## Output Format

Each line in the output JSONL file contains a chunk with the following structure:

```json
{
  "id": "ff13_chunk_0001",
  "content": "Chunk content...",
  "metadata": {
    "section": "A",
    "subsection": "A1",
    "section_title": "GENERAL INFORMATION",
    "subsection_title": "DISCLAIMERS",
    "chunk_index": 1
  },
  "embedding_text": "Section A | GENERAL INFORMATION | Subsection A1 | DISCLAIMERS\n\nChunk content...",
  "timestamp": "2025-08-25T00:00:00"
}
```

## Requirements

- Python 3.9+
- No additional dependencies beyond the base scraper requirements

## Integration with Vector Databases

The output JSONL file can be easily ingested into popular vector databases:

- **Pinecone**: Use the Pinecone Python client to upsert records
- **Weaviate**: Use the Weaviate Python client to batch import
- **Chroma**: Use Chroma's `add` method with the JSONL data
- **FAISS**: Convert the JSONL to the appropriate format for FAISS indexing

## Customization

You can customize the chunking behavior by modifying the constants in the script:

- `CHUNK_SIZE`: Target size for text chunks (default: 1000 characters)
- `CHUNK_OVERLAP`: Overlap between consecutive chunks (default: 200 characters)