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
    """проверяем , что транзакция была тратой"""
    logger.info("проверяем , что транзакция была тратой")
    if amount < 0:
        return abs(amount) // 100
    else:
        return 0


def get_valid_date():
    """Ввод даты для получения информации по транзакциям"""
    print(
        """Предлагаю вывести по каждой карте последние 4 цифры, общую сумму расходов и кешбек.
А также могу вывести топ-5 транзакций по сумме платежа, курс валют (USD, EUR) и стоимост акций из S&P500!"""
    )
    while True:
        input_date = input(
            "Введите дату в формате дд.мм.гггг за период 2018 - 2021: "
        ).strip()
        try:
            datetime_obj = datetime.strptime(input_date, "%d.%m.%Y")
            if 2018 <= datetime_obj.year <= 2021:
                formatted_date = datetime_obj.strftime("%d.%m.%Y %H:%M:%S")
                return formatted_date
        except ValueError:
            print("Некорректный формат даты")


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
    """вывод топ 5 транзакций по сумме платежа"""
    logger.info("вывод топ 5 транзакций по сумме платежа")
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


def read_user_settings(file_path):
    """чтение user_settings"""
    logger.info("чтение user_settings")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            user_settings = json.load(f)
            return user_settings
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{file_path}': {e}")
        return None


def get_exchange_rate(api_key, BASE_URL, user_currencies):
    """получение курса USD  и EUR"""
    logger.info("получение курса USD  и EUR ")
    try:
        url = f"{BASE_URL}{api_key}/latest/RUB"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            raise Exception(f"Error fetching exchange rate: {data['error-type']}")

        rates = data["conversion_rates"]
        result = []

        for currency in user_currencies:
            if currency in rates:
                rate = round(1 / rates[currency], 2)
                result.append({"currency": currency, "rate": rate})
            else:
                print(f"Currency rate for {currency} not found in API response.")
        return result
    except Exception as e:
        print(e)
        return None


def get_stock_prices(user_stocks):
    """получение курса stock_prices"""
    logger.info("получение курса stock_prices ")
    prices = []

    for symbol in user_stocks:
        try:
            stock = yf.Ticker(symbol)
            data = stock.info

            if "currentPrice" in data:
                stock_info = {"stock": symbol, "price": data["currentPrice"]}
                prices.append(stock_info)
            else:
                print(f"Цена акции {symbol} не найдена")
        except Exception as e:
            print(f"Ошибка при получении данных для акции {symbol}: {str(e)}")

    return prices


def json_result(greeting, transactions, top_transactions, exchange_rate, stock_prices):
    """вывод всей собранной информации в JSON формате"""
    logger.info("вывод всей собранной информации в JSON формате ")
    result = {
        "greeting": greeting,
        "cards": transactions,
        "top_transactions": top_transactions,
        "currency_rates": exchange_rate,
        "stock_prices": stock_prices,
    }
    return json.dumps(result, indent=4, ensure_ascii=False)
