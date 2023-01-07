from typing import Any
from email.message import EmailMessage
from aiosmtplib import send

from actions.base_action import BaseAction


class EmailAction(BaseAction):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.recipients = kwargs.get('recipients', [])
        self.hostname = kwargs.get('hostname', 'localhost')
        self.port = kwargs.get('port', 25)
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')

    async def action(self, meta: str, message: str) -> None:
        email = EmailMessage()
        email['From'] = self.username
        email['To'] = ', '.join(self.recipients)
        email['Subject'] = meta
        email.set_content(message)

        await send(
            email,
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
        )
