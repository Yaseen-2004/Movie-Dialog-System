import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.preprocessing.load_data import load_lines, load_conversations

OUTPUT_PATH = "data/processed/conversations.json"


def save_conversations(conversations):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(conversations, f)

    print(f"Saved {len(conversations)} conversations to {OUTPUT_PATH}")


if __name__ == "__main__":
    print("Loading data...")
    lines = load_lines()
    conversations = load_conversations(lines)

    print("Saving...")
    save_conversations(conversations)