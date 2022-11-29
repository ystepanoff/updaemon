import logging


class LogAction:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def action(self, message):
        self.logger.info(message)
