import logging
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "read_transactions_excel.log")
file_handler = logging.FileHandler(path, encoding="utf-8")
logger = logging.getLogger(__name__)
# file_handler = logging.FileHandler(
#     "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/logs/read_transactions_excel.log",
#     encoding="utf-8",
# )
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_data_transactions(path):
    """чтение файла с транзакциями"""

    try:
        df = pd.read_excel(path)
        logger.info(f"открытие файла {path}")
        logger.info("Получение информации о транзакциях")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"путь к файлу {path} не найден")
        return "{}"
    except ValueError as e:
        logger.error(f"Ошибка при парсинге Excel файла: {str(e)}")
        return "{}"


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "data", "operations.xls")
    # path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    list_trans = get_data_transactions(path)

    for trans in list_trans:
        print(trans)
