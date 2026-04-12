from pathlib import Path


def load_txt_files(directory: str):
    documents = []

    for file_path in Path(directory).glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            documents.append({
                "content": text,
                "source": file_path.name
            })

    return documents


if __name__ == "__main__":
    docs = load_txt_files("data/raw")
    print(docs)