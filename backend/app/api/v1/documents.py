import fitz
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Document, DocumentChunk
from app.services.pdf_ingestion import extract_pdf_chunks

router = APIRouter(prefix="/documents", tags=["Documents"])

MAX_PDF_SIZE = 10 * 1024 * 1024  # 10 MiB


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    file: UploadFile,
    db: Session = Depends(get_db),
) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    filename = file.filename.replace("\\", "/").rsplit("/", 1)[-1]

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF files are supported")

    try:
        pdf_bytes = await file.read(MAX_PDF_SIZE + 1)
    finally:
        await file.close()

    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    if len(pdf_bytes) > MAX_PDF_SIZE:
        raise HTTPException(
            status_code=413,
            detail="PDF exceeds the 10 MiB upload limit",
        )

    if not pdf_bytes.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="Invalid PDF file")

    try:
        page_count, chunks = extract_pdf_chunks(pdf_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (fitz.FileDataError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail="Could not read PDF") from exc

    document = Document(filename=filename, status="processing")
    db.add(document)

    try:
        db.flush()

        for index, chunk in enumerate(chunks):
            db.add(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    page_number=chunk["page_number"],
                    content=chunk["content"],
                )
            )

        document.status = "ready"
        db.commit()
        db.refresh(document)

        return {
            "id": document.id,
            "filename": document.filename,
            "status": document.status,
            "pages_processed": page_count,
            "chunks_created": len(chunks),
        }

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save document",
        ) from exc
