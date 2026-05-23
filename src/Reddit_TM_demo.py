from pathlib import Path
from bertopic import BERTopic
import os

reddit_text_files = Path(__file__).parent.parent / "data" / "reddit_text_demo" 

def load_reddit_posts(folder_path):
    posts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                posts.append(f.read())

    print(f"Loaded documents: {len(posts)}")
    print(f"Empty documents: {sum(1 for p in posts if not p.strip())}")
    return posts

posts = load_reddit_posts(reddit_text_files)

model = BERTopic(umap_model=None)
topics, probabilities = model.fit_transform(posts)

print("Number of topics:", len(set(topics)))
print(model.get_topic_info())

# model.get_topic_freq().head()

print(f"Topic words -1 (outliers/noise): {model.get_topic(-1)}")
