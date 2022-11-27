import aiosmtplib
from email.message import EmailMessage
from typing import List


class EmailAction:
    def __init__(self, smtp_host: str, sender: str, recipitents: List[str]) -> None:
        self.smtp_host = smtp_host
        self.sender = sender
        self.recipients = recipitents

    async def action(self, meta: str, message: str) -> None:
        email = EmailMessage()
        email.set_content(message)
        email['From'] = self.sender
        email['To'] = ', '.join(self.recipients)
        email['Subject'] = meta

        with await aiosmtplib.SMTP(self.smtp_host) as smtp:
            await smtp.send_message(email)
