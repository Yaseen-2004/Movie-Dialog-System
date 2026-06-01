import json

INPUT_PATH = "data/processed/conversations.json"
OUTPUT_PATH = "data/processed/chunks.json"


def chunk_text(text, chunk_size=3):
    sentences = text.split(".")
    chunks = []

    for i in range(0, len(sentences), chunk_size):
        chunk = ".".join(sentences[i:i+chunk_size]).strip()

        if len(chunk.split()) > 5: 
            chunks.append(chunk)

    return chunks


def process_chunks():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    all_chunks = []

    for convo in conversations:
        chunks = chunk_text(convo["dialogue"])

        for chunk in chunks:
            all_chunks.append({
                "movie_id": convo["movie_id"],
                "text": chunk
            })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f)

    print(f"Generated {len(all_chunks)} chunks")


if __name__ == "__main__":
    process_chunks()