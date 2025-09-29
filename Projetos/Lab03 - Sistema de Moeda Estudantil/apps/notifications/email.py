# apps/notifications/email.py
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_moedas_recebidas(aluno, professor, valor, motivo):
    """
    Envia e-mail HTML informando ao aluno que recebeu moedas.
    Retorna True se tentou enviar (aluno tem e-mail), False caso contrário.
    """
    to_email = (aluno.email or "").strip()
    if not to_email:
        return False  # Sem e-mail do aluno: não envia

    context = {
        "aluno": aluno,
        "professor": professor,
        "valor": int(valor),
        "motivo": motivo,
        "site_name": getattr(settings, "SITE_NAME", "Moeda Acadêmica"),
        "site_url": getattr(settings, "SITE_URL", "http://localhost:8000"),
        "from_email_public": getattr(settings, "DEFAULT_FROM_EMAIL", "moeda.academia@gmail.com"),
    }

    subject = f"Você recebeu {context['valor']} moedas — {context['site_name']}"
    from_email = settings.DEFAULT_FROM_EMAIL

    # Versões do corpo
    text_body = render_to_string("emails/moedas_recebidas.txt", context)
    html_body = render_to_string("emails/moedas_recebidas.html", context)

    msg = EmailMultiAlternatives(subject, text_body, from_email, [to_email])
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)
    return True
