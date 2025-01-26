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


# Имя файла с текстом
texts = load_texts_from_file("texts.txt")
# Индекс файла с текстом
current_text_index = 0


# Функция отправки сообщения
def send_message() -> None:
    global current_text_index
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Почта отправителя
    from_email = os.getenv("from_email")
    # Почта получателя
    to_email = os.getenv("to_email")
    # Пароль приложения от почты отправителя
    password = os.getenv("password")

    # Тема письма
    subject = "Тестовое письмо"
    # Тело сообщения
    body = texts[current_text_index]

    msg = MIMEMultipart()
    # Кто отправляет сообщение
    msg["From"] = from_email
    # Кому отправлятся сообщение
    msg["To"] = to_email
    # Тема сообщения
    msg["Subject"] = subject

    # Тело сообщения
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
    else:
        print("Письмо успешно отправлено!")

    # Переключатель к другому сообщению
    current_text_index += 1
    # Проверка на индекс
    if current_text_index >= len(texts):
        current_text_index = 0


# Отправляет сообщения каждые 4 часа
schedule.every(4).hours.do(send_message)

# Бесконечный цикл для отправки сообщений до его прерывания
while True:
    schedule.run_pending()
    time.sleep(1)
