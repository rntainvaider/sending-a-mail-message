import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import schedule
from dotenv import load_dotenv

_ = load_dotenv()


def load_texts_from_file(filename: str) -> list[str]:
    with open(filename, "r", encoding="UTF-8") as file:
        return [line.strip() for line in file.readlines()]


texts = load_texts_from_file("texts.txt")
current_text_index = 0


def send_message() -> None:
    global current_text_index
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    from_email = os.getenv("from_email")
    to_email = os.getenv("to_email")
    password = os.getenv("password")

    subject = "Тестовое письмо"
    body = texts[current_text_index]

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")

    current_text_index += 1
    if current_text_index >= len(texts):
        current_text_index = 0


schedule.every(30).seconds.do(send_message)

while True:
    schedule.run_pending()
    time.sleep(1)
