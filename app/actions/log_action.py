from actions.base_action import BaseAction


class LogAction(BaseAction):
    async def action(self, meta: str, message: str) -> None:
        self.logger.info('%s – %s', meta, message)
