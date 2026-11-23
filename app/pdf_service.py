import asyncio
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from playwright.async_api import async_playwright, Page

from app.config import settings


async def get_page_dimensions(page: Page) -> tuple[int, int]:
    """Get dimensions of the page content."""
    content_handle = await page.query_selector('body')
    bounding_box = await content_handle.bounding_box()

    if not bounding_box:
        return settings.DEFAULT_VIEWPORT_WIDTH, settings.DEFAULT_VIEWPORT_HEIGHT

    return int(bounding_box['width']), int(bounding_box['height'])


def add_lang_param(url: str, lang: str) -> str:
    """Add lang parameter to URL."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    params['lang'] = [lang]

    new_query = urlencode(params, doseq=True)
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return new_url


A4_WIDTH_PX = 794  # 210mm at 96 DPI
A4_HEIGHT_PX = 1123  # 297mm at 96 DPI


async def generate_pdf_from_url(
    url: str,
    lang: str = "en",
    width: int = 1440,
    height: int = 800,
    page_format: str = "full",
    orientation: str = "portrait",
) -> bytes:
    """Generate PDF from the given URL."""
    # Add lang parameter to URL
    url_with_lang = add_lang_param(url, lang)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
            ]
        )
        page = await browser.new_page()

        try:
            await page.set_viewport_size({
                'width': width,
                'height': height
            })

            print(f"Attempting to navigate to: {url_with_lang}")

            await page.goto(url_with_lang, wait_until='networkidle', timeout=30000)

            print(f"Successfully loaded: {url}")

            await page.wait_for_selector('body', timeout=settings.DEFAULT_TIMEOUT)
            await asyncio.sleep(settings.PAGE_LOAD_DELAY)

            if page_format == "a4":
                # Scale down so the layout keeps the requested viewport width
                # and is split into A4 pages.
                landscape = orientation == "landscape"
                paper_width = A4_HEIGHT_PX if landscape else A4_WIDTH_PX
                scale = max(0.1, min(1.0, paper_width / width))
                pdf_buffer = await page.pdf(
                    format='A4',
                    landscape=landscape,
                    scale=scale,
                    print_background=True,
                )
            else:
                _, content_height = await get_page_dimensions(page)

                pdf_buffer = await page.pdf(
                    width=f'{width}px',
                    height=f'{content_height}px',
                    print_background=True,
                )

            return pdf_buffer

        finally:
            await browser.close()
