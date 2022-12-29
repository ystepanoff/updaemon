from typing import Dict, Any, Optional
import requests

from scrapers.base_scraper import BaseScraper


class DummyScraper(BaseScraper):
    def __init__(self, remote: str, params: Dict[str, Any]) -> None:
        super(DummyScraper, self).__init__(remote, params)

    async def scrape(self, attempts: int = 5) -> Optional[str]:
        response = requests.get(self.remote)
        if response.status_code == 200:
            return response.text
        else:
            self.logger.error("Failed to fetch HTML: {}, attempts left: {}.".format(response.status_code, attempts))
            if attempts > 0:
                return await self.fetch(attempts - 1)
