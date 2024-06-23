import logging
from datetime import datetime
from read_transactions_excel import get_data_transactions
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
MY_API_KEY = os.getenv("API_KEY")
MY_BASE_URL = os.getenv("BASE_URL")

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


def get_exchange_rate(api_key, BASE_URL):
    try:
        url = f"{BASE_URL}{api_key}/latest/RUB"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            raise Exception(f"Error fetching exchange rate: {data['error-type']}")

        rates = data["conversion_rates"]
        usd_to_rub = rates.get("USD")
        eur_to_rub = rates.get("EUR")
        if usd_to_rub is None or eur_to_rub is None:
            raise Exception("Currency rates not found")

        usd_rate = round(1 / usd_to_rub, 2)
        eur_rate = round(1 / eur_to_rub, 2)

        result = (
            f"currency: 'USD',\nrate: {usd_rate}\n"
            f"currency: 'EUR',\nrate: {eur_rate}"
        )

        return result
    except Exception as e:
        print(e)
        return None


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
    my_exchange_rate = get_exchange_rate(MY_API_KEY, MY_BASE_URL)
    print(my_exchange_rate)
