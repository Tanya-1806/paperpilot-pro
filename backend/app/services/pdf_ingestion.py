import fitz

from app.services.chunking import chunk_text


def extract_pdf_chunks(pdf_bytes: bytes) -> tuple[int, list[dict]]:
    """Extract page-aware chunks from a PDF held in memory."""
    chunks = []

    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        if document.needs_pass:
            raise ValueError("Password-protected PDFs are not supported")

        page_count = len(document)

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            for chunk_index_on_page, content in enumerate(chunk_text(text)):
                chunks.append(
                    {
                        "page_number": page_number,
                        "content": content,
                        "chunk_index_on_page": chunk_index_on_page,
                    }
                )

    if not chunks:
        raise ValueError(
            "No extractable text found. Scanned PDFs require OCR, "
            "which is not supported yet."
        )

    return page_count, chunks
