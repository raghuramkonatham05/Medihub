import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_otp_email(to_email, otp):
    # ✅ READ ENV VARS INSIDE FUNCTION (CRITICAL FIX)
    SENDER_EMAIL = os.getenv("SMTP_EMAIL")
    SENDER_PASSWORD = os.getenv("SMTP_PASSWORD")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        raise RuntimeError(
            f"SMTP credentials not configured. "
            f"SMTP_EMAIL={SENDER_EMAIL}, SMTP_PASSWORD={'SET' if SENDER_PASSWORD else None}"
        )

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "MediHub Password Reset OTP"

    body = f"""
Hello,

Your OTP to reset your MediHub password is:

{otp}

This OTP is valid for 10 minutes.

If you did not request this, please ignore this email.

Regards,
MediHub Team
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {e}")
def send_welcome_email(to_email):
    import os
    import smtplib
    from email.message import EmailMessage

    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials not configured")

    msg = EmailMessage()
    msg["Subject"] = "Welcome to MediHub 🎉"
    msg["From"] = f"MediHub <{SMTP_EMAIL}>"
    msg["To"] = to_email

    msg.set_content(
        f"""
Welcome to MediHub!

Your account has been created successfully.

You can now securely log in and start uploading your medical lab reports.
Our AI-powered system will help you understand your health reports better.

Thank you for choosing MediHub.

— MediHub Team
        """
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
def send_welcome_email(to_email):
    import os
    import smtplib
    from email.message import EmailMessage

    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials not configured")

    msg = EmailMessage()
    msg["Subject"] = "Welcome to MediHub 🎉"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    msg.set_content(f"""
Hi 👋,

Welcome to MediHub!

Your account has been created successfully.
You can now upload medical reports and get AI-powered insights.

🔐 Login anytime using your registered email.

If you did not create this account, please ignore this email.

Regards,
MediHub Team
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
