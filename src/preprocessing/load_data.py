import os

DATA_PATH = "data/raw/"

def load_lines():
    file_path = os.path.join(DATA_PATH, "movie_lines.txt")
    lines = {}

    with open(file_path, 'r', encoding='iso-8859-1') as f:
        for line in f:
            parts = line.split(" +++$+++ ")

            if len(parts) == 5:
                line_id = parts[0]
                movie_id = parts[2]
                text = parts[4].strip()

                lines[line_id] = {
                    "movie_id": movie_id,
                    "text": text
                }

    print(f"Loaded {len(lines)} lines")
    return lines


def load_conversations(lines):
    import ast

    file_path = os.path.join(DATA_PATH, "movie_conversations.txt")
    conversations = []

    with open(file_path, 'r', encoding='iso-8859-1') as f:
        for line in f:
            parts = line.split(" +++$+++ ")
            line_ids = ast.literal_eval(parts[-1])

            convo = []
            for lid in line_ids:
                if lid in lines:
                    convo.append(lines[lid]["text"])

            if convo:
                conversations.append({
                    "movie_id": lines[line_ids[0]]["movie_id"],
                    "dialogue": " ".join(convo)
                })

    print(f"Built {len(conversations)} conversations")
    return conversations


if __name__ == "__main__":
    lines = load_lines()
    conversations = load_conversations(lines)