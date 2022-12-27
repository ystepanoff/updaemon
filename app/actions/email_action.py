import asyncio
import aiosmtplib
from email.message import EmailMessage
from typing import List


class EmailAction:
    def __init__(self, **kwargs) -> None:
        self.recipients = kwargs.get('to', [])
        self.smtp_host = kwargs.get('smtp_host', 'updaemon-smtp')
        self.sender = kwargs.get('from', 'updaemon@updaemon')

    async def action(self, meta: str, message: str) -> None:
        email = EmailMessage()
        email['From'] = self.sender
        email['To'] = ', '.join(self.recipients)
        email['Subject'] = meta
        email.set_content(message)

        print(self.smtp_host)
        await aiosmtplib.send(message=email, hostname=self.smtp_host, port=25)
