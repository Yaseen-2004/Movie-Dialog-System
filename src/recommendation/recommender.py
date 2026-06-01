import os
from collections import Counter
from search.search_engine import SearchEngine

MOVIE_META_PATH = "data/raw/movie_titles_metadata.txt"


class Recommender:
    def __init__(self):
        print("Initializing recommender...")
        self.search_engine = SearchEngine()
        self.movie_map = self.load_movie_metadata()

    def load_movie_metadata(self):
        movie_map = {}

        if not os.path.exists(MOVIE_META_PATH):
            print("⚠️ Movie metadata file not found!")
            return movie_map

        with open(MOVIE_META_PATH, 'r', encoding='iso-8859-1') as f:
            for line in f:
                parts = line.strip().split(" +++$+++ ")

                if len(parts) >= 2:
                    movie_id = parts[0]
                    title = parts[1]
                    movie_map[movie_id] = title

        print(f"Loaded {len(movie_map)} movie titles")
        return movie_map

    def recommend(self, query, top_k=20, top_n=5):
        results = self.search_engine.search(query, top_k=top_k)

        movie_scores = {}
        movie_dialogues = {}

        for r in results:
            mid = r["movie_id"]

            # Use similarity score (lower distance = better)
            score = 1 / (1 + r["score"])

            movie_scores[mid] = movie_scores.get(mid, 0) + score

            if mid not in movie_dialogues:
                movie_dialogues[mid] = []

            movie_dialogues[mid].append(r["text"])

        ranked = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

        recommendations = []

        for movie_id, score in ranked:
            title = self.movie_map.get(movie_id, movie_id)

            recommendations.append({
                "title": title,
                "score": round(score, 3),
                "samples": movie_dialogues[movie_id][:2]
            })

        return recommendations