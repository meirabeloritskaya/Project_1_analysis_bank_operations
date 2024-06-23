import logging
from datetime import datetime


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(
    "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/logs/read_transactions_excel.log",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def greeting():
    """Приветствие"""
    logger.info("Приветствие")

    current_time = datetime.now().time()
    if 5 <= current_time.hour < 12:
        greeting = "Доброе утро!"
    elif 12 <= current_time.hour < 18:
        greeting = "Добрый день!"
    elif 18 <= current_time.hour < 23:
        greeting = "Добрый вечер!"
    else:
        greeting = "Добрый ночи!"
    return greeting


if __name__ == "__main__":
    print(greeting())
