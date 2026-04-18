import os
import smtplib
from pathlib import Path
from typing import Dict, List, Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.config import settings


class EmailService:
    """Reusable SMTP email service with Jinja2 templating support."""

    def __init__(self):
        self.sender = settings.EMAIL_USER
        self.password = settings.EMAIL_PASS
        self.host = settings.EMAIL_HOST
        self.port = settings.EMAIL_PORT
        templates_root = Path(__file__).resolve().parent.parent / "templates" / "emails"
        self.templates_dir = templates_root
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(["html", "xml"])
        )

    def render_template(self, template_name: str, context: Optional[Dict[str, any]] = None) -> str:
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**(context or {}))
        except Exception as exc:
            print(f"[EMAIL] Failed to render template {template_name}: {exc}")
            return ""

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        attachments: Optional[List[str]] = None,
    ) -> bool:
        """Send an HTML email (optionally with attachments)."""
        if not to_email:
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(html_body, "html"))

            for attachment_path in attachments or []:
                if not attachment_path or not os.path.exists(attachment_path):
                    continue
                with open(attachment_path, "rb") as attachment_file:
                    part = MIMEApplication(attachment_file.read(), Name=os.path.basename(attachment_path))
                part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                msg.attach(part)

            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.sendmail(self.sender, to_email, msg.as_string())

            print(f"[EMAIL] Sent '{subject}' to {to_email}")
            return True
        except Exception as exc:
            print(f"[EMAIL] Failed to send email to {to_email}: {exc}")
            return False

    def send_templated_email(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        context: Optional[Dict[str, any]] = None,
        attachments: Optional[List[str]] = None,
    ) -> bool:
        html_body = self.render_template(template_name, context)
        if not html_body:
            return False
        return self.send_email(to_email, subject, html_body, attachments=attachments)


email_service = EmailService()

