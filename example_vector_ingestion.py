"""
Example script showing how to use the RAG-processed FF13 walkthrough data
with a vector database or embedding model.

This script demonstrates:
1. Loading the processed chunks
2. Preparing data for embedding
3. Example of how to structure for vector database ingestion
"""

import json
from typing import List, Dict, Any
from pathlib import Path

def load_rag_chunks(filepath: str) -> List[Dict[str, Any]]:
    """
    Load RAG chunks from JSONL file.
    
    Args:
        filepath: Path to the JSONL file
        
    Returns:
        List of chunk dictionaries
    """
    chunks = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks

def prepare_for_embedding(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prepare chunks for embedding by extracting the text to embed.
    
    Args:
        chunks: List of chunk dictionaries
        
    Returns:
        List of dictionaries with id and text for embedding
    """
    embedding_data = []
    for chunk in chunks:
        embedding_data.append({
            "id": chunk["id"],
            "text": chunk["embedding_text"],
            "metadata": chunk["metadata"]
        })
    return embedding_data

def example_vector_database_ingestion(chunks: List[Dict[str, Any]]):
    """
    Example of how to ingest chunks into a vector database.
    
    This is a mock example - in practice you would use a real vector database client.
    """
    print("Example vector database ingestion:")
    print(f"Total chunks to ingest: {len(chunks)}")
    
    # Example of first few chunks
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i+1}:")
        print(f"  ID: {chunk['id']}")
        print(f"  Text length: {len(chunk['text'])} characters")
        print(f"  Section: {chunk['metadata'].get('section', 'N/A')}")
        print(f"  Subsection: {chunk['metadata'].get('subsection', 'N/A')}")
        print(f"  Preview: {chunk['text'][:100]}...")

def main():
    """Main example function."""
    # Load the processed chunks
    chunks_file = Path("rag_output") / "ffxiii_walkthrough_rag.jsonl"
    chunks = load_rag_chunks(str(chunks_file))
    
    print(f"Loaded {len(chunks)} chunks from {chunks_file}")
    
    # Prepare for embedding
    embedding_data = prepare_for_embedding(chunks)
    
    # Example ingestion
    example_vector_database_ingestion(embedding_data)
    
    print("\nTo use with a real vector database, you would:")
    print("1. Generate embeddings for each chunk's text")
    print("2. Store the embeddings with the chunk ID and metadata")
    print("3. Use similarity search to retrieve relevant chunks for queries")

if __name__ == "__main__":
    main()