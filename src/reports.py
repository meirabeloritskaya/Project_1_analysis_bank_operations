import logging
import pandas as pd
from datetime import datetime
import functools
from read_transactions_excel import get_data_transactions

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(
    "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/logs/reports.log",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def report_to_file(filename='file_report.txt'):
    '''Декоратор записывает данные по отчету в файл'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(result))
                logger.info('записан результат отчета в файл')
            return result
        return wrapper
    return decorator

@report_to_file('file_report.txt')
def spending_by_category(transactions, category, date=None):
    '''функция возвращает траты по категориям за последние три месяца'''

    try:
        transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
        print(transactions['Дата операции'])
        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, '%d.%m.%Y')

        start_date = end_date - pd.DateOffset(months=3)


        filtered_transactions = transactions[(transactions['Дата операции'] >= start_date) &
                                             (transactions['Дата операции'] <= end_date) &
                                             (transactions['Категория'] == category)]

        if filtered_transactions.empty:
            logger.info("Нет данных для указанного периода и категории")
            return []

        grouped_transactions = filtered_transactions.resample('M', on='Дата операции').agg({
                'Сумма операции': 'sum'
        }).reset_index()

        logger.info(f'Траты за последние три месяца по категории {category}')

        print("Данные после группировки:")
        print(grouped_transactions)

        return grouped_transactions.to_dict(orient='records')

    except Exception as e:
          print(f"ошибка {e}")
          logger.error(f'ошибка {e}')
          return []

if __name__ == '__main__':
    path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    list_trans = get_data_transactions(path)

    transactions = pd.DataFrame(list_trans)

    category = 'Переводы'
    date = '30.12.2021'

    result = spending_by_category(transactions, category, date)
    print(*result, sep='\n')
