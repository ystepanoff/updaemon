from typing import Dict, Any, Optional
import logging


class BaseScraper:
    def __init__(self, remote: str, params: Dict[str, Any]) -> None:
        self.__remote = remote
        self.__params = params
        self.__logger = logging.getLogger(__name__)

    async def scrape(self, attempts: int, timeout: int) -> Optional[str]:
        raise NotImplementedError("Each child class must implement scrape().")
