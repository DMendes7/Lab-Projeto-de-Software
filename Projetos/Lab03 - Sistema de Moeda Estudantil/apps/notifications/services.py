from dataclasses import dataclass
from django.core.mail import send_mail
from django.conf import settings

@dataclass
class EmailResult:
    ok: bool
    error: str = ""

class NotificacaoService:
    @staticmethod
    def enviar_email(to: str, subject: str, body: str) -> EmailResult:
        try:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to], fail_silently=False)
            return EmailResult(True)
        except Exception as e:
            return EmailResult(False, str(e))
