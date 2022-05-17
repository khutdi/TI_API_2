from intro.quotation_dt import quotation_count
from datetime import datetime
from pathlib import Path
import tinkoff.invest
import intro.basek
import intro.accid
import pandas as pd
import pandas_ta as ta
import time

# Здесь запросы токена и id из stub файлов, и самого клиента из библиотеки Тинькофф
TOKEN = intro.basek.TINKOFF_INVEST_DOG_NEW
SDK_client = tinkoff.invest.Client(TOKEN)
User_acc_ID = intro.accid.ACC_ID

# Здесь переменные по которым будет производиться запрос свечей (Figi инструмента,
# интервал данных и месяц, а так же числа за который нужны данные.
# Эти значения выбираем вручную из полученного списка инструментов
cti_future = 'FUTBR0622000'
tf = tinkoff.invest.CandleInterval.CANDLE_INTERVAL_5_MIN
month_data = 5
first_date = 1
last_date = 30

# Функция получения данных свечей по инструменту
def current_trade_instrument_candles(cti_figi, interval, chosen_month):
    try:
        with SDK_client as client:
            days_in_month = range(first_date, last_date)
            for i in days_in_month:
                start = [2022, chosen_month, i, 13, 0]  #time from 10 a.m. UTC+3
                end = [2022, chosen_month, i, 22, 0]  #time to 7 p.m. UTC+3
                cti_candles = client.market_data.get_candles(
                    figi=cti_figi,
                    from_=datetime(start[0], start[1], start[2], start[3], start[4]),
                    to=datetime(end[0], end[1], end[2], end[3], end[4]),
                    interval=interval
                )
                # Обработка запроса по форме
                candle_df = create_candle_df(cti_candles.candles)
                # Запись полученных данных в табличку
                # указать название файла соответствующее инструменту
                filepath = Path('csv_files/brent062022_list_1min.csv')
                df = pd.DataFrame(candle_df)
                df.to_csv(filepath, mode='a')

                time.sleep(1)
                print('Record ', i, ' complete')

    except tinkoff.invest.RequestError as e:
        print(str(e))

# Форма для обработки полученных данных
def create_candle_df(candles: [tinkoff.invest.HistoricCandle]):
    candle_df = pd.DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': quotation_count(c.open),
        'close': quotation_count(c.close),
        'high': quotation_count(c.high),
        'low': quotation_count(c.low),
    } for c in candles])
    return candle_df

current_trade_instrument_candles(cti_future, tf, month_data)
