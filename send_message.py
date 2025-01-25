import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

_ = load_dotenv()


def send_email(subject, body, to_email, from_email, password):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)

        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")


send_email(
    subject="Тестовое письмо",
    body="Привет, это тектовое сообщение!",
    to_email=os.getenv("receiver_email"),
    from_email=os.getenv("sender_email"),
    password=os.getenv("pass_app"),
)
