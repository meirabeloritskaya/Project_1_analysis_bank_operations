from datetime import datetime
import math
import logging
from read_transactions_excel import get_data_transactions
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "services.log")
file_handler = logging.FileHandler(path, encoding="utf-8")
logger = logging.getLogger(__name__)

# file_handler = logging.FileHandler(
#     "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/logs/services.log",
#     encoding="utf-8",
# )
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_valid_month():
    """Функция для ввода корректного месяца и года."""
    print("Выберите условия для вашей инвесткопилки!")
    while True:
        input_date = input("Для этого введите месяц и год в формате гггг-мм за период 2018-2021: ").strip()
        try:
            logger.info("Преобразование даты в формат datetime")
            datetime_obj = datetime.strptime(input_date, "%Y-%m")
            if 2018 <= datetime_obj.year <= 2021:
                return datetime_obj
            else:
                print("Введите год в диапазоне 2018-2021.")
        except ValueError:
            print("Некорректный формат даты. Попробуйте еще раз!")


def get_limit():
    """Функция для выбора лимита из предложенных значений."""
    while True:
        print("Выберите лимит для округления (10, 50, 100 руб):")
        print("1. 10 руб")
        print("2. 50 руб")
        print("3. 100 руб")
        choice = input("Введите номер выбранного лимита: ").strip()
        logger.info("выбор лимита для инвесткопилки")
        if choice == "1":
            return 10
        elif choice == "2":
            return 50
        elif choice == "3":
            return 100
        else:
            print("Некорректный выбор. Попробуйте еще раз.")


def investment_bank(month_start, transactions, limit):
    """Функция для вычисления суммы инвесткопилки с заданным месяцем и лимитом."""
    logger.info("Начало вычисления суммы инвесткопилки")
    total_savings = 0.0

    for transaction in transactions:
        date_str = transaction.get("Дата платежа")

        if not isinstance(date_str, str) or date_str.lower() == "nan":
            logger.info("Отсутствует дата транзакции")
            continue

        try:
            transaction_date = datetime.strptime(date_str, "%d.%m.%Y")
            if transaction_date.year == month_start.year and transaction_date.month == month_start.month:
                amount = transaction["Сумма операции"]

                if amount >= 0:
                    logger.info("Положительная транзакция, пропуск")
                    continue
                else:
                    modul_amount = -amount
                    rounded_amount = math.ceil(modul_amount / limit) * limit
                    difference = rounded_amount - modul_amount
                    total_savings += difference

        except ValueError:
            logger.error(f"Ошибка формата даты: {date_str}")
            continue

    logger.info("Вычисление суммы инвесткопилки завершено")
    return round(total_savings, 2)


def my_services():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "data", "operations.xls")
    # path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    list_trans = get_data_transactions(path)  # Получаем данные транзакций из Excel

    month_start = get_valid_month()  # Запрашиваем у пользователя месяц и год
    limit = get_limit()  # Запрашиваем у пользователя лимит для округления

    total_savings = investment_bank(month_start, list_trans, limit)
    print(f"Сумма инвесткопилки за {month_start.strftime('%Y-%m')}: {total_savings}")


if __name__ == "__main__":
    print(my_services())
