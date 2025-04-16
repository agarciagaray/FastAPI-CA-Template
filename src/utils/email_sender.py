import smtplib
from email.message import EmailMessage

def send_email(subject, body, to, smtp_user, smtp_password, smtp_server, smtp_port, attachment=None, attachment_filename=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to
    msg.set_content(body)

    if attachment and attachment_filename:
        msg.add_attachment(
            attachment,
            maintype="application",
            subtype="octet-stream",
            filename=attachment_filename
        )

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(msg)