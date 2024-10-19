import os
from langlink_SQL import upload_SQL , delete_all_file
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-distilroberta-base-v1')

def read_all_file(file_path: str):
    texts = []
    paths = []
    try:
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            texts.append(f.read())
                            paths.append(path)
                    except Exception as e:
                        print(f"無法讀取檔案 {path}: {e}")
    except Exception as e:
        print(f"在讀取目錄時發生錯誤: {e}")
    return texts, paths

def read_file(file_path: str):
    try:
        if file_path.endswith('.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                print(f"無法讀取檔案 {file_path}: {e}")
    except Exception as e:
        print(f"在讀取檔案時發生錯誤: {e}")

texts, paths = read_all_file(r"G:\我的雲端硬碟\主資料庫")
embeddings = model.encode(texts)
names = [os.path.basename(path) for path in paths]

upload_SQL(names, embeddings, paths)

