from .base_scraper import BaseScraper, SUPPORTED_TYPES
from .dummy_scraper import DummyScraper

SCRAPERS_REGISTRY = {
    'dummy': DummyScraper,
}
