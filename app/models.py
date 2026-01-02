from pydantic import BaseModel, HttpUrl

class PDFSize(BaseModel):
    """Model representing the size of the PDF."""
    
    width: int
    height: int


class PDFRequest(BaseModel):
    """Request model for PDF generation."""
    
    currentPage: HttpUrl
    currentLanguage: str = "en"
    size: PDFSize


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str
    service: str
    dev_mode: bool
