from pathlib import Path
import os
import json

reddit_json_demo = Path(__file__).parent.parent / "data" / "reddit_json_demo" 
reddit_text_demo = Path(__file__).parent.parent / "data" / "reddit_text_demo"

def load_reddit_posts(folder_path):
    
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            json_path = os.path.join(folder_path, file)
            
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            title = data.get("title")
            post = data.get("post")
            full_post = f"{title}\n\n{post}"
            
            file_name = Path(file).stem
            new_file_name = file_name + ".txt"
            txt_path = os.path.join(reddit_text_demo, new_file_name)
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_post)
            
            print(f"Converted: {file} -> {new_file_name}")

load_reddit_posts(reddit_json_demo)