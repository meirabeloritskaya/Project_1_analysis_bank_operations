
import yfinance as yf
import json


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
    return json.dumps(result, ensure_ascii=False, indent=4)


# Пример использования:
my_greeting = "Доброе утро!"
my_transactions = ["транзакция 1", "транзакция 2", "транзакция 3"]
my_top_transactions = ["топ транзакция 1", "топ транзакция 2", "топ транзакция 3"]
my_exchange_rate = {"currency": "USD", "rate": 87.11}

# Получаем цены акций
my_stock_prices = get_stock_prices()

# Формируем и печатаем JSON
my_json_result = json_result(
    my_greeting, my_transactions, my_top_transactions, my_exchange_rate, my_stock_prices
)
print(my_json_result)
