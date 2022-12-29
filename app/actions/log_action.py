import logging


class LogAction:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)

    async def action(self, meta, message):
        self.logger.info('%s – %s', meta, message)
