from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Адрес твоего фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

class PDFRequest(BaseModel):
    currentPage: str

@app.post("/generate-pdf")
async def generate_pdf(request: PDFRequest):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1800, 'height': 800})

        await page.goto(request.currentPage, wait_until='networkidle')

        await page.wait_for_selector('body', timeout=10000)

        await asyncio.sleep(2)  # Ensure all dynamic content is loaded

        content_handle = await page.query_selector('body')
        bounding_box = await content_handle.bounding_box()

        width = bounding_box['width'] if bounding_box else 1800
        height = bounding_box['height'] if bounding_box else 2000

        pdf_buffer = await page.pdf(
            width=f'{width}px',
            height=f'{height}px',
            print_background=True,
        )

        await browser.close()

        return Response(
            content=pdf_buffer,
            media_type='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename="generated.pdf"'
            }
        )