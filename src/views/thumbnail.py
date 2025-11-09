from fastapi import APIRouter, HTTPException, Response
from ..utils.Scraper import FakeBrowser
from playwright.async_api import Browser, Page, async_playwright, Playwright
from pathlib import Path


class Thumbnail:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.add_api_route(
            "/thumbnail",
            self.from_url,
            methods=["GET"],
            responses={
                400: {"description": "Failed to load the image"},
                200: {"description": "Image fetched succesfully", "content": {"image/png": {}},}
            }
        )
        
        self.router.on_shutdown = [self.handle_shutdown]    
        self.browser: FakeBrowser | None = None
        self.playwright: Playwright | None = None
        self.playwright_browser: Browser | None = None
    
    async def handle_shutdown(self) -> None:
        if self.playwright_browser:
            await self.playwright_browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def from_url(self, url: str):
        if not self.browser:
            self.playwright = await async_playwright().start()
            self.playwright_browser = await self.playwright.chromium.launch(headless=True)
            page = await self.playwright_browser.new_page()
            self.browser = FakeBrowser(self.playwright_browser, page)

        path: Path | None = await self.browser.capture(url, False)
        if path is None:
            raise HTTPException(status_code=400, detail="Page load error")
        
        return Response(content=path.read_bytes(), media_type="image/png")