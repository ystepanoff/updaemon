from typing import Any
import logging


class LogAction:
    def __init__(self, **kwargs: Any) -> None:
        name = kwargs.get('name', __name__)
        self.logger = logging.getLogger(name)

    async def action(self, meta: str, message: str) -> None:
        self.logger.info('%s – %s', meta, message)
