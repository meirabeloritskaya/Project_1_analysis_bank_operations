import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import json
import pandas as pd

from src.utils import (
    greeting,
    calculate_cashback,
    get_valid_date,
    get_transactions_by_date,
    top_5_trans_by_amount,
    read_user_settings,
    get_exchange_rate,
    get_stock_prices,
    json_result,
)


def test_greeting():
    current_time = datetime.now().time()
    if 5 <= current_time.hour < 12:
        expected_greeting = "Доброе утро!"
    elif 12 <= current_time.hour < 18:
        expected_greeting = "Добрый день!"
    elif 18 <= current_time.hour < 23:
        expected_greeting = "Добрый вечер!"
    else:
        expected_greeting = "Добрый ночи!"

    assert greeting() == expected_greeting


def test_calculate_cashback():
    assert calculate_cashback(-100) == 1
    assert calculate_cashback(-50) == 0
    assert calculate_cashback(100) == 0
    assert calculate_cashback(0) == 0


@patch("builtins.input", side_effect=["25.12.2020"])
def test_get_valid_date(mock_input):
    expected_date = "25.12.2020 00:00:00"
    assert get_valid_date() == expected_date


def test_get_transactions_by_date():
    transactions = [
        {
            "Дата операции": "01.12.2020 12:00:00",
            "Номер карты": "1234",
            "Сумма операции": -200,
        },
        {
            "Дата операции": "15.12.2020 12:00:00",
            "Номер карты": "5678",
            "Сумма операции": -300,
        },
        {
            "Дата операции": "01.01.2021 12:00:00",
            "Номер карты": "1234",
            "Сумма операции": -100,
        },
    ]
    date = "31.12.2020 00:00:00"
    expected_transactions = [
        {"last_dijits": "1234", "total_spent": -200, "cashback": 2},
        {"last_dijits": "5678", "total_spent": -300, "cashback": 3},
    ]
    assert get_transactions_by_date(transactions, date) == expected_transactions


@patch("pandas.read_excel")
def test_top_5_trans_by_amount(mock_read_excel):
    mock_df = pd.DataFrame(
        {
            "Дата платежа": [
                "01.12.2020",
                "02.12.2020",
                "03.12.2020",
                "04.12.2020",
                "05.12.2020",
            ],
            "Сумма платежа": [500, 400, 300, 200, 100],
            "Категория": [
                "Категория1",
                "Категория2",
                "Категория3",
                "Категория4",
                "Категория5",
            ],
            "Описание": [
                "Описание1",
                "Описание2",
                "Описание3",
                "Описание4",
                "Описание5",
            ],
        }
    )
    mock_read_excel.return_value = mock_df
    path = "dummy_path"
    expected_top_5 = [
        {
            "date": "01.12.2020",
            "amount": 500,
            "category": "Категория1",
            "description": "Описание1",
        },
        {
            "date": "02.12.2020",
            "amount": 400,
            "category": "Категория2",
            "description": "Описание2",
        },
        {
            "date": "03.12.2020",
            "amount": 300,
            "category": "Категория3",
            "description": "Описание3",
        },
        {
            "date": "04.12.2020",
            "amount": 200,
            "category": "Категория4",
            "description": "Описание4",
        },
        {
            "date": "05.12.2020",
            "amount": 100,
            "category": "Категория5",
            "description": "Описание5",
        },
    ]
    assert top_5_trans_by_amount(path) == expected_top_5


def test_read_user_settings():
    file_path = "dummy_settings.json"
    dummy_settings = {"key": "value"}

    with patch(
        "builtins.open", unittest.mock.mock_open(read_data=json.dumps(dummy_settings))
    ):
        assert read_user_settings(file_path) == dummy_settings

    with patch("builtins.open", side_effect=FileNotFoundError):
        assert read_user_settings(file_path) is None

    with patch("builtins.open", unittest.mock.mock_open(read_data="invalid json")):
        assert read_user_settings(file_path) is None


@patch("requests.get")
def test_get_exchange_rate(mock_get):
    api_key = "dummy_key"
    BASE_URL = "https://dummy_url/"
    user_currencies = ["USD", "EUR"]

    mock_response = MagicMock()
    mock_response.json.return_value = {"conversion_rates": {"USD": 0.013, "EUR": 0.011}}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    expected_rates = [
        {"currency": "USD", "rate": round(1 / 0.013, 2)},
        {"currency": "EUR", "rate": round(1 / 0.011, 2)},
    ]
    assert get_exchange_rate(api_key, BASE_URL, user_currencies) == expected_rates


@patch("yfinance.Ticker")
def test_get_stock_prices(mock_ticker):
    user_stocks = ["AAPL", "GOOG"]

    mock_stock = MagicMock()
    mock_stock.info = {"currentPrice": 150}
    mock_ticker.return_value = mock_stock

    expected_prices = [
        {"stock": "AAPL", "price": 150},
        {"stock": "GOOG", "price": 150},
    ]
    assert get_stock_prices(user_stocks) == expected_prices


def test_json_result():
    greeting_msg = "Доброе утро!"
    transactions = [{"last_dijits": "1234", "total_spent": -200, "cashback": 2}]
    top_transactions = [
        {
            "date": "01.12.2020",
            "amount": 500,
            "category": "Категория1",
            "description": "Описание1",
        }
    ]
    exchange_rate = [
        {"currency": "USD", "rate": 76.92},
        {"currency": "EUR", "rate": 90.91},
    ]
    stock_prices = [{"stock": "AAPL", "price": 150}]

    expected_result = json.dumps(
        {
            "greeting": greeting_msg,
            "cards": transactions,
            "top_transactions": top_transactions,
            "currency_rates": exchange_rate,
            "stock_prices": stock_prices,
        },
        indent=4,
        ensure_ascii=False,
    )

    assert (
        json_result(
            greeting_msg, transactions, top_transactions, exchange_rate, stock_prices
        )
        == expected_result
    )


if __name__ == "__main__":
    test_greeting()
    test_calculate_cashback()
    test_get_valid_date()
    test_get_transactions_by_date()
    test_top_5_trans_by_amount()
    test_read_user_settings()
    test_get_exchange_rate()
    test_get_stock_prices()
    test_json_result()
    print("All tests passed!")
