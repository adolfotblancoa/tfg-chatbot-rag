from pathlib import Path
from pypdf import PdfReader


def load_txt_file(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return {
        "content": text,
        "source": file_path.name,
        "type": "txt"
    }


def load_pdf_file(file_path: Path) -> dict:
    reader = PdfReader(str(file_path))
    pages_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        if page_text.strip():
            pages_text.append(page_text)

    full_text = "\n".join(pages_text)

    return {
        "content": full_text,
        "source": file_path.name,
        "type": "pdf"
    }


def load_documents(directory: str):
    documents = []
    path = Path(directory)

    for file_path in path.glob("*"):
        if file_path.suffix.lower() == ".txt":
            documents.append(load_txt_file(file_path))
        elif file_path.suffix.lower() == ".pdf":
            documents.append(load_pdf_file(file_path))

    return documents


if __name__ == "__main__":
    docs = load_documents("data/raw")
    for doc in docs:
        print(f"{doc['source']} ({doc['type']}) -> {len(doc['content'])} caracteres")