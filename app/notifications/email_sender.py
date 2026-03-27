import smtplib
import os
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def _send(to, subject, body):
    username  = os.environ.get("MAIL_USERNAME")
    password  = os.environ.get("MAIL_PASSWORD")
    from_addr = os.environ.get("MAIL_FROM", username)

    if not username or not password:
        print("[email_sender] Credentials not set — skipping.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = from_addr
    msg["To"]      = to
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(from_addr, [to], msg.as_string())
        print(f"[email_sender] Sent to {to}: {subject}")
    except Exception as e:
        print(f"[email_sender] Failed: {e}")


def send_email(to: str, subject: str, body: str) -> bool:
    """Send email in background thread so it never blocks the request."""
    thread = threading.Thread(target=_send, args=(to, subject, body), daemon=True)
    thread.start()
    return True