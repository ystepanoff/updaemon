import requests
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

    def get_data(self, attempts: int = 5) -> Optional[str]:
        def get_html() -> str:
            response = requests.get(self.source)
            if response.status_code == 200:
                return response.text
            else:
                self.logger.error("Failed to fetch HTML: {}, attempt left: {}.".format(response.code, attempts))
                return self.get_data(attempts - 1)

        if attempts > 0:
            if self.type == 'html':
                return get_html()

    def process(self, data: str) -> Any:
        raise NotImplementedError("Each child class must implement process().")
