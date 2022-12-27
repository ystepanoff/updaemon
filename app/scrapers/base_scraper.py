from typing import Dict, Any, Optional
import logging

SUPPORTED_TYPES = {
    'html',
}


class BaseScraper:
    def __init__(self, name: str, params: Dict[str, Any]) -> None:
        assert 'type' in params, "Scraper params must contain 'type'."
        assert 'source' in params, "Scraper params must contain 'source'."
        assert params['type'] in SUPPORTED_TYPES, "Scraper type must be one of {}.".format(', '.join(SUPPORTED_TYPES))
        self.name = name
        self.type = params['type']
        self.source = params['source']
        self.logger = logging.getLogger(__name__)

    async def scrape(self, attempts: int = 5) -> Optional[str]:
        raise NotImplementedError("Each child class must implement scrape().")
