from playwright.async_api import Browser, Page
from pathlib import Path
import re
import logging

logger = logging.getLogger("thumbnail-gen")

URL = str

class FakeBrowser:
    def __init__(self, browser: Browser, page: Page) -> None:
        logger.info("Initializing a new browser")
        self.browser: Browser = browser
        self.page: Page = page

    @staticmethod
    def sanitize_url(url: URL) -> str:
        return re.sub(r"[^A-Za-z0-9._-]", "_", url.lower())


    async def capture(self, url: URL, force_refresh: bool = False) -> Path | None:
        if not url.startswith("https://") or not url.startswith("http://"):
            url = "https://" + url
        
        logger.info(f"Getting page {url[:64]}")
        sanitized_url: str = FakeBrowser.sanitize_url(url)

        save_path: str = f"/tmp/{sanitized_url}.png"

        if Path(save_path).exists() and not force_refresh:
            logger.info("Path already exists, returning")
            return Path(save_path)
        
        logger.info(f"Capturing webpage")

        try:
            await self.page.goto(url, timeout=15000)
        except Exception as e:
            logger.error(e)
            return None
        
        await self.page.screenshot(path=save_path, type="png", animations="disabled")
        return Path(save_path)