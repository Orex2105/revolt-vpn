import datetime
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='utils.Greeting')


def set_greeting() -> str:
    hour_now = datetime.datetime.now().hour
    if hour_now >= 23 or hour_now < 6:
        hi_message = "Доброй ночи"
    elif hour_now in range(6, 12):
        hi_message = "Доброе утро"
    elif hour_now in range(12, 16):
        hi_message = "Добрый день"
    else:
        hi_message = "Добрый вечер"

    return hi_message