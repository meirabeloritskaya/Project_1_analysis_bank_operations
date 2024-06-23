import logging
import json
from datetime import datetime

import pandas as pd
import requests

import yfinance as yf


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
    date_obj = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    first_day_of_month = date_obj.replace(day=1)
    start_date = first_day_of_month.strftime("%d.%m.%Y")
    end_date = date[:10]

    filtered_transactions = [
        trans
        for trans in transactions
        if start_date <= trans["Дата операции"][:10] <= end_date
    ]

    transaction_details = []

    for trans in filtered_transactions:
        number_card = trans["Номер карты"]
        amount = trans["Сумма операции"]
        cashback = calculate_cashback(amount)

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

        result = [
            {"currency": "USD", "rate": usd_rate},
            {"currency": "EUR", "rate": eur_rate},
        ]

        return result
    except Exception as e:
        print(e)
        return None


def get_stock_prices():
    symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    prices = []

    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            data = stock.info

            # Проверяем, есть ли поле 'currentPrice' в полученных данных
            if "currentPrice" in data:
                stock_info = {"stock": symbol, "price": data["currentPrice"]}
                prices.append(stock_info)
            else:
                print(f"Цена акции {symbol} не найдена")
        except Exception as e:
            print(f"Ошибка при получении данных для акции {symbol}: {str(e)}")

    return prices


def json_result(greeting, transactions, top_transactions, exchange_rate, stock_prices):
    result = {
        "greeting": greeting,
        "cards": transactions,
        "top_transactions": top_transactions,
        "currency_rates": exchange_rate,
        "stock_prices": stock_prices,
    }
    return json.dumps(result, indent=4, ensure_ascii=False)
