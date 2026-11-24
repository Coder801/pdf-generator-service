from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.config import settings
from app.models import PDFHtmlRequest, PDFRequest, HealthCheckResponse
from app.pdf_service import generate_pdf_from_html, generate_pdf_from_url


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

        pdf_buffer = await generate_pdf_from_url(
            currentPage,
            currentLanguage,
            width=width,
            height=height,
            page_format=request.format,
            orientation=request.orientation,
        )

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


@router.post("/generate-pdf-html")
async def generate_pdf_html(request: PDFHtmlRequest):
    """Generate an A4 PDF from a ready HTML page sent in the request.

    For pages behind a login: the caller renders the page itself and sends its HTML,
    so the browser here needs no session and no access to the caller's address.
    """
    try:
        pdf_buffer = await generate_pdf_from_html(request.html, request.orientation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
    name = request.filename if request.filename.lower().endswith(".pdf") else f"{request.filename}.pdf"
    ascii_name = name.encode("ascii", "ignore").decode() or "document.pdf"
    return Response(
        content=pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{ascii_name}"; filename*=UTF-8\'\'{quote(name)}'
            )
        },
    )
