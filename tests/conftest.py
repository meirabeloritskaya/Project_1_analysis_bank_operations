import pytest
from datetime import datetime
import json


@pytest.fixture
def transactions():
    return [
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


@pytest.fixture
def expected_transactions():
    return [
        {"last_dijits": "1234", "total_spent": -200, "cashback": 2},
        {"last_dijits": "5678", "total_spent": -300, "cashback": 3},
    ]


@pytest.fixture
def mock_exchange_rate_response():
    return {"conversion_rates": {"USD": 0.013, "EUR": 0.011}}


@pytest.fixture
def expected_exchange_rates():
    return [
        {"currency": "USD", "rate": round(1 / 0.013, 2)},
        {"currency": "EUR", "rate": round(1 / 0.011, 2)},
    ]


@pytest.fixture
def mock_stock_info():
    return {"currentPrice": 150}


@pytest.fixture
def expected_stock_prices():
    return [
        {"stock": "AAPL", "price": 150},
        {"stock": "GOOG", "price": 150},
    ]


@pytest.fixture
def user_settings():
    return {"key": "value"}


@pytest.fixture
def invalid_user_settings():
    return "invalid json"


@pytest.fixture
def user_currencies():
    return ["USD", "EUR"]


@pytest.fixture
def user_stocks():
    return ["AAPL", "GOOG"]


@pytest.fixture
def greeting_expected():
    current_time = datetime.now().time()
    if 5 <= current_time.hour < 12:
        return "Доброе утро!"
    elif 12 <= current_time.hour < 18:
        return "Добрый день!"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер!"
    else:
        return "Добрый ночи!"


@pytest.fixture
def expected_top_5():
    return [
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


@pytest.fixture
def greeting_msg():
    return "Доброе утро!"


@pytest.fixture
def transactions_for_json():
    return [{"last_dijits": "1234", "total_spent": -200, "cashback": 2}]


@pytest.fixture
def top_transactions():
    return [
        {
            "date": "01.12.2020",
            "amount": 500,
            "category": "Категория1",
            "description": "Описание1",
        }
    ]


@pytest.fixture
def exchange_rate():
    return [
        {"currency": "USD", "rate": 76.92},
        {"currency": "EUR", "rate": 90.91},
    ]


@pytest.fixture
def stock_prices():
    return [{"stock": "AAPL", "price": 150}]


@pytest.fixture
def expected_json_result(greeting_msg, transactions_for_json, top_transactions, exchange_rate, stock_prices):
    return json.dumps(
        {
            "greeting": greeting_msg,
            "cards": transactions_for_json,
            "top_transactions": top_transactions,
            "currency_rates": exchange_rate,
            "stock_prices": stock_prices,
        },
        indent=4,
        ensure_ascii=False,
    )
