from pathlib import Path
from pypdf import PdfReader


def load_txt_file(file_path: Path) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return [{
        "content": text,
        "source": file_path.name,
        "type": "txt",
        "page": 1
    }]


def load_pdf_file(file_path: Path) -> list[dict]:
    reader = PdfReader(str(file_path))
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""

        if page_text.strip():
            documents.append({
                "content": page_text,
                "source": file_path.name,
                "type": "pdf",
                "page": page_number
            })

    return documents


def load_documents(directory: str) -> list[dict]:
    documents = []
    path = Path(directory)

    for file_path in path.glob("*"):
        if file_path.suffix.lower() == ".txt":
            documents.extend(load_txt_file(file_path))
        elif file_path.suffix.lower() == ".pdf":
            documents.extend(load_pdf_file(file_path))

    return documents


if __name__ == "__main__":
    docs = load_documents("data/raw")
    for doc in docs[:10]:
        print(
            f"{doc['source']} | tipo={doc['type']} | página={doc['page']} | "
            f"caracteres={len(doc['content'])}"
        )