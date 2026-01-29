from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.config import settings
from app.models import PDFRequest, HealthCheckResponse
from app.pdf_service import generate_pdf_from_url


router = APIRouter()


@router.get("/", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="ok",
        service="PDF Generator",
        dev_mode=settings.DEV_MODE
    )


@router.post("/generate-pdf")
async def generate_pdf(request: PDFRequest):
    """Generate PDF from a web page."""
    try:
        currentPage = str(request.currentPage)
        currentLanguage = str(request.currentLanguage)
        width = request.size.width
        height = request.size.height

        pdf_buffer = await generate_pdf_from_url(currentPage, currentLanguage, width=width, height=height)

        return Response(
            content=pdf_buffer,
            media_type='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename="generated.pdf"'
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}"
        )
