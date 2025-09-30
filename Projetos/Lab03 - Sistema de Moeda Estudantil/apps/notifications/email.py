# apps/notifications/email.py
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def _get_site_meta():
    """
    Metadados básicos do site usados nos e-mails.
    Evita depender de request/get_current_site.
    """
    site_name = getattr(settings, "SITE_NAME", "Moeda Acadêmica")
    site_url = getattr(settings, "SITE_URL", "http://127.0.0.1:8000")
    from_public = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
    return site_name, site_url, from_public


# --------------------------------------------------------------------
# 1) E-mail quando o professor envia moedas ao aluno
# --------------------------------------------------------------------
def send_moedas_recebidas(*, aluno, professor, valor, motivo=""):
    """
    Envia um e-mail simples e em HTML notificando o aluno do crédito.
    """
    if not getattr(aluno, "email", None):
        return  # sem e-mail, não há para onde enviar

    site_name, site_url, from_public = _get_site_meta()

    ctx = {
        "aluno": aluno,
        "professor": professor,
        "valor": valor,
        "motivo": motivo,
        "site_name": site_name,
        "site_url": site_url,
        "from_email_public": from_public,
    }

    subject = f"[{site_name}] Você recebeu {valor} moedas"
    text_body = render_to_string("emails/moedas_recebidas.txt", ctx)
    html_body = render_to_string("emails/moedas_recebidas.html", ctx)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[aluno.email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)


# --------------------------------------------------------------------
# 2) E-mail com CUPOM quando o aluno resgata uma vantagem
# --------------------------------------------------------------------
def send_cupom_resgatado(*, aluno, vantagem, codigo: str, custo: int):
    """
    Envia o cupom de resgate para o aluno.
    """
    if not getattr(aluno, "email", None):
        return

    site_name, site_url, from_public = _get_site_meta()

    ctx = {
        "aluno": aluno,
        "vantagem": vantagem,
        "codigo": codigo,
        "custo": custo,
        "empresa": getattr(vantagem, "empresa", None),
        "site_name": site_name,
        "site_url": site_url,
        "from_email_public": from_public,
    }

    subject = f"[{site_name}] Cupom de resgate — {vantagem.titulo}"
    text_body = render_to_string("emails/cupom_resgatado.txt", ctx)
    html_body = render_to_string("emails/cupom_resgatado.html", ctx)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[aluno.email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)
