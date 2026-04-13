def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    text = clean_text(text)

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]

        if end < text_length:
            last_break = max(
                chunk.rfind("\n"),
                chunk.rfind(". "),
                chunk.rfind("; "),
                chunk.rfind(", ")
            )
            if last_break > chunk_size // 2:
                chunk = chunk[:last_break + 1]
                end = start + len(chunk)

        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = max(end - overlap, 0)

    return chunks