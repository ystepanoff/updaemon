from typing import Dict, Any, Optional
import requests

from scrapers.base_scraper import BaseScraper


class DummyScraper(BaseScraper):
    def __init__(self, name: str, params: Dict[str, Any]) -> None:
        super(DummyScraper, self).__init__(name, params)
        self.data = None

    async def scrape(self, attempts: int = 5) -> Optional[str]:
        response = requests.get(self.source)
        if response.status_code == 200:
            return response.text
        else:
            self.logger.error("Failed to fetch HTML: {}, attempts left: {}.".format(response.status_code, attempts))
            if attempts > 0:
                return await self.fetch(attempts - 1)
