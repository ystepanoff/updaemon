from typing import Dict, Any, Optional
import requests

from scrapers.base_scraper import BaseScraper


class DummyScraper(BaseScraper):
    def __init__(self, remote: str, params: Dict[str, Any]) -> None:
        super().__init__(remote, params)

    async def scrape(self, attempts: int = 5, timeout: int = 60) -> Optional[str]:
        response = requests.get(self.remote, timeout=timeout)
        if response.status_code == 200:
            return response.text
        self.logger.error('Failed to fetch: %d, attempts left: %s.', response.status_code, attempts)
        if attempts > 0:
            return await self.scrape(attempts - 1)
