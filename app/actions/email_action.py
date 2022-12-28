import asyncio
from aiosmtplib import SMTP, send
from email.message import EmailMessage
from typing import List


class EmailAction:
    def __init__(self, **kwargs) -> None:
        self.recipients = kwargs.get('to', [])
        self.hostname = ''
        self.port = 0
        self.username = ''
        self.password = ''

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
