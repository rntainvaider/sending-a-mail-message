import os
import smtplib
import time

import schedule
from dotenv import load_dotenv

_ = load_dotenv()

# Заготовленные текста
texts = ["text1", "text2", "text3", "text4", "text5"]


# Функция для отправки сообщений
def send_email() -> None:
    current_text_input = 0
    sender_email = os.getenv("sender_email")  # Email отправителя
    receiver_email = os.getenv("receiver_email")  # Email получателя
    password = os.getenv("password")  # Пароль отправителя от почты

    # Соодщение для отправления
    message = f"Message: Ваш текст\n\n{texts[current_text_input]}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 465) as server:
            server.starttls  # Защита соединения
            server.login(user=sender_email, password=password)
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
            print(f"Email отправлен: {texts[current_text_input]}")
    except Exception as e:
        print(f"Ошибка: {e}")

    # Переключатель на следующий текст
    current_text_input += 1
    if current_text_input >= len(texts):
        current_text_input = 0


# Планирование отправки сообщения каждые 30 секунд
schedule.every(30).seconds.do(send_email)

# Запуск цикла
while True:
    schedule.run_pending()
    time.sleep(1)
