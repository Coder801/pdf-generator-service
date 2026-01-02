import os


class Settings:
    """Application settings."""
    
    DEV_MODE: bool = os.getenv("DEV_MODE", "false").lower() == "true"
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "")
    
    # Viewport settings
    DEFAULT_VIEWPORT_WIDTH: int = 1440
    DEFAULT_VIEWPORT_HEIGHT: int = 800
    
    # Timeout settings
    DEFAULT_TIMEOUT: int = 10000
    PAGE_LOAD_DELAY: int = 2
    
    # App metadata
    APP_TITLE: str = "PDF Generator Service"
    APP_DESCRIPTION: str = "Generate PDFs from web pages using Playwright"
    APP_VERSION: str = "1.0.0"


settings = Settings()
