import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to: str, subject: str, body: str) -> bool:
    """
    Send a plain-text email via Gmail SMTP.
    Returns True on success, False on failure.
    Reads credentials from MAIL_USERNAME and MAIL_PASSWORD env vars.
    """
    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    from_addr = os.environ.get("MAIL_FROM", username)

    if not username or not password:
        print("[email_sender] MAIL_USERNAME or MAIL_PASSWORD not set — skipping email.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = from_addr
    msg["To"]      = to
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(username, password)
            server.sendmail(from_addr, [to], msg.as_string())
        print(f"[email_sender] Email sent to {to}: {subject}")
        return True
    except Exception as e:
        print(f"[email_sender] Failed to send email to {to}: {e}")
        return False