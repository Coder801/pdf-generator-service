from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

MAX_HTML_BYTES = 20 * 1024 * 1024  # a report with an embedded font and drawings fits well

class PDFSize(BaseModel):
    """Model representing the size of the PDF."""
    
    width: int
    height: int


class PDFRequest(BaseModel):
    """Request model for PDF generation."""
    
    currentPage: HttpUrl
    currentLanguage: str = "en"
    size: PDFSize
    format: Literal["full", "a4"] = "full"
    orientation: Literal["portrait", "landscape"] = "portrait"


class PDFHtmlRequest(BaseModel):
    """Request model for PDF generation from a ready HTML page.

    The page is printed as it is: its own @page rule sets the paper, margins and the
    margin boxes (page numbers); scripts and external files are not needed.
    """

    html: str = Field(min_length=1, max_length=MAX_HTML_BYTES)
    orientation: Literal["portrait", "landscape"] = "portrait"
    filename: str = Field(default="document.pdf", max_length=200)


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str
    service: str
    dev_mode: bool
