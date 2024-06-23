import logging
from datetime import datetime
from read_transactions_excel import get_data_transactions
import pandas as pd

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(
    "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/logs/views.log",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


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


def calculate_cashback(amount):
    if amount < 0:
        return round(abs(amount) / 100)
    else:
        return 0


def get_transactions_by_date(transactions, date):
    """вывод номера карты, суммы операций, кешбек"""
    logger.info("вывод номера карты, суммы операций, кешбек")
    filtered_transactions = [
        trans for trans in transactions if trans["Дата операции"][:10] == date[:10]
    ]
    transaction_details = []

    for trans in filtered_transactions:
        number_card = trans["Номер карты"]
        amount = trans["Сумма операции"]
        cashback = calculate_cashback(amount)

        # Добавляем детали текущей транзакции в список
        transaction_details.append(
            {"last_dijits": number_card, "total_spent": amount, "cashback": cashback}
        )

    return transaction_details


def top_5_trans_by_amount(path):
    df = pd.read_excel(path)
    top_5_transactions = df.nlargest(5, "Сумма платежа")
    top_details = []
    for index, trans in top_5_transactions.iterrows():
        date_payment = trans["Дата платежа"]
        amount_payment = trans["Сумма платежа"]
        category_payment = trans["Категория"]
        description_payment = trans["Описание"]
        top_details.append(
            {
                "date": date_payment,
                "amount": amount_payment,
                "category": category_payment,
                "description": description_payment,
            }
        )
    return top_details


if __name__ == "__main__":
    my_date = "16.02.2018 00:00:00"
    my_path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    print(greeting())
    my_transactions = get_data_transactions(my_path)
    my_data_by_date = get_transactions_by_date(my_transactions, my_date)
    # print(my_data_by_date)
    print(*my_data_by_date, sep="\n")
    my_top_5_trans_by_amount = top_5_trans_by_amount(my_path)
    print(*my_top_5_trans_by_amount, sep="\n")
