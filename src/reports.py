import logging
import pandas as pd
from datetime import datetime, timedelta
import functools
from src.read_transactions_excel import get_data_transactions
import json
import os

# Настройка логирования
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "reports.log")
file_handler = logging.FileHandler(path, encoding="utf-8")
logger = logging.getLogger(__name__)
#
# file_handler = logging.FileHandler(
#     "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/logs/reports.log",
#     encoding="utf-8",
# )
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def report_to_file(filename="file_report.json"):
    """Декоратор записывает данные по отчету в файл"""
    logger.info("создан декоратор для отчетов")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for entry in result:
                entry["Дата операции"] = entry["Дата операции"].strftime("%d.%m.%Y %H:%M:%S")
            with open(filename, "w+", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
                logger.info("Результат отчета записан в файл в формате JSON")
            return result

        return wrapper

    return decorator


@report_to_file("report.json")
def spending_by_category(transactions, category, date=None):
    """Функция возвращает траты по категориям за указанный месяц"""
    try:
        # Преобразование столбца 'Дата операции' в формат datetime
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%d.%m.%Y")

        # Начало и конец месяца для фильтрации
        start_date = end_date - timedelta(days=3 * 30)

        # Фильтрация транзакций по дате и категории
        filtered_transactions = transactions[
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
            & (transactions["Категория"] == category)
            & (transactions["Сумма платежа"] < 0)
        ]

        # Проверка, есть ли отфильтрованные данные
        if filtered_transactions.empty:
            logger.info("Нет данных для указанного периода и категории")
            print("Нет данных для указанного периода и категории")
            return []

        logger.info(f"Траты за указанный месяц по категории {category}")
        return filtered_transactions.to_dict(orient="records")

    except Exception as e:
        print(f"ошибка {e}")
        logger.error(f"ошибка {e}")
        return []


def get_unique_categories(transactions):
    """Функция для получения уникальных категорий из транзакций"""
    return transactions["Категория"].unique().tolist()


def choose_category(categories):
    """Функция для выбора категории из списка"""
    print("Предлагаю посмотреть отчет за траты по категориям за 3-х месячный период с указаной  вами датой!")
    print("Для этого выберите категорию из списка:")
    for idx, category in enumerate(categories):
        print(f"{idx + 1}. {category}")

    while True:
        try:
            choice = int(input("Введите номер категории: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            else:
                print("Неверный номер категории. Попробуйте снова.")
        except ValueError:
            print("Некорректный ввод. Введите номер категории.")


def get_valid_date():
    """Функция для ввода корректной даты"""
    while True:
        input_date = input("Введите дату в формате дд.мм.гггг: ").strip()
        try:
            datetime_obj = datetime.strptime(input_date, "%d.%m.%Y")
            return datetime_obj
        except ValueError:
            print("Некорректный формат даты. Попробуйте снова.")


def my_reports():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "data", "operations.xls")
    # path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    list_trans = get_data_transactions(path)
    transactions = pd.DataFrame(list_trans)

    categories = get_unique_categories(transactions)
    category = choose_category(categories)
    date = get_valid_date()

    result = spending_by_category(transactions, category, date.strftime("%d.%m.%Y"))
    print(*result, sep="\n")


if __name__ == "__main__":
    print(my_reports())
