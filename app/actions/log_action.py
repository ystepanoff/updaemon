import logging


class LogAction:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def action(self, meta, message):
        self.logger.info(message)
