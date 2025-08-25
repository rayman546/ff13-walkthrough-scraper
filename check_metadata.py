import json

# Read the first 100 chunks and check their metadata
with open('rag_output/ffxiii_walkthrough_rag.jsonl', 'r', encoding='utf-8') as f:
    for i in range(100):
        line = f.readline()
        if not line:
            break
        data = json.loads(line)
        metadata = data['metadata']
        if metadata['section']:
            print(f"Chunk {i} metadata: {metadata}")
            print(f"Content preview: {data['content'][:200]}...")
            break
    else:
        print("No chunks with section metadata found in first 100 chunks")