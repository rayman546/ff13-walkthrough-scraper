"""
FF13 Walkthrough Scraper for RAG Pipeline

This script scrapes the FF13 walkthrough and prepares it for use in a Retrieval Augmented Generation (RAG) pipeline.
It chunks the content appropriately and extracts metadata for each chunk to optimize retrieval.

Key features for RAG:
- Semantic chunking based on content structure
- Metadata extraction for filtering and relevance scoring
- JSON output format for easy ingestion into vector databases
- Configurable chunk sizes and overlap
"""

import json
import re
import logging
from typing import List, Dict, Any, Generator
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
OUTPUT_DIR = Path("rag_output")
CHUNK_SIZE = 1000  # Target chunk size in characters
CHUNK_OVERLAP = 200  # Overlap between chunks in characters
MARKDOWN_FILE = "ffxiii_walkthrough.md"
OUTPUT_FILE = "ffxiii_walkthrough_rag.jsonl"


@dataclass
class RAGChunk:
    """Data class for a chunk of text prepared for RAG pipeline."""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding_text: str  # Text to be embedded (may differ from content)
    timestamp: str


class FF13RAGProcessor:
    """Processor for converting FF13 walkthrough into RAG-optimized chunks."""
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        """
        Initialize the RAG processor.
        
        Args:
            chunk_size: Target size for text chunks
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.section_pattern = re.compile(r'^## Section ([A-H]):\s*(.*)$')
        self.subsection_pattern = re.compile(r'^### ([A-Z]\d+):\s*(.*)$')
        self.separator_pattern = re.compile(r'^---+$')
        
    def read_markdown_file(self, filepath: str) -> List[str]:
        """
        Read the markdown file and return lines.
        
        Args:
            filepath: Path to the markdown file
            
        Returns:
            List of lines from the file
        """
        logger.info(f"Reading markdown file: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        logger.info(f"Read {len(lines)} lines from file")
        return lines
    
    def extract_metadata(self, lines: List[str], start_idx: int) -> Dict[str, Any]:
        """
        Extract metadata from lines around the chunk.
        
        Args:
            lines: All lines from the document
            start_idx: Starting index of the chunk
            
        Returns:
            Dictionary of metadata
        """
        metadata = {
            "section": None,
            "subsection": None,
            "section_title": None,
            "subsection_title": None,
            "chunk_index": start_idx
        }
        
        # Look backwards to find the most recent section and subsection
        for i in range(start_idx, -1, -1):
            line = lines[i].strip()
            
            # Check for section
            section_match = self.section_pattern.match(line)
            if section_match:
                metadata["section"] = section_match.group(1)
                metadata["section_title"] = section_match.group(2)
                break
                
            # Check for subsection
            subsection_match = self.subsection_pattern.match(line)
            if subsection_match and metadata["subsection"] is None:
                metadata["subsection"] = subsection_match.group(1)
                metadata["subsection_title"] = subsection_match.group(2)
        
        return metadata
    
    def semantic_chunking(self, lines: List[str]) -> Generator[RAGChunk, None, None]:
        """
        Perform semantic chunking of the document.
        
        This approach respects the document structure while creating chunks
        of appropriate size for embedding.
        
        Args:
            lines: List of lines from the document
            
        Yields:
            RAGChunk objects
        """
        logger.info("Starting semantic chunking")
        
        content_buffer = []
        chunk_index = 0
        char_count = 0
        start_line_idx = 0
        
        i = 0
        while i < len(lines):
            line = lines[i]
            line_length = len(line)
            
            # Check if adding this line would exceed chunk size
            if char_count + line_length > self.chunk_size and content_buffer:
                # Create a chunk
                content = ''.join(content_buffer).strip()
                
                # Extract metadata
                metadata = self.extract_metadata(lines, start_line_idx)
                metadata["chunk_index"] = chunk_index
                
                # Create embedding text (could be different from content for optimization)
                embedding_text = self.prepare_embedding_text(content, metadata)
                
                chunk = RAGChunk(
                    id=f"ff13_chunk_{chunk_index:04d}",
                    content=content,
                    metadata=metadata,
                    embedding_text=embedding_text,
                    timestamp=datetime.now().isoformat()
                )
                
                yield chunk
                
                # Reset for next chunk with overlap
                chunk_index += 1
                
                # Calculate overlap - go back to find appropriate overlap point
                overlap_chars = 0
                overlap_buffer = []
                j = len(content_buffer) - 1
                
                while overlap_chars < self.chunk_overlap and j >= 0:
                    overlap_line = content_buffer[j]
                    overlap_buffer.insert(0, overlap_line)
                    overlap_chars += len(overlap_line)
                    j -= 1
                
                content_buffer = overlap_buffer
                char_count = overlap_chars
                start_line_idx = i - len(overlap_buffer)
            else:
                # Add line to buffer
                content_buffer.append(line)
                char_count += line_length
                i += 1
        
        # Handle remaining content
        if content_buffer:
            content = ''.join(content_buffer).strip()
            metadata = self.extract_metadata(lines, start_line_idx)
            metadata["chunk_index"] = chunk_index
            
            embedding_text = self.prepare_embedding_text(content, metadata)
            
            chunk = RAGChunk(
                id=f"ff13_chunk_{chunk_index:04d}",
                content=content,
                metadata=metadata,
                embedding_text=embedding_text,
                timestamp=datetime.now().isoformat()
            )
            
            yield chunk
    
    def prepare_embedding_text(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Prepare text for embedding by adding context.
        
        Args:
            content: The chunk content
            metadata: Metadata for the chunk
            
        Returns:
            Text optimized for embedding
        """
        # Add contextual information to help with embedding
        context_parts = []
        
        if metadata.get("section"):
            context_parts.append(f"Section {metadata['section']}")
            if metadata.get("section_title"):
                context_parts.append(metadata['section_title'])
        
        if metadata.get("subsection"):
            context_parts.append(f"Subsection {metadata['subsection']}")
            if metadata.get("subsection_title"):
                context_parts.append(metadata['subsection_title'])
        
        context_header = " | ".join(context_parts)
        
        # Combine context with content
        if context_header:
            return f"{context_header}\n\n{content}"
        else:
            return content
    
    def process_document(self, filepath: str) -> List[RAGChunk]:
        """
        Process the entire document into RAG chunks.
        
        Args:
            filepath: Path to the markdown file
            
        Returns:
            List of RAGChunk objects
        """
        logger.info(f"Processing document: {filepath}")
        
        # Read the file
        lines = self.read_markdown_file(filepath)
        
        # Perform chunking
        chunks = list(self.semantic_chunking(lines))
        
        logger.info(f"Created {len(chunks)} chunks from document")
        return chunks
    
    def save_chunks(self, chunks: List[RAGChunk], output_dir: Path = None) -> Path:
        """
        Save chunks to JSONL file.
        
        Args:
            chunks: List of RAGChunk objects
            output_dir: Directory to save files (defaults to OUTPUT_DIR)
            
        Returns:
            Path to the saved file
        """
        output_dir = output_dir or OUTPUT_DIR
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / OUTPUT_FILE
        logger.info(f"Saving {len(chunks)} chunks to {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(json.dumps(asdict(chunk), ensure_ascii=False) + '\n')
        
        logger.info(f"Chunks saved successfully")
        return output_file
    
    def generate_statistics(self, chunks: List[RAGChunk]) -> Dict[str, Any]:
        """
        Generate statistics about the chunking process.
        
        Args:
            chunks: List of RAGChunk objects
            
        Returns:
            Dictionary of statistics
        """
        if not chunks:
            return {}
        
        content_lengths = [len(chunk.content) for chunk in chunks]
        embedding_lengths = [len(chunk.embedding_text) for chunk in chunks]
        
        stats = {
            "total_chunks": len(chunks),
            "avg_content_length": sum(content_lengths) / len(content_lengths),
            "min_content_length": min(content_lengths),
            "max_content_length": max(content_lengths),
            "avg_embedding_length": sum(embedding_lengths) / len(embedding_lengths),
            "min_embedding_length": min(embedding_lengths),
            "max_embedding_length": max(embedding_lengths),
            "sections": list(set(chunk.metadata.get("section") for chunk in chunks if chunk.metadata.get("section"))),
            "processing_timestamp": datetime.now().isoformat()
        }
        
        return stats


def main():
    """Main entry point for RAG processing."""
    logger.info("Starting FF13 walkthrough RAG processing")
    
    # Initialize processor
    processor = FF13RAGProcessor()
    
    try:
        # Process the document
        chunks = processor.process_document(MARKDOWN_FILE)
        
        # Generate and save statistics
        stats = processor.generate_statistics(chunks)
        logger.info(f"Processing statistics: {stats}")
        
        # Save chunks
        output_file = processor.save_chunks(chunks)
        
        # Save statistics
        stats_file = OUTPUT_DIR / "processing_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"RAG processing completed successfully. Output saved to {output_file}")
        logger.info(f"Statistics saved to {stats_file}")
        
    except Exception as e:
        logger.error(f"Error during RAG processing: {e}")
        raise


if __name__ == "__main__":
    main()