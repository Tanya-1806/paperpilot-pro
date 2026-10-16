from sqlalchemy import select

from app.models.document import Document, DocumentChunk


def test_upload_pdf_saves_document_and_chunks(client, valid_pdf):
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("research.pdf", valid_pdf, "application/pdf")},
    )

    assert response.status_code == 201
    data = response.json()

    assert data["filename"] == "research.pdf"
    assert data["status"] == "ready"
    assert data["pages_processed"] == 1
    assert data["chunks_created"] >= 1


def test_upload_rejects_non_pdf_filename(client):
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("notes.txt", b"some text", "text/plain")},
    )

    assert response.status_code == 415


def test_upload_rejects_invalid_pdf(client):
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("broken.pdf", b"not a real PDF", "application/pdf")},
    )

    assert response.status_code == 400


def test_upload_rejects_pdf_without_extractable_text(client):
    import fitz

    pdf = fitz.open()
    pdf.new_page()
    pdf_bytes = pdf.tobytes()
    pdf.close()

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("empty.pdf", pdf_bytes, "application/pdf")},
    )

    assert response.status_code == 422
