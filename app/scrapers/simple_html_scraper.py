from typing import Optional
import requests
from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class SimpleHTMLScraper(BaseScraper):
    def _process(self, html: str) -> Optional[str]:
        soup = BeautifulSoup(html, features='lxml')
        tag = self.params.get('tag', 'html')
        attrs = self.params.get('attrs')
        result = soup.find(tag, attrs=attrs)
        if result is not None:
            result = str(result)
        return result

    async def scrape(self, attempts: int = 5, timeout: int = 60) -> Optional[str]:
        response = requests.get(self.remote, timeout=timeout)
        if response.status_code == 200:
            return self._process(response.text)
        self.logger.error('Failed to fetch: %d, attempts left: %s.', response.status_code, attempts)
        if attempts > 0:
            return await self.scrape(attempts - 1)
