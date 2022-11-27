from base_scraper import BaseScraper
from typing import Dict, Any, Optional


class DummyScraper(BaseScraper):
    def __init__(self, name: str, params: Dict[str, Any]) -> None:
        super(TestScraper, self).__init__(name, params)
        self.data = self.get_data(attempts=5)

    def process(self, data: str) -> Optional[str]:
        return self.data
