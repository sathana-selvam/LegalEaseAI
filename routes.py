from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiGenerator
from ai_core.generator import create_docx


router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    details: dict


class DocumentResponse(BaseModel):
    success: bool
    message: str
    document: str
    file_url: str | None = None


@router.get("/")
def root():
    return {
        "application": "LegalEase",
        "message": "LegalEase API is running",
        "status": "online"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):

    try:

        if not request.details:
            raise HTTPException(
                status_code=400,
                detail="Please provide document details."
            )

        generator = GeminiGenerator()

        document_text = generator.generate_document(
            document_type=request.document_type,
            user_details=request.details
        )

        file_path = create_docx(
            document_text=document_text,
            document_type=request.document_type
        )

        filename = Path(file_path).name

        return DocumentResponse(
            success=True,
            message="Document generated successfully.",
            document=document_text,
            file_url=f"/download/{filename}"
        )

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get("/download/{filename}")
def download_document(filename: str):

    docs_folder = Path("docs")

    file_path = docs_folder / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )
    )s