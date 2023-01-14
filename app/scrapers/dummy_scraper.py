from typing import Optional
import requests

from scrapers.base_scraper import BaseScraper


class DummyScraper(BaseScraper):
    async def scrape(self, attempts: int = 5, timeout: int = 60) -> Optional[str]:
        response = requests.get(self.remote, timeout=timeout)
        if response.status_code == 200:
            return response.text
        self.logger.error('Failed to fetch: %d, attempts left: %s.', response.status_code, attempts)
        if attempts > 0:
            return await self.scrape(attempts - 1)
