from pydantic import BaseModel, HttpUrl


class PDFRequest(BaseModel):
    """Request model for PDF generation."""
    
    currentPage: HttpUrl
    currentLanguage: str = "en"


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str
    service: str
    dev_mode: bool
