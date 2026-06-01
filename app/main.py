import sys
import os

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.recommendation.recommender import Recommender


def main():
    print("🎬 Dialogue-Based Movie Recommender")
    print("Type 'exit' to quit\n")

    recommender = Recommender()

    while True:
        query = input("\nEnter your query: ")

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query.strip():
            print("⚠️ Please enter a valid query")
            continue

        print("\nSearching...\n")

       
        results = recommender.recommend(query)

        print(" Recommended Movies:\n")

        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['title']} (score: {r['score']})")

            print("   Sample dialogues:")
            for d in r["samples"]:
                print(f"   - {d[:120]}...")


if __name__ == "__main__":
    main()