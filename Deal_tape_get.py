# Этот файл заточен под работу с фьючерсами, для акций нужно изменить параметры.
# Плюс сейчас не хавтает аналитической части,
# она происходит уже в самой табдице (Посредством Google Sheets например).
# import os
import time
import intro.basek
import pandas as pd
from intro.quotation_dt import quotation_count
# import datetime
from pathlib import Path

from tinkoff.invest import (
    TradeInstrument,
    Client,
    MarketDataRequest,
    SubscribeTradesRequest,
    MarketDataResponse,
    SubscriptionAction,
)

TOKEN = intro.basek.TINKOFF_INVEST_DOG_NEW


def last_trades_array(trades: [MarketDataResponse.trade]):
    lp_array = pd.DataFrame([{
        'figi': trades.figi,
        'direction': trades.direction,
        'price': quotation_count(trades.price),
        'quanitty': trades.quantity,
        'time': pd.Timestamp(trades.time)
    }])
    return lp_array


def main():
    def request_iterator():
        yield MarketDataRequest(
                subscribe_trades_request=SubscribeTradesRequest(
                    subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                    instruments=[
                        TradeInstrument(
                            figi="FUTNASD06230") # Для примера взят фьючерс NASDAQ 06.23
                        ],
                    )
                )
        while True:
            time.sleep(0.01)

    with Client(TOKEN) as client:
        for marketdata in client.market_data_stream.market_data_stream(
            request_iterator()
        ):
            print(marketdata)
            if marketdata.trade==None:
                continue
            else:
                filepath1 = Path('csv_files/NASDAQ_Future0623_Trades_11_04_2023.csv')
                df = last_trades_array(marketdata.trade)
                df.to_csv(filepath1, sep=";", mode='a', header=False, index=False, escapechar=';')
                print(df)


if __name__ == "__main__":
    main()

