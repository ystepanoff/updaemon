from typing import Any
import logging


class BaseAction:
    def __init__(self, **kwargs: Any) -> None:
        name = kwargs.get('name', __name__)
        self.logger = logging.getLogger(name)

    async def action(self, meta: str, message: str) -> None:
        raise NotImplementedError("Each child class must implement action().")
