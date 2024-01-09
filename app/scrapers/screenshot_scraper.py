from typing import Optional

from scrapers.base_scraper import BaseScraper

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


class ScreenshotScraper(BaseScraper):
    def __init__(self, *args, **kwargs) -> None:
        self.__driver = webdriver.Chrome(
            service=ChromiumService(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            )
        )
        super().__init__(*args, **kwargs)

    async def scrape(self, attempts: int, timeout: int) -> Optional[str]:
        try:
            self.__driver.get(self.__remote)
            return self.__driver.get_screenshot_as_base64()
        except:
            if attempts > 0:
                return await self.scrape(attempts - 1, timeout)
