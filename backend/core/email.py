# backend/core/email.py
from __future__ import annotations
import resend
from backend.core.config import settings


def _init():
    resend.api_key = settings.RESEND_API_KEY


def _html_wrapper(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:40px 20px;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0"
             style="background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

        <tr>
          <td style="background:linear-gradient(135deg,#111827,#374151);padding:32px 40px;text-align:center;">
            <div style="font-size:26px;font-weight:800;color:#ffffff;letter-spacing:-0.5px;">
              🏢 Portale Fornitori Condomini
            </div>
          </td>
        </tr>

        <tr>
          <td style="padding:40px 40px 32px;">
            {body}
          </td>
        </tr>

        <tr>
          <td style="background:#f8fafc;padding:20px 40px;text-align:center;border-top:1px solid #e5e7eb;">
            <p style="margin:0;font-size:12px;color:#9ca3af;line-height:1.6;">
              Hai ricevuto questa email perché sei registrato come fornitore sul Portale Fornitori Condomini.<br/>
              Se non sei stato tu, ignora questa email o contattaci a
              <a href="mailto:{settings.EMAIL_FROM}" style="color:#4f8ef7;">{settings.EMAIL_FROM}</a>
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def send_richiesta_preventivo_email(
    to_email: str,
    fornitore_nome: str,
    admin_nome: str,
    servizio_nome: str,
    condominio_denominazione: str,
    condominio_indirizzo: str,
    descrizione: str | None,
) -> bool:
    """Notifica un fornitore registrato per il servizio di una nuova richiesta di preventivo."""
    _init()
    dashboard_url = f"{settings.FRONTEND_URL}/dashboard"

    descrizione_html = (
        f'<p style="margin:16px 0 0;font-size:14px;color:#374151;line-height:1.6;">{descrizione}</p>'
        if descrizione else ""
    )

    body = f"""
    <h2 style="margin:0 0 8px;font-size:22px;font-weight:700;color:#111827;">
      Nuova richiesta di preventivo
    </h2>
    <p style="margin:0 0 24px;font-size:15px;color:#6b7280;line-height:1.6;">
      Ciao <strong style="color:#111827;">{fornitore_nome}</strong>,<br/>
      hai ricevuto una nuova richiesta di preventivo per il servizio
      <strong>{servizio_nome}</strong>.
    </p>

    <table cellpadding="0" cellspacing="0" width="100%"
           style="border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;margin-bottom:24px;">
      <tr style="background:#f9fafb;">
        <td style="padding:12px 16px;font-size:13px;font-weight:600;color:#374151;
                   border-bottom:1px solid #e5e7eb;width:160px;">Richiesto da</td>
        <td style="padding:12px 16px;font-size:13px;color:#111827;
                   border-bottom:1px solid #e5e7eb;">{admin_nome}</td>
      </tr>
      <tr>
        <td style="padding:12px 16px;font-size:13px;font-weight:600;color:#374151;
                   border-bottom:1px solid #e5e7eb;">Servizio</td>
        <td style="padding:12px 16px;font-size:13px;color:#111827;
                   border-bottom:1px solid #e5e7eb;">{servizio_nome}</td>
      </tr>
      <tr style="background:#f9fafb;">
        <td style="padding:12px 16px;font-size:13px;font-weight:600;color:#374151;">Condominio</td>
        <td style="padding:12px 16px;font-size:13px;color:#111827;">
          {condominio_denominazione} — {condominio_indirizzo}
        </td>
      </tr>
    </table>
    {descrizione_html}

    <div style="text-align:center;margin:32px 0 0;">
      <a href="{dashboard_url}"
         style="display:inline-block;background:linear-gradient(135deg,#111827,#374151);
                color:#ffffff;text-decoration:none;font-weight:700;font-size:15px;
                padding:14px 36px;border-radius:12px;letter-spacing:0.01em;">
        Vai alla dashboard
      </a>
    </div>
    """

    try:
        resend.Emails.send({
            "from": f"Portale Fornitori Condomini <{settings.EMAIL_FROM}>",
            "to": [to_email],
            "subject": f"Nuova richiesta di preventivo — {servizio_nome}",
            "html": _html_wrapper("Nuova richiesta di preventivo", body),
        })
        return True
    except Exception as e:
        print(f"[email] Errore invio richiesta preventivo a {to_email}: {e}")
        return False
